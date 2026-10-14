---
platform: UVA
id: 10038
title: Jolly Jumpers
difficulty: Basic
tags: Array, Math, Simulation
status: AC
solved: 2026-10-14
review_date: 2026-10-21
url: https://onlinejudge.org/external/100/10038.pdf
---

# UVA 10038 — Jolly Jumpers（僅為示範，不計入統計）

## 1. 題目一句話摘要
對長度 N 的數列求相鄰差的絕對值；如果正好收齊 1..N−1，就稱為 Jolly。

## 2. 關鍵觀察 / 解題思路
差值共有 N−1 個。如果每個差值介於 1..N−1 且**沒有重複**，就必然每種差值各出現一次。用 `seen[diff]` 記錄出現過的差值。

## 3. 時間與空間複雜度
- Time: `O(N)`
- Space: `O(N)`

## 4. 曾經犯的錯 / WA、TLE、RE 原因
- 範圍判斷 `diff < 1 || diff >= N`，`||` 不可誤寫成 `&&`。
- 不要用雙層迴圈暴力比對重複差值；用布林陣列更簡潔。
- `n = 1` 時沒有差值，仍然是 Jolly。

## 5. 邊界測資
- `1 100` → `Jolly`
- `4 1 4 2 3` → `Jolly`
- `4 1 4 2 2` → `Not jolly`

## 6. 下次複習時的自我測驗
- [ ] 為什麼不需要排序？
- [ ] 如何避免陣列越界？
- [ ] N−1 個差值且全部不同，為什麼代表 1..N−1 都出現？

## 7. 延伸 / 其他解法
可以用 set，但空間仍 O(N)，且平衡樹插入需 O(log N)。
