---
platform: UVA
id: 11727
title: Cost Cutting
difficulty: 2
tags: Sorting, Array, Implementation
status: AC
solved: 2026-10-14
review_date: "-"
url: https://onlinejudge.org/external/117/11727.pdf
---


# UVA 11727 — Cost Cutting

## 1. 題目摘要
給定三位員工的薪水，找出排序後位於中間的薪水。

每筆測試資料的輸出格式為：
Case X: Answer

## 2. 核心觀念
- Sorting：排序
- Vector：儲存三筆薪水
- Median：中位數
- sort()：C++ STL 排序函式

## 3. 解題思路
1. 讀入測試資料數量 T。
2. 每筆測資讀入三個整數。
3. 使用 sort() 由小到大排序。
4. 取出索引 1 的元素作為答案。
5. 按照 Case i: answer 格式輸出。

## 4. 複雜度分析
- Time Complexity: O(1) 每筆測資
- Total Time Complexity: O(T)
- Space Complexity: O(1)

每次只排序固定三個數字，
因此單筆測資所需時間與空間皆為常數。

## 5. 易錯觀念
- 題目要求中位數，不是平均數。
- 排序後中間元素的索引是 1，不是 2。
- Case 編號從 1 開始。
- 輸出格式必須完全符合題目要求。

## 6. 複習重點
- sort() 的使用方式
- vector 的索引從 0 開始
- 中位數與平均數的差別
- 為什麼本題排序仍然是 O(1)？
- 如果改成 N 個數字，複雜度會如何改變？

## 7. 解題紀錄
- Result: Accepted (AC)
- Language: C++
- Solved: 2026-10-14
- Next Review: 2026-10-17
