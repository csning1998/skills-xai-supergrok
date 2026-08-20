# Collaboration Principles

本檔為跨專案常駐規範。只寫不隨產品改變的協作規則。技術棧細節在 `~/.grok/hooks/principles/`，僅在當次工作需要該棧時讀取。

## Section 1. Read Adjudication First

改已被 `planning/architecture_倉名*.md` 涵蓋的 `terraform/`、`ansible/`、`packer/`，或改 `planning/` 本身之前，必須先讀 `planning/decisions.md` 與至少一份對應的 `architecture*.md`。讀完之後寫出搬移、命名、DAG、當次範圍。未出現在檔名中的倉不套用此條。

未讀就動手，會把未裁決的命名與依賴寫進共用路徑。

## Section 2. Shared Modules Stay Generic

共用模組（`terraform/modules/`、`ansible/roles/utils_*`）只宣告資源結構。環境別名與產品名由呼叫端傳入。未在提示寫 `leave generic module` 不得改共用模組。

為單一呼叫端改共用模組，會把業務判斷擴散到所有呼叫端。

## Section 3. One Owner Mints Secrets

任一 Secret 只允許一個 Owner 負責 Generate。其餘層只許參照。消費層不得宣告 `random_password`，也不得呼叫 mint 模組。

消費層自己 mint，重建暫態層會弄丟持久資料的唯一密鑰。

## Section 4. Repair Declarations, Not Guests

宣告與現實不一致時，改宣告源頭，或 Assert 後停下。禁止把 `psql`、`ALTER USER`、`local-exec` 寫進 play、Terraform、Packer、腳本、Makefile 或 CI 當修補步驟。guest 上的唯讀偵錯不在 hook 閘內。用 guest SQL 改密碼或清 dirty 來蓋掉宣告漂移，下一次套用會再漂。該類命令需要當次 owner 片語 `allow guest sql`，且仍不得寫進檔案。

## Section 5. Stay In Scope

當次只做指定範圍。範圍外的問題用文字回報，不得順手修改。

範圍外修改會讓審查無法對齊當次裁決。

## Section 6. Verify Before Stating Versions

版本、預設值、旗標、棄用狀態先查官方來源。查不到就聲明缺乏資訊並停在該點。

以記憶陳述版本會寫出已失效的旗標與預設值。

Hook 只擋 Section 1 到 4 中可靜態判斷的動作。改共用模組請在提示寫 `leave generic module`。關閉 hook 請設 `ENGINEERING_PRINCIPLES_HOOK=0`。
