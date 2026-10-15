---
platform: UVA
id: 272
title: TEX Quotes
difficulty: 2
tags: String, Simulation, Implementation, State Machine
status: AC
solved: 2026-10-15
review_date: 2026-10-18
url: "https://onlinejudge.org/external/2/272.html"
---

# UVA 272 — TEX Quotes

## 1. 題目摘要 (Problem Summary)

將輸入文章中的一般雙引號 `"` 依出現順序轉成 TeX 引號：第一個雙引號替換成兩個反引號 `` ` ` ``（實際輸出為連續兩個反引號），下一個雙引號替換成兩個單引號 `''`，再下一個重新使用兩個反引號，如此交替直到 EOF。其他字元（含空白與換行）必須原樣輸出。

- 輸入：多行文字，讀取直到 EOF。
- 輸出：替換雙引號後的文字，保留原本排版。

## 2. 核心觀念 (Key Concepts)

- **Character-by-character Input（逐字元讀取）**：`cin.get(c)` 會讀取空白、Tab、換行，與 `cin >> c` 會跳過空白字元不同。
- **Boolean State（布林狀態）**：`bool X = false` 表示下一個 `"` 應被當成開引號；`true` 表示下一個應被當成閉引號。
- **Toggle（狀態切換）**：每遇到一次 `"` 就翻轉狀態。
- **EOF（檔案結尾）**：`while (cin.get(c))` 只要成功讀入字元就繼續執行。
- **State Machine（有限狀態機）**：只有「期待開引號」與「期待閉引號」兩種狀態。

## 3. 解題思路 (Approach)

依照**我原本 AC 的程式碼**分析：

1. 宣告 `char c`，每次保存讀進來的一個字元。
2. 宣告 `bool X = false`，初始化為「下一個雙引號是開引號」。
3. `while (cin.get(c))` 持續讀取到 EOF，不遺漏任何空白和換行。
4. 如果 `c == '"'`：
   - `X == false`：輸出兩個反引號（C++ 寫作 `cout << "``";`），再設 `X = true`。
   - 否則：輸出兩個單引號（`cout << "''";`），再設 `X = false`。
5. 如果不是雙引號，就 `cout << c` 原樣輸出。

### 原始 AC 程式碼

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    char c;
    bool X = false;
    while (cin.get(c)) {
        if (c == '"') {
            if (X == false) {
                X = true;
                cout << "``";
            }
            else {
                X = false;
                cout << "''";
            }
        }
        else {
            cout << c;
        }
    }
}
```

**程式追蹤**：輸入 `"Hi"` 時，第一次 `"` 讓 `X` 從 `false` 變 `true` 並輸出兩個反引號；`H`、`i` 原樣輸出；第二次 `"` 讓 `X` 從 `true` 變 `false` 並輸出 `''`。

## 4. 複雜度分析 (Complexity Analysis)

設全文共有 `N` 個字元：

- **Time Complexity：O(N)**，每個字元恰好讀取與判斷一次。
- **Space Complexity：O(1)**，只用 `char c` 和 `bool X` 等固定數量變數；輸出直接串流，不儲存全文。

## 5. 易錯觀念 (Common Mistakes)

- **誤用 `cin >> c`**：會跳過空格、Tab 和換行，文章格式遭破壞。
- **誤用 `while (cin >> c)`**：同樣會遺失空白；應使用 `cin.get(c)`。
- **每行把 `X` 設回 `false`**：引號配對狀態可能跨行延續，狀態應從文章開始維持到 EOF。
- **將輸出寫成單個符號**：開引號是兩個反引號，閉引號是兩個單引號，不是一個。
- **把單引號 `'` 也替換**：本題僅處理 ASCII 雙引號 `"`。
- **把反引號與單引號搞混**：反引號是鍵盤上的 `` ` ``；單引號是 `'`。

## 6. 邊界測資 (Edge Cases)

**單組引號**

輸入：
```text
"Hi"
```
輸出：
```text
``Hi''
```

**多組引號（狀態交替）**

輸入：
```text
"A" "B"
```
輸出：
```text
``A'' ``B''
```

**跨行且保留換行**

輸入：
```text
"Hello
world"
```
輸出：
```text
``Hello
world''
```

**沒有雙引號：完全不變**

輸入：
```text
A B
C D
```
輸出：
```text
A B
C D
```

## 7. 其他解法 (Alternative Solutions)

我的原版寫法是 `if / else` 切換布林值，已經簡單正確。若希望少寫幾行，可先依狀態輸出，再統一切換：

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    char c;
    bool opening = true;
    while (cin.get(c)) {
        if (c == '"') {
            cout << (opening ? "``" : "''");
            opening = !opening;
        } else {
            cout << c;
        }
    }
}
```

這是**替代寫法，不取代原本 AC 程式碼**。複雜度一樣為 O(N) 時間、O(1) 額外空間。

## 8. 複習重點 (Review Questions)

**2026-10-18 複習時，先不要看解答：**

1. 為什麼 `cin.get(c)` 可以保留空白與換行，但 `cin >> c` 不行？
2. `bool X = false` 在原程式中代表什麼？每讀到一個雙引號，狀態如何改變？
3. 如果開引號在第一行、閉引號在下一行，為什麼不能每行重設 `X`？
4. 為什麼 `while (cin.get(c))` 能正確處理不固定行數的輸入？
5. 不看解答，能否用一個 `bool` 和一個 `char` 在 5 分鐘內重寫？

**複習目標**：先口述狀態機，再手寫完整程式，驗證雙引號交替與換行保留。

## 9. 解題紀錄 (Submission Record)

- Result：AC（依本人提供）
- Language：C++
- Solved：2026-10-15
- Next Review：2026-10-18（三天後）
- Original Approach：`cin.get(c)` 逐字元處理；`bool X` 控制開、閉引號交替；其餘字元原樣輸出。
