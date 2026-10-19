---
platform: LeetCode
id: 2089
title: Find Target Indices After Sorting Array
difficulty: 2
tags: Sorting, Array, Implementation
status: AC
solved: 2026-10-19
review_date: "-"
url: https://leetcode.com/problems/find-target-indices-after-sorting-array/
---

# LeetCode 2089 — Find Target Indices After Sorting Array

## 1. 題目摘要 (Problem Summary)

給定一個從索引 `0` 開始的整數陣列 `nums`，以及目標值 `target`。先將 `nums` **由小到大（非遞減）排序**，再找出排序後所有滿足 `nums[i] == target` 的索引 `i`。

- **輸入**：`vector<int> nums` 與整數 `target`（LeetCode 透過函式參數提供，不需自行讀取標準輸入）。
- **輸出**：`vector<int>`，包含排序後所有目標值所在的索引，依遞增順序排列；不存在則回傳空陣列 `[]`。
- **資料範圍**：`1 <= nums.size() <= 100`，`1 <= nums[i], target <= 100`。
- **重要條件**：題目要求的是**排序後的位置**，不是原始陣列中的索引；目標值可能重複出現。
- **官方難度**：Easy；**個人八級難度**：Lv.2 基礎（排序後線性掃描）。
- **時間與記憶體限制**：官方題目頁未提供可固定引用的數值，不自行假設。

官方範例：`nums = [1,2,5,2,3]`，`target = 2`；排序後為 `[1,2,2,3,5]`，答案是 `[1,2]`。

## 2. 核心觀念 (Key Concepts)

- **Sorting（排序）**：`sort(nums.begin(),nums.end())` 將陣列原地排序，使相同數字聚集在一起。
- **Array / Vector（動態陣列）**：`nums` 保存排序後資料，`vector<int> a` 收集符合條件的索引。
- **Linear Scan（線性掃描）**：使用一個迴圈由左至右檢查每個位置，判斷 `nums[i] == target`。
- **Zero-based Index（從零開始的索引）**：第一個元素的索引為 `0`，不是 `1`。
- **Output Order（輸出順序）**：因為 `i` 從小到大走訪，透過 `push_back(i)` 得到的答案天然就是遞增順序，無須再次排序。

**本題的關鍵規律**：排序之後，所有小於 `target` 的數字在前，所有等於 `target` 的數字連續出現。因此，目標索引形成一段連續區間；這個觀察也能推導出不需排序的解法。

## 3. 解題思路 (Approach)

### 觀察與推導

1. 題目要求的索引是**排序之後**的索引，所以不能直接掃描原陣列就回傳原位置。
2. 對 `nums` 做遞增排序，目標值相同的元素自然相鄰。
3. 依序檢查每個索引 `i`，遇到 `nums[i] == target` 就將 `i` 放入答案 `a`。
4. 掃描完畢後回傳 `a`；如果沒有任何元素相等，`a` 保持空陣列。

### 對照原始 AC Code

| 程式片段 | 實際作用 |
|---|---|
| `sort(nums.begin(),nums.end());` | 將 `nums` 由小到大原地排序。 |
| `vector<int>a;` | 建立空的結果陣列，儲存符合條件的**索引**。 |
| `for (int i =0;i<nums.size();i++)` | 從索引 `0` 掃描到 `nums.size()-1`。 |
| `if (nums[i]==target)` | 判斷目前的元素是否為目標值。 |
| `a.push_back(i);` | 記錄當前索引 `i`，不是存入 `nums[i]`。 |
| `return a;` | 回傳所有符合條件的排序後索引。 |

### 範例追蹤

`nums = [1,2,5,2,3]`，`target = 2`：

1. 排序：`[1,2,2,3,5]`。
2. `i=0`，`nums[0]=1`：不加入。
3. `i=1`，`nums[1]=2`：`a=[1]`。
4. `i=2`，`nums[2]=2`：`a=[1,2]`。
5. `i=3,4` 都不相等：答案維持 `[1,2]`。

### 原始 AC Code（保留原有邏輯、變數與排版）

```cpp
class Solution {
public:
   vector<int> targetIndices(vector<int>& nums, int target) {
       sort(nums.begin(),nums.end());
       vector<int>a;
       for (int i =0;i<nums.size();i++)
       {
           if (nums[i]==target)a.push_back(i);
       }
       return a;
   }
};
```

> 這是使用者提供的 LeetCode `class Solution` 程式碼，不是獨立的 `main()` 程式；原貼文中的 `\<` 屬於 Markdown 轉義，已還原為 C++ 的 `<`，並未更動演算法。`sort` 會修改傳入的 `nums`。

### 為什麼正確？

- **排序正確性**：`sort` 後的 `nums` 依非遞減順序排列，符合題目所要求的陣列順序。
- **掃描不變量**：每次處理索引 `i` 之前，`a` 恰好包含區間 `[0, i)` 中所有 `nums[j] == target` 的索引，而且按遞增順序排列。
- **維持不變量**：當 `nums[i] == target`，加入 `i`；否則不加入。因此處理完 `i` 後，不變量仍成立。
- **結束時**：所有索引都已被檢查，每個符合條件的位置都加入一次，不符合的都未加入；因此 `a` 正是題目要求的答案。若無符合者，正確回傳空陣列。

## 4. 複雜度分析 (Complexity Analysis)

設 `N = nums.size()`，`K = nums` 中等於 `target` 的元素數量，且 `0 <= K <= N`。

