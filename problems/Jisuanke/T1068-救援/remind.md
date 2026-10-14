---
platform: Jisuanke
id: T5461
title: 救援
difficulty: 2
tags: Math, Geometry, Simulation, Implementation
status: AC
solved: 2026-10-14
review_date: 2026-10-17
url: "-"
---
# T5461 — 救援 (Rescue)
## 1. 題目摘要 (Problem Summary)

從原點 `(0, 0)` 的大本營派出救生船，依序前往 `n` 個屋頂救援。每次都從大本營出發，接到該屋頂的全部人員後沿原路返回大本營。

- 屋頂座標為 `(x, y)`，船速為每分鐘 `50` 公尺。
- 每人上船需 `1` 分鐘，每人下船需 `0.5` 分鐘。
- 輸入：屋頂數 `n`，接著每行為 `x y r`（`r` 是人數）。
- 輸出：全部救援所需的總分鐘數，**向上取整**。

## 2. 核心觀念 (Key Concepts)

- **Euclidean Distance（歐幾里得距離）**：由畢氏定理得 `distance = sqrt(x*x + y*y)`。
- **Round Trip（往返路程）**：每次要去屋頂再回原點，故距離為 `2 * distance`。
- **Time = Distance / Speed**：船速 `50` 公尺／分鐘，航行時間為 `2 * distance / 50`。
- **Accumulation（累加）**：每個屋頂的救援時間彼此相加。
- **Ceiling（向上取整）**：答案應使用 `ceil(total)`；原 AC 程式使用整數轉型及判斷小數部分實現。

## 3. 解題思路 (Approach)

1. 設 `m = 0` 為總航行距離，`uptime = 0` 為總上船時間，`downtime = 0` 為總下船時間。
2. 讀入每個屋頂的座標 `(x, y)`，以 `sqrt(x*x + y*y)` 求原點到屋頂的直線距離。
3. 因為每次救援都需要往返，將該距離乘以 `2`，加到 `m`。
4. 讀入人數 `r`：`uptime += r`；`downtime += 0.5 * r`。
5. 全部讀完後，航行時間 `mtime = m / 50`。
6. 計算 `total = mtime + uptime + downtime`，向上取整輸出。

也可以直接寫成：

$$
T = \left\lceil \sum_{i=1}^{n}
\left(\frac{2\sqrt{x_i^2+y_i^2}}{50}+1.5r_i\right)
\right\rceil
$$

**範例**：`(30, 40)` 距離為 `50` 公尺，3 人上、下船合計 `4.5` 分鐘，航行 `2` 分鐘，總共 `6.5` 分鐘，向上取整為 `7`。

## 4. 複雜度分析 (Complexity Analysis)

- Time Complexity：**O(n)**。每個屋頂只處理一次，每次計算與加總皆為常數時間。
- Space Complexity：**O(1)**。只使用固定數量的變數，不儲存全部屋頂。

## 5. 易錯觀念 (Common Mistakes)

- **忘記回程**：求出的原點距離必須乘以 `2`。
- **把上下船時間算錯**：每人共需 `1 + 0.5 = 1.5` 分鐘，不是全船只花 `1.5` 分鐘。
- **把最後答案四捨五入**：題目要求向上取整（`ceil`），例如 `6.5 → 7`。
- **太早轉為 `int`**：應先累加完整的浮點數總時間，再統一向上取整。
- **使用 `double n`**：原 AC 程式可以在整數輸入下運作，但屋頂數本質上是整數，改用 `int n` 更清楚。
- **浮點精度**：原程式的「和整數部分比較」方式已 AC，但一般建議使用 `ceil(total)` 表達意圖；在非常接近整數時仍需留意浮點誤差。

## 6. 邊界測資 (Edge Cases)

**題目範例**
```text
輸入：
1
30 40 3

輸出：
7
```

**剛好整數分鐘**
```text
輸入：
1
30 40 2

輸出：
5
```

**多屋頂累加**
```text
輸入：
2
30 40 1
30 40 1

輸出：
7
```

## 7. 其他解法 (Alternative Solutions)

不必將航行、上船、下船時間分成三個變數；可以在每次迴圈中直接累加：

```cpp
int n;
cin >> n;
double total = 0;
for (int i = 0; i < n; ++i) {
    double x, y;
    int r;
    cin >> x >> y >> r;
    total += 2.0 * hypot(x, y) / 50.0 + 1.5 * r;
}
cout << (int)ceil(total) << '\n';
```

`hypot(x, y)` 會計算 `sqrt(x*x + y*y)`；這個寫法比較簡潔。時間 O(n)、空間 O(1)。

## 8. 複習重點 (Review Questions)

**2026-10-17 複習時先不要看原始程式，嘗試回答：**

1. 為什麼距離要乘上 `2`？什麼情況下不能乘 `2`？
2. 為什麼每個屋頂人數 `r` 對應的時間是 `1.5 * r`？
3. `ceil(6.0)` 與 `ceil(6.1)` 分別是多少？為什麼不可使用 `round()`？
4. 能否在只使用 O(1) 額外空間的情況下，一次讀取就算出答案？

**練習目標**：10 分鐘內不看解答，重寫 C++ 程式並通過範例與邊界測資。

## 9. 解題紀錄 (Submission Record)

- Result：AC
- Language：C++
- Solved：2026-10-14
- Next Review：2026-10-17
- Note：保留原本的距離累加、上下船時間累加與自行向上取整的解題邏輯；已通過題目測試。
