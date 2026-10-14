# 升級方式（不會影響你既有的 AC 解答）

請將此 ZIP 解壓縮後的**以下檔案**，放到 GitHub Repo 的對應路徑，取代同名內容：

- `scripts/generate_index.py` — README 自動按 8 級排序
- `scripts/new_problem.py` — 新題可指定 `--difficulty 1..8`，支援 Jisuanke
- `templates/remind.md` — 補上難度說明註記
- `docs/DIFFICULTY.md` — 新增說明頁
- `tests/test_difficulty.py` — 新增難度排序測試

`tests/test_index.py` 在壓縮包裡也附有原始版本供本機測試，但**不需要覆蓋倉庫的舊版測試**。

重要：**不要**用舊版起始專案的 README 覆蓋 GitHub 首頁。既有 `problems/`、`solution.cpp` 與 `remind.md` 不需要刪除。

原筆記調整：
- `problems/Jisuanke/T1001-Calculate-A-Plus-B/remind.md` 的 `difficulty: Beginner` → `difficulty: 1`
- `problems/UVA/11727-Cost-Cutting/remind.md` 的 `difficulty: Beginner` → `difficulty: 2`

完成修改並 Commit 後，GitHub Actions 自動重新產生 README 裡的難度清單。

若在本機操作：`python -m unittest discover -s tests -v` 和 `python scripts/generate_index.py`。
