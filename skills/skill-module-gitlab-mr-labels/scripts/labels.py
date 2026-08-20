"""Pure label-set computation from layer-supplied tables."""

from __future__ import annotations

import re
from typing import Any


def label_names(raw: Any) -> list[str]:
    """Return label name strings from a GitLab API labels field."""
    if not raw:
        return []
    if isinstance(raw[0], dict):
        return [str(item.get("name")) for item in raw if item.get("name")]
    return [str(item) for item in raw]


def project_path(mr: dict[str, Any]) -> str:
    """Return group/repo from a merge request web_url path."""
    from urllib.parse import urlsplit

    url = mr.get("web_url") or ""
    path = urlsplit(url).path
    return path.split("/-/merge_requests/")[0].lstrip("/")


def validate_tables(cfg: dict[str, Any]) -> str | None:
    """Return an error when mapping tables cannot be used."""
    allowlist = cfg.get("allowlist")
    if not isinstance(allowlist, list) or not allowlist:
        return "tables.allowlist missing"
    for item in cfg.get("area_patterns") or []:
        if not isinstance(item, dict):
            return "tables.area_patterns needs pattern and label"
        pattern = item.get("pattern")
        if not item.get("label") or not isinstance(pattern, str):
            return "tables.area_patterns needs pattern and label"
        try:
            re.compile(pattern)
        except re.error as exc:
            return f"tables.area_patterns invalid regex: {exc}"
    return None


def compute_labels(
    title: str,
    current: list[str],
    path: str,
    cfg: dict[str, Any],
) -> list[str]:
    """Return the desired label set using only tables in cfg."""
    allowlist = set(cfg.get("allowlist") or [])
    if not allowlist:
        raise ValueError("tables.allowlist missing")
    keep_exact = set(cfg.get("keep_exact") or [])
    accepted = allowlist | keep_exact
    keep_prefixes = list(cfg.get("keep_prefixes") or [])
    type_from_conv = {
        k.lower(): v for k, v in (cfg.get("type_from_conv") or {}).items()
    }
    out: set[str] = set()

    conv_type = None
    scope = ""
    bang = False
    if type_from_conv:
        keys = sorted(type_from_conv, key=len, reverse=True)
        pattern = (
            r"^(?P<type>"
            + "|".join(re.escape(k) for k in keys)
            + r")(?:\((?P<scope>[^)]+)\))?(?P<bang>!)?:\s"
        )
        match = re.match(pattern, title.strip(), re.I)
        if match:
            conv_type = match.group("type").lower()
            scope = match.group("scope") or ""
            bang = bool(match.group("bang"))

    if conv_type is not None:
        out.add(type_from_conv[conv_type])
        bang_adds = cfg.get("bang_adds")
        if bang and bang_adds:
            out.add(bang_adds)
    else:
        for name in current:
            if name.startswith("type::") and name in allowlist:
                out.add(name)
                break

    blob = f"{scope} {title}"
    area = None
    for item in cfg.get("area_patterns") or []:
        if re.search(item["pattern"], blob, re.I):
            area = item["label"]
            break
    if area is None:
        for name in current:
            if name.startswith("area::") and name in allowlist:
                area = name
                break
    if area is None:
        old_area = cfg.get("old_area") or {}
        for name in current:
            if name in old_area:
                area = old_area[name]
                break
    if area is None:
        area = (cfg.get("repo_area") or {}).get(path)
    if area:
        out.add(area)

    haystack = f"{title} {scope} {' '.join(current)}".lower()
    for item in cfg.get("title_contains") or []:
        if item["needle"].lower() in haystack:
            out.add(item["add"])

    rename = cfg.get("rename") or {}
    for name in current:
        if name in keep_exact:
            out.add(name)
        for prefix in keep_prefixes:
            if name.startswith(prefix) and name in allowlist:
                out.add(name)
        if name in rename:
            target = rename[name]
            if target not in accepted:
                raise ValueError(f"rename target not in allowlist: {target}")
            out.add(target)

    return sorted(name for name in out if name in accepted)
