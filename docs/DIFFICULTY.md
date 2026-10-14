# 演算法難度八級制度

此難度是本知識庫內的**主觀、跨平台評估**，不等於 Codeforces Rating 或 LeetCode 的 Easy/Medium/Hard。

| 數值（remind.md） | 顯示 | 參考特徵 |
|:--:|---|---|
| `1` | 🔴 啟蒙 | 簡單輸入輸出、基本算術 |
| `2` | 🟠 基礎 | 基本條件判斷、簡單排序與模擬 |
| `3` | 🟡 初階 | 常見資料結構與入門演算法 |
| `4` | 🟢 中階 | 雙指針、二分、貪心等方法的基本運用 |
| `5` | 🩵 進階 | 需要較完整推導的 DP、圖論或綜合技巧 |
| `6` | 🔵 高階 | 複雜狀態設計、進階資料結構或技巧 |
| `7` | 🟣 專家 | 高難度競賽思維與嚴謹推導 |
| `8` | ⚫ 大師 | 極高難度的綜合競賽題 |
| `-` | ⚪ 未分類 | 尚未評級 |

## 修改方法

在 `problems/<平台>/<題目>/remind.md` 最上方使用：

```yaml
---
platform: Jisuanke
id: T1001
title: 計算A+B（新手教程）
difficulty: 1
tags: Basic I/O, Arithmetic
status: AC
solved: 2026-10-14
review_date: 2026-10-17
url: https://www.jisuanke.com/problem/T1001
---
```

另一題 UVA 11727 建議填 `difficulty: 2`。

舊筆記的 `Beginner`、`Basic`、`Medium`、Codeforces rating 數值等舊格式**不會被擅自換算**，索引暫時將其顯示為未分類。請自行逐題改成 `1` 到 `8`；如果想保留原網站分數，可以在筆記正文另註明。

注意：檔案必須以第一行 `---` 開頭；GitHub 首頁自動更新區位於 `README.md` 的 `AUTO-INDEX` 註解之間，請勿手動修改該區。
