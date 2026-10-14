
---
platform: Jisuanke
id: T5461
title: 人口普查
difficulty: 3
tags: Array, String, Frequency Counting, Implementation
status: AC
solved: 2026-10-14
review_date: 2026-10-17
url: https://www.jisuanke.com/problem/T5461
---

# T5461 — 人口普查

## 1. 題目摘要 (Problem Summary)

給定 n 位國民的名字首字母，全部為 a～z。

統計每個字母出現的次數。

如果某個字母的出現次數嚴格大於 m，
就按照字母順序輸出該字母，每行一個。

限制：
- 1 ≤ n ≤ 100000
- 1 ≤ m ≤ n

## 2. 核心觀念 (Key Concepts)

- Array：陣列
- String：字串
- Frequency Counting：頻率統計
- Character Indexing：字元索引轉換
- ASCII：字元編碼

## 3. 解題思路 (Approach)

1. 建立大小為 26 的整數陣列 A，全部初始化為 0。
2. 讀入 n、m 和字串 s。
3. 遍歷字串，統計每個字母出現的次數。
4. 從索引 0 遍歷到 25。
5. 若 A[i] > m，輸出對應的小寫字母。

### 關鍵程式碼

```cpp
A[s[i]-'a'] += 1;
```

因為字母依順序排列：

- 'a' - 'a' = 0
- 'b' - 'a' = 1
- 'c' - 'a' = 2
- ...
- 'z' - 'a' = 25

因此可以直接將字母轉換為陣列索引。

### 索引轉回字母

```cpp
char(i + 97)
```

在 ASCII 中，小寫字母 'a' 的編碼是 97。

也可以使用更容易閱讀的：

```cpp
char('a' + i)
```

## 4. 複雜度分析 (Complexity Analysis)

- Time Complexity: O(n + 26) = O(n)
- Space Complexity: O(n + 26) = O(n)

原因：

第一個迴圈遍歷 n 個字元，需要 O(n)。

第二個迴圈固定遍歷 26 個字母，需要 O(26)。

計數陣列固定 26 個元素，為 O(1) 額外空間。

但程式還儲存長度為 n 的字串，因此整體空間為 O(n)。

## 5. 易錯觀念 (Common Mistakes)

- 題目要求嚴格大於 m，必須使用 >，不能使用 >=。
- 陣列 A 必須初始化為 0。
- 字元 'a' 對應索引 0，而不是 1。
- 題目要求按照字母順序輸出。
- 不需要使用 sort()，因為直接遍歷 0～25 就已經是字母順序。

## 6. 邊界測資 (Edge Cases)

- 某個字母剛好出現 m 次，不應輸出。
- 所有字母都沒有超過 m。
- 字串全部由相同字母組成。
- n 達到 100000 的最大限制。

## 7. 其他解法 (Alternative Solutions)

可以使用 map<char, int> 或 unordered_map<char, int>
統計每個字母的出現次數。

但由於題目只有 26 個小寫英文字母，
使用固定陣列更簡單，額外空間也更小。

## 8. 複習重點 (Review Questions)

- 為什麼 s[i] - 'a' 可以轉成陣列索引？
- 為什麼不需要 sort()？
- char(i + 97) 與 char('a' + i) 有什麼差別？
- O(n + 26) 為什麼可以化簡成 O(n)？
- 使用 map 和陣列計數有什麼差別？

## 9. 解題紀錄 (Submission Record)

- Result: Accepted (AC)
- Language: C++
- Solved: 2026-10-14
- Next Review: 2026-10-17
