---
platform: Jisuanke
id: T1079
title: 開關燈
difficulty: 2
tags: Array, Simulation, Implementation
status: AC
solved: 2026-10-15
review_date: 2026-10-22
url: https://www.jisuanke.com/problem/T1079
---

# T1079 — 開關燈

## 1. 題目摘要 (Problem Summary)

一共有 N 盞燈，起初全部亮著。

依序有 M 個人操作燈泡：
- 第 i 個人會反轉編號為 i 的倍數的所有燈。
- 亮燈變暗，暗燈變亮。
- 最後輸出所有熄滅的燈泡編號，以逗號分隔。

## 2. 核心觀念 (Key Concepts)

- **Array / Vector**：使用 `vector<int> a(N, 1)`，初始值 1 代表亮燈。
- **Simulation**：按照每個人的操作順序模擬。
- **倍數判斷**：`(j+1)%i==0` 代表燈泡編號是 i 的倍數。
- **狀態反轉**：`a[j]*=-1`，讓 1 與 -1 互相轉換。
- **索引轉換**：陣列索引從 0 開始，燈泡編號從 1 開始。

## 3. 解題思路 (Approach)

1. 建立長度為 N 的 vector，全部初始化為 1。
2. 外層迴圈 i 從 1 到 M，代表每個人。
3. 內層迴圈 j 從 0 到 N-1，代表每盞燈。
4. 如果 `(j+1)%i==0`，執行 `a[j]*=-1`。
5. 操作完成後，將 a[i] 等於 -1 的燈泡編號 i+1 存入 b。
6. 輸出 b，最後一個元素不加逗號。

例如 N=10、M=3：

初始：全部亮燈。

第 1 人：關閉全部燈。

第 2 人：反轉 2、4、6、8、10。

第 3 人：反轉 3、6、9。

最後關閉：
`1,5,6,7`

## 4. 複雜度分析 (Complexity Analysis)

- **Time Complexity：O(NM)**
  - 外層迴圈執行 M 次。
  - 內層迴圈執行 N 次。
  - 總共約 N×M 次判斷。

- **Space Complexity：O(N)**
  - a 儲存 N 盞燈的狀態。
  - b 最多儲存 N 個燈泡編號。

## 5. 易錯觀念 (Common Mistakes)

### ① Vector 初始化

錯誤：
`vector<int> a(N) = {1};`

正確：
`vector<int> a(N, 1);`

代表建立 N 個元素，全部初始化為 1。

### ② 陣列索引與燈泡編號

- `a[0]` 代表第 1 號燈。
- `a[1]` 代表第 2 號燈。
- `a[N-1]` 代表第 N 號燈。

因此必須使用 `(j+1)%i==0` 判斷倍數。

### ③ push_back 存入錯誤資料

錯誤：
`b.push_back(a[i]);`

這樣存入的是燈泡狀態 -1。

正確：
`b.push_back(i+1);`

這樣才是燈泡編號。

### ④ Vector 最後一個元素

錯誤：
`b[b.size()]`

正確：
`b[b.size()-1]`

因為 vector 索引從 0 開始。

### ⑤ size()-1 的風險

當 vector 為空時，`b.size()-1` 會發生無號整數下溢。

本題 N>=1 且 M>=1 時，第 1 號燈一定會關閉，因此 b 不為空。

更通用的輸出方式：

`for (int i=0; i<b.size(); i++) { if(i) cout << ","; cout << b[i]; }`

## 6. 邊界測資 (Edge Cases)

### 測資 1
Input:
`1 1`

Output:
`1`

### 測資 2
Input:
`10 3`

Output:
`1,5,6,7`

### 測資 3
Input:
`5 1`

Output:
`1,2,3,4,5`

### 測資 4
Input:
`10 10`

Output:
`1,4,9`

## 7. 其他解法 (Alternative Solutions)

### 方法一：倍數跳躍（類似埃氏篩）

原本每個人都檢查全部燈泡。

可以直接跳到 i 的倍數：

```cpp
for (int i=1; i<=M; i++)
{
    for (int j=i; j<=N; j+=i)
    {
        a[j-1]*=-1;
    }
}
```

時間複雜度：
`O(N log(M+1))`

空間複雜度：
`O(N)`

### 方法二：因數數量

第 k 號燈被反轉的次數，等於 k 在 1 到 M 之間的正因數數量。

- 奇數次反轉：最後關閉。
- 偶數次反轉：最後開啟。

當 M=N 時，只有完全平方數擁有奇數個正因數。

例如：
`1,4,9,16,25,36...`

注意：當 M<N 時，不能直接套用完全平方數規則。

## 8. 複習重點 (Review Questions)

1. `vector<int> a(N,1)` 的 N 和 1 分別代表什麼？
2. 為什麼使用 `(j+1)%i==0`？
3. `a[j]*=-1` 如何實現燈泡反轉？
4. `push_back(a[i])` 與 `push_back(i+1)` 有什麼差別？
5. 為什麼最後一個元素是 `b[b.size()-1]`？
6. 如何避免輸出最後一個多餘的逗號？
7. 如何使用 `j+=i` 優化時間複雜度？
8. 為什麼完全平方數的正因數個數是奇數？

## 9. 解題紀錄 (Submission Record)

- Result：AC
- Language：C++
- Solved：2026-10-15
- Next Review：2026-10-22
- Solution：solution.cpp
