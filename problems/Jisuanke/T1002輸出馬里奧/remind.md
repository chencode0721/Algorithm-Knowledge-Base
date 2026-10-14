
---
platform: Jisuanke
id: T1002
title: 輸出馬里奧
difficulty: 1
tags: Basic I/O, Implementation, ASCII Art
status: AC
solved: 2026-10-14
review_date: 2026-10-17
url: https://www.jisuanke.com/problem/T1002
---

# T1002 — 輸出馬里奧

## 1. 題目摘要
按照題目提供的樣例輸出馬里奧圖案。

不需要讀取任何輸入資料。

## 2. 核心觀念
- cout：標準輸出
- endl：輸出換行並刷新緩衝區
- String Literal：字串常值
- ASCII Art：使用文字與符號組成圖案
- Output Formatting：輸出格式控制

## 3. 解題思路
1. 觀察題目要求的馬里奧圖案。
2. 確認每一行的空格與特殊符號。
3. 使用 cout 輸出每一行。
4. 使用 endl 換行。
5. 確保輸出內容與題目要求一致。

## 4. 複雜度分析
- Time Complexity: O(1)
- Space Complexity: O(1)

原因：
輸出固定行數與固定數量的字元，
不隨輸入規模改變。

## 5. 易錯觀念
- 行首空格不能隨意省略。
- 注意 *、#、. 的數量與位置。
- 每行都要正確換行。
- 不要輸出題目沒有要求的提示文字。
- 最後一行不一定需要額外換行。

## 6. 複習重點
- cout 如何輸出字串？
- endl 與 \n 有什麼差別？
- 為什麼本題是 O(1)？
- 如何避免複製 ASCII 圖案時發生格式錯誤？

## 7. 解題紀錄
- Result: Accepted (AC)
- Language: C++
- Solved: 2026-10-14
- Next Review: 2026-10-17
