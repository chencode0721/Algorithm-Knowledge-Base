# Algorithm Knowledge Base｜演算法刷題知識庫

以 **Codeforces / CSES / UVA / LeetCode** 為題目存放來源，以 **演算法 Tags** 與 **複習日期** 建立自動索引。

> 核心原則：每道題只保留一個來源資料夾（`solution.cpp` + `remind.md`）；演算法分類只是指向原始檔案的連結，不複製答案。

## 🚀 快速開始

需要 Python 3.10+（標準函式庫即可；不需安裝套件）。

```bash
# 新增一題 LeetCode（預設 WIP，尚未 AC）
python scripts/new_problem.py LeetCode 904 "Fruit Into Baskets" --tags "Sliding Window, Hash Map" --url "https://leetcode.com/problems/fruit-into-baskets/"

# 新增 CSES 題目，指定平台章節
python scripts/new_problem.py CSES 1068 "Weird Algorithm" --category "Introductory Problems" --tags "Simulation, Math"

# 完成解答後：將該題 remind.md 的 status 改成 AC、solved 改成日期
# 產生首頁索引
python scripts/generate_index.py

# 檢查 README 是否與題目同步（不修改檔案）
python scripts/generate_index.py --check

# 執行單元測試
python -m unittest discover -s tests -v
```

純 GitHub 網頁操作也可以：在 `problems/<平台>/<題目>/` 建立 `solution.cpp` 和 `remind.md`，把 `templates/remind.md` 的 `{{...}}` 改為實際資料即可。儲存至 `main` 後，GitHub Actions 會幫你生成索引。

## 📁 資料夾規則

```text
Algorithm-Knowledge-Base/
├── README.md                        # 人工導覽 + 自動索引
├── .github/workflows/update-index.yml # 每次 push / 手動 / 每日更新索引
├── .gitignore
├── problems/                        # 真正收錄並統計的題目
│   ├── Codeforces/
│   │   └── 4A-Watermelon/           # 例：按 ID-Title 命名
│   │       ├── solution.cpp
│   │       └── remind.md
│   ├── CSES/
│   │   └── Introductory-Problems/
│   │       └── 1068-Weird-Algorithm/
│   │           ├── solution.cpp
│   │           └── remind.md
│   ├── UVA/
│   └── LeetCode/
├── templates/                        # 新增題目時使用的樣板
│   ├── remind.md
│   ├── solution-main.cpp
│   └── solution-leetcode.cpp
├── scripts/
│   ├── new_problem.py               # 建立資料夾與兩份檔案
│   └── generate_index.py            # 自動更新統計、平台/Tags 索引、複習清單
├── examples/                         # 示範題（不計入自己的已解題數）
├── docs/
│   └── TAGS.md                      # 標籤規範
└── tests/                            # 自動化測試
```

可複製 `examples/UVA-10038-Jolly-Jumpers/` 至 `problems/UVA/10038-Jolly-Jumpers/` 參考完整範例。但**示範題不表示你真的 AC**；只有親自提交通過後才把 `status` 寫為 `AC`。

## 📝 remind.md 中繼資料規則

開頭必須有下列欄位（`tags` 為逗號分隔；**不是** YAML 陣列）：

```yaml
---
platform: LeetCode
id: 904
title: Fruit Into Baskets
difficulty: Medium
tags: Sliding Window, Hash Map
status: AC
solved: 2026-10-14
review_date: 2026-10-21
url: https://leetcode.com/problems/fruit-into-baskets/
---
```

- `platform`：只接受 `Codeforces`、`CSES`、`UVA`、`LeetCode`，且要與資料夾名稱相符。
- `id`：平台內唯一；純數字 `0001` 與 `1` 視為同一題，避免重複統計。
- `tags`：標籤名請參考 [TAGS.md](docs/TAGS.md)，建議每題 2–4 個。
- `status`：`WIP`（尚未提交通過）或 `AC`（確實通過）。
- `solved`：狀態為 `AC` 時必填 `YYYY-MM-DD`。
- `review_date`：選填，`YYYY-MM-DD` 或 `-`。已到期與未來七日複習清單依 **Asia/Taipei** 日期產生。
- `difficulty`、`url`：可填 `-`。

解析器只支援 **簡單的 `欄位: 文字`** 格式；請勿使用巢狀 YAML 結構。必要欄位有錯誤時會停止生成索引，避免 silently 遺漏題目。

## 🧾 建議刷題流程

1. 建立題目（用 `new_problem.py` 或 GitHub 網頁）；預設狀態為 `WIP`。
2. 在 `solution.cpp` 寫出能通過判題平台的解法。
3. 完成後更新 `remind.md`：`status: AC`、`solved: 日期`、演算法 `tags`、WA 原因、複習問題。
4. 本機執行 `python scripts/generate_index.py`，並提交 `git add . && git commit -m "solve: UVA 10038" && git push`。
5. 如果沒有在本機跑索引，GitHub Actions 也會在推送至 `main` 後重新生成並提交 `README.md`。

**重要**：GitHub Actions 的工作流程使用 `contents: write` 更新 README；如果倉庫啟用了保護分支或禁止工作流程寫入，可能無法自動提交。此時可在本機執行產生器後自己提交。定期排程只重新計算已到期複習題，**不會自動幫你把複習狀態改成完成**。

## 🔎 自動索引

保留這兩行標記。腳本只會替換它們之間的內容；其他 README 文字不受影響。

<!-- AUTO-INDEX:START -->
> 此區由 `python scripts/generate_index.py` 自動產生。只需修改各題的 `remind.md`；**不要直接改此區**。

## 📊 刷題統計

**總收錄：0 題｜已 AC：0 題｜進行中：0 題**

| 平台 | AC | WIP | 總題數 |
|:--|--:|--:|--:|
| Codeforces | 0 | 0 | 0 |
| CSES | 0 | 0 | 0 |
| UVA | 0 | 0 | 0 |
| LeetCode | 0 | 0 | 0 |

## 🗂️ 依平台查找

### Codeforces（0 題）

目前尚無題目。

### CSES（0 題）

目前尚無題目。

### UVA（0 題）

目前尚無題目。

### LeetCode（0 題）

目前尚無題目。

## 🧠 依演算法查找

目前尚無可分類的題目。

## 🔁 複習清單（台灣時間）

### 已到期

無到期題目。

### 接下來 7 天

無排定題目。

<sub>提醒：複習後請自行更新該題 `review_date`；系統只負責產生清單，不會自動判定你已經複習。</sub>
<!-- AUTO-INDEX:END -->

## 🔧 常用命令

```bash
# 補上本機索引
python scripts/generate_index.py

# 依照自己的日期手動檢查複習清單（例如）
python scripts/generate_index.py --today 2026-10-14

# 建立 Codeforces 題目
python scripts/new_problem.py Codeforces 4A "Watermelon" --tags "Math, Implementation" --difficulty 800
```

## 📌 注意事項

- `LeetCode` 的 `solution.cpp` 使用 `class Solution` 樣板；其他平台使用 `main()` 樣板。
- 不要提交執行檔、建置目錄、token 或登入憑證。
- 筆記以自己的話摘要題意，不要直接複製平台完整題目敘述。
- 將 GitHub 預設分支設為 `main`；如果使用別的預設分支，要同步修改 `.github/workflows/update-index.yml` 中的 `branches` 與檢查條件。