- **Time Complexity：`O(N log N)`**。
  - `sort(nums.begin(),nums.end())`：`O(N log N)`。
  - `for` 迴圈逐一檢查：`O(N)`；`push_back` 平均攤銷 `O(1)`，合計 `O(K)`。
  - 總時間 `O(N log N + N + K) = O(N log N)`。
- **Auxiliary Space Complexity（不計回傳答案）**：常見 C++ `std::sort` 實作使用約 `O(log N)` 的遞迴堆疊空間；排序本身不需要另一份長度為 `N` 的陣列。
- **包含結果陣列的額外空間**：`O(log N + K)`，最壞情況 `K=N`，所以為 `O(N)`。

> 因為本題 `N <= 100`，排序加掃描已經十分足夠，不需要為了效能而犧牲程式直觀性。

## 5. 易錯觀念 (Common Mistakes)

以下是本題**常見風險**，不是使用者曾經發生 WA 的紀錄。

1. **忘記排序**：`nums = [2,1,2]`、`target = 2`。原陣列中的索引為 `[0,2]`，但排序成 `[1,2,2]` 後，正解應為 `[1,2]`。
2. **將值當成索引**：`a.push_back(nums[i])` 會存入目標值；本題需要 `a.push_back(i)`。
3. **只找到第一個就停止**：目標值可能重複，必須記錄全部符合條件的位置。
4. **錯誤處理不存在的目標**：找不到時應回傳空 `vector<int>`，而不是 `[-1]`。
5. **索引從零開始**：例如排序後 `[2,2,3]`、`target = 2`，答案是 `[0,1]`，不是 `[1,2]`。
6. **修改原始陣列**：`sort` 會改變參數 `nums` 的內容；本題允許這樣解題，但若其他情境要求保留原順序，就要先複製陣列。
7. **型別警告**：`nums.size()` 是無號整數型別，原始程式用 `int i` 比較時可能有 signed/unsigned 編譯警告；本題長度最多 `100`，不影響此解法的正確性。原始 AC Code 保持不修改。

## 6. 邊界測資 (Edge Cases)

以下將 LeetCode 函式參數表示為輸入；實際判題不需讀入文字。

| 類型 | `nums` | `target` | 預期回傳 | 說明 |
|---|---|---:|---|---|
| 官方範例 1 | `[1,2,5,2,3]` | 2 | `[1,2]` | 目標出現兩次。 |
| 官方範例 2 | `[1,2,5,2,3]` | 3 | `[3]` | 目標出現一次。 |
| 官方範例 3 | `[1,2,5,2,3]` | 5 | `[4]` | 目標在排序後最後一格。 |
| 目標不存在 | `[1,2,5,2,3]` | 4 | `[]` | 結果為空。 |
| 最短輸入且符合 | `[1]` | 1 | `[0]` | 索引從零開始。 |
| 最短輸入且不符合 | `[1]` | 2 | `[]` | 不應越界。 |
| 所有元素相等 | `[2,2,2,2]` | 2 | `[0,1,2,3]` | 所有位置都要輸出。 |
| 值域上界 | `[100,1,100,2]` | 100 | `[2,3]` | 排序後為 `[1,2,100,100]`。 |

## 7. 其他解法 (Alternative Solutions)

### 方法：Counting（計數，不必排序）

排序後所有小於 `target` 的元素一定在前面，而與 `target` 相等的元素形成連續區間。因此只需要計算：

- `smaller`：原陣列中 **小於 `target`** 的元素數量。
- `equal`：原陣列中 **等於 `target`** 的元素數量。

答案恰好是 `smaller, smaller+1, ..., smaller+equal-1`；當 `equal=0` 時答案為空。

```cpp
// 替代寫法：不是本次原始 AC 提交版本
class Solution {
public:
    vector<int> targetIndices(vector<int>& nums, int target) {
        int smaller = 0, equal = 0;
        for (int x : nums) {
            if (x < target) ++smaller;
            else if (x == target) ++equal;
        }
        vector<int> ans;
        for (int i = 0; i < equal; ++i) {
            ans.push_back(smaller + i);
        }
        return ans;
    }
};
```

- **時間複雜度**：`O(N + K) = O(N)`，不需要 `sort`。
- **額外空間**：不計回傳結果為 `O(1)`；包含結果為 `O(K)`。
- **與原始 AC Code 的差異**：原始解法先排序再掃描，較直觀，但會修改 `nums`；計數解法不修改 `nums`，效率更高，也更直接利用目標值在排序後形成連續區間的性質。

## 8. 複習重點 (Review Questions)

1. 為什麼本題必須考慮「排序後」的索引，而不是原陣列的索引？
2. 為什麼原始程式不必另外排序 `a`，回傳結果卻一定是遞增的？
3. 當 `target` 不存在或全部元素都等於 `target` 時，原始程式各會回傳什麼？
4. 如何利用「小於目標值的數量」與「等於目標值的數量」，在不排序的情況下算出答案？
5. 原始解法的排序時間、掃描時間與輸出空間應如何分開分析？
6. 能否不看程式碼，重新寫出「排序 + 掃描」及「計數」兩種解法，並解釋各自的適用情境？

## 9. 解題紀錄 (Submission Record)

- **Result**：Accepted (AC)（依使用者提供）
- **Platform / ID**：LeetCode 2089
- **Language**：C++
- **Solved**：2026-10-19
- **Next Review**：2026-10-25
- **Difficulty**：Lv.2 基礎
- **Solution**：`solution.cpp`（索引器要求與 `remind.md` 位於同一題目資料夾）
