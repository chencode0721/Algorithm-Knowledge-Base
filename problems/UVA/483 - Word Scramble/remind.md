---
platform: UVA
id: 483
title: Word Scramble
difficulty: 2
tags: String, Simulation, Implementation
status: AC
solved: 2026-10-15
review_date: 2026-10-18
url: https://onlinejudge.org/external/4/483.html
---

# UVA 483 — Word Scramble

## 1. 題目摘要 (Problem Summary)

輸入多行英文文字，將每個單字內部的字元順序反轉，但不改變單字在句子中的排列順序。

- **輸入**：多行文字，讀取直到 EOF。
- **輸出**：反轉每個單字，保留原本的空格與換行。
- **注意**：反轉的是單字內的字元，而不是單字的排列順序。

## 2. 核心觀念 (Key Concepts)

- **Character Input**：`cin.get(c)` 可以讀取空格與換行。
- **Vector**：使用 `vector<char>` 暫存單字。
- **Reverse Traversal**：利用反向 `for` 迴圈輸出字元。
- **Delimiter**：空格 `' '` 與換行 `'\n'` 都代表單字結束。
- **EOF**：輸入結束後仍須處理最後一個單字。

## 3. 解題思路 (Approach)

1. 宣告 `char c` 與 `vector<char> v`。
2. 使用 `while(cin.get(c))` 逐字元讀取。
3. 如果不是空格或換行，利用 `push_back()` 存入 `v`。
4. 如果遇到空格或換行：
   - 反向輸出 `v` 裡面的字元。
   - 使用 `cout << c` 輸出原本的分隔字元。
   - 使用 `v.clear()` 清空容器。
5. EOF 後，再反向輸出容器內剩下的字元。

### AC Code

```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    char c;
    vector<char> v;
    while (cin.get(c)) {
            if (c==' '||c=='\n') {
                for (int i = v.size()-1; i >= 0 ; i--)
                    cout << v[i];
                if (c == ' ' || c == '\n')cout << c;
                v.clear();
            }
            else
            {
                v.push_back(c);
            }
    }
    for (int i = v.size()-1; i >= 0 ; i--)
        cout << v[i];
}
```

### 程式執行流程

輸入：

```text
I love you
```

處理過程：

| 讀取內容 | Vector | 輸出 |
|---|---|---|
| I | I | |
| 空格 | I | I |
| love | love | |
| 空格 | love | evol |
| you | you | |
| EOF | you | uoy |

最終輸出：

```text
I evol uoy
```

## 4. 複雜度分析 (Complexity Analysis)

假設輸入共有 N 個字元，最長單字長度為 K。

- **Time Complexity：O(N)**
  - 每個字元讀取一次。
  - 每個單字反向輸出一次。
  - 總時間複雜度為 O(N)。

- **Space Complexity：O(K)**
  - `vector<char>` 只儲存目前的單字。
  - 額外空間取決於最長單字長度。

## 5. 易錯觀念 (Common Mistakes)

### 只判斷空格

```cpp
if(c == ' ')
```

問題：遇到換行時不會結束單字，導致不同列的單字連接。

正確：

```cpp
if(c == ' ' || c == '\n')
```

### 遇到換行直接輸出

```cpp
if(c == '\n')
    cout << '\n';
```

問題：沒有先反向輸出目前單字，也沒有清空容器。

### 把換行變成空格

```cpp
cout << " ";
```

問題：原本的換行格式會消失。

正確：

```cpp
cout << c;
```

### 忘記清空 Vector

```cpp
v.clear();
```

如果沒有清空，前一個單字的字元會殘留，影響下一個單字。

### 忘記處理 EOF

當最後一個單字沒有空格或換行結尾時，必須在 `while` 結束後再次反向輸出。

### 重複判斷

原始 AC 程式中的：

```cpp
if (c == ' ' || c == '\n') cout << c;
```

因為外層已經判斷過相同條件，所以可以簡化成：

```cpp
cout << c;
```

### size() 型別問題

`v.size()` 回傳 `size_t`，屬於無號整數。

較嚴謹的迴圈寫法：

```cpp
for(int i = (int)v.size()-1; i >= 0; i--)
    cout << v[i];
```

## 6. 邊界測資 (Edge Cases)

### Test 1：基本輸入

Input：

```text
I love you
```

Output：

```text
I evol uoy
```

### Test 2：多行輸入

Input：

```text
Hello World
Good Morning
```

Output：

```text
olleH dlroW
dooG gninroM
```

### Test 3：連續空格

Input：

```text
ab  cd
```

Output：

```text
ba  dc
```

### Test 4：最後沒有換行

Input：

```text
abc
```

Output：

```text
cba
```

### Test 5：單一字元

Input：

```text
A
```

Output：

```text
A
```

## 7. 其他解法 (Alternative Solutions)

除了 `vector<char>`，也可以使用 `string` 暫存單字，再利用 `reverse()` 反轉。

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    char c;
    string s;

    while(cin.get(c)) {
        if(c == ' ' || c == '\n') {
            reverse(s.begin(), s.end());
            cout << s << c;
            s.clear();
        }
        else {
            s += c;
        }
    }

    reverse(s.begin(), s.end());
    cout << s;
}
```

- **Time Complexity：O(N)**
- **Space Complexity：O(K)**

原本的 Vector 解法已經 AC，不需要更換。

## 8. 複習重點 (Review Questions)

1. `cin.get(c)` 與 `cin >> c` 有什麼不同？
2. 為什麼空格和換行都需要判斷？
3. 為什麼每次反向輸出後都需要 `v.clear()`？
4. `cout << c` 和 `cout << " "` 有什麼差別？
5. 為什麼 `while` 迴圈結束後還需要另一個 `for`？
6. `v.size()` 的回傳型別是什麼？
7. 為什麼時間複雜度是 O(N)？
8. 可以不使用 `vector<char>` 完成這題嗎？

**複習目標：**

不參考程式碼，獨立使用 `cin.get(c)` 與 `vector<char>` 完成 UVA 483，正確處理空格、換行以及 EOF。

## 9. 解題紀錄 (Submission Record)

- **Result**：AC
- **Language**：C++
- **Solved Date**：2026-10-15
- **Next Review**：2026-10-18
- **Data Structure**：vector<char>
- **Algorithm**：Simulation / String Processing
- **Time Complexity**：O(N)
- **Space Complexity**：O(K)

### Debugging History

1. 最初只處理空格，沒有處理換行。
2. 嘗試單獨處理換行，但沒有先反轉並清空 Vector。
3. 合併空格與換行判斷。
4. 發現固定輸出空格會破壞換行格式。
5. 改用 `cout << c` 保留原本的分隔字元。
6. 最終提交成功，獲得 AC。

### 核心記憶

**讀取字元 → 累積單字 → 遇到分隔字元 → 反向輸出 → 清空容器 → EOF 處理剩餘字元。**
