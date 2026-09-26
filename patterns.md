# LeetCode patterns

Not solutions. When you see X, reach for Y. After each problem, add one line under the pattern it actually used. If a problem is just a twist, hang it on an existing pattern. New heading only when the move is new.

How to read an entry: **when** (the tell) → **move** (what you do) → **problems** (the one insight each taught).

---

## Character-closed intervals → greedy earliest-end

**When:** substrings must include all occurrences of every char they contain; you want the max number of non-overlapping such pieces (min total length on ties).

**Move:** for each letter take `[first, last]`, expand until closed under other letters’ ranges; keep only intervals that start at their own letter’s first index (≤26). They nest or are disjoint. Sort by end; greedily take non-overlapping. Nesting ⇒ max count also min total length.

- **1520** Maximum Number of Non-Overlapping Substrings: ≤26 closed intervals; sort by end + greedy pick.

---

## Sort + cluster by gap

**When:** you may swap, merge, or connect values if `|a - b| <= limit` (or any threshold). You want to rearrange inside groups, not across them.

**Move:** sort the values. A new cluster starts when consecutive sorted values differ by more than `limit`. Within a cluster, values can move to any of that cluster's original indices. Assign greedily there (usually zip sorted values onto sorted indices).

You do not build a graph. Sorting turns connected components into contiguous slices.

- **2948** Make Lexicographically Smallest Array by Swapping Elements: lex smallest means smallest values on the leftmost slots of each cluster.

---

## Cover two positions from the ends

**When:** you can only take/delete from the front or the back, and you must cover two special indices (min and max, or two targets).

**Move:** `min` of three: both from the left, both from the right, one from each. Deleting through index `i` from the front costs `i + 1`. Leftmost/rightmost of the two positions, not "index of the min value".

- **2091** Removing Minimum and Maximum From Array: `min(b+1, n-a, a+1+n-b)` after `a, b = sorted((i_min, i_max))`.

---

---

## Two pointers from both ends

**When:** a pair's score is `f(width, min(left, right))` (or similar), brute force is all pairs, and shrinking the window is the only way left to improve.

**Move:** start at `i = 0`, `j = n-1`. Keep a running best. Always advance the pointer at the shorter line. That index is done: any inner partner gives smaller width and height at most what you already used, so those pairs lose without being enumerated. Area is not monotonic; the proof is "this pointer is dead," not "this step must get bigger."

- **11** Container With Most Water: area `(j-i)*min(h[i], h[j])`. Kill the shorter end.

---
## Enumerate under tiny n

**When:** `n` is tiny (≤10–15) and you need distinct objects under simple position/digit rules (leading zeros, parity, etc.).

**Move:** generate candidates (permutations or nested loops over the multiset), filter the constraints, put survivors in a set. Reach for digit DP only when `n` is large.

- **3483** Unique 3-Digit Even Numbers: no leading zero + even units; distinctness is a set of the formed values (n≤10, so generate-and-filter beats digit DP).

---

## Weighted intervals, pick ≤k

**When:** pick up to a tiny `k` non-overlapping weighted intervals (`n` large), often with a lex-smallest index tie-break. Boundary-touch usually counts as overlap.

**Move:** sort by end. Binary-search the previous interval with `end < start`. DP `take[i][t]` / prefix-best for `t = 1..k`, keeping `(score, sorted index tuple)` and preferring higher score then lex-smaller indices.

- **3414** Maximum Score of Non-overlapping Intervals: `k≤4` + lex-smallest indices; shared endpoint = overlap.

---


## Count votes for a relative transform

**When:** you need the best alignment of two sparse point sets (or binary grids) under a pure translation (no rotation), and n is small enough to pair points.

**Move:** list the 1-coordinates in each image. Every pair (p1, p2) votes for vector p1−p2. Answer = max vote count (0 if either set is empty).

- **835** Image Overlap: max overlap after translating one binary matrix onto the other; vector votes replace O(n⁴) shift loops.

---

---

## Axis-aligned box overlap (strict)

**When:** two axis-aligned rectangles (AABB); you need whether they overlap with positive area (not just share an edge or corner).

**Move:** check both projections with strict inequalities: `rec1[0] < rec2[2] and rec2[0] < rec1[2] and rec1[1] < rec2[3] and rec2[1] < rec1[3]`.

- **836** Rectangle Overlap: positive-area overlap iff both x and y projections intersect with strict inequalities (edge/corner touch is false).

---

## Greedy earliest palindrome of length k or k+1

**When:** max *count* of non-overlapping palindromic substrings each of length ≥ k (n up to ~2e3).

**Move:** any palindrome longer than k contains a palindrome of length k or k+1, so only those lengths matter. Scan left→right; at each index try length k then k+1; on a hit, take it and jump past its end (earliest-end greedy for max count).

- **2472** Maximum Number of Non-overlapping Palindrome Substrings: only need len k / k+1; greedy take earliest and jump.

---

---

## Combinatorial map: segments → C(n+k-1, 2k)

**When:** count ways to place exactly `k` non-overlapping objects of length ≥1 on `n` discrete points (sharing endpoints OK), answer modulo `10^9+7`; `n≤1000`.

**Move:** each segment uses ≥1 unit of length; sharing endpoints is free. A stars-and-bars / endpoint transform reduces the count to `C(n+k-1, 2k)`. Compute with modular inverse (or factorials) — no DP table once the identity is known.

- **1621** Number of Sets of K Non-Overlapping Line Segments: answer is `C(n+k-1, 2k) mod 10^9+7`.


## Sliding window + prefix-min pairing

**When:** you need two (or a few) non-overlapping subarrays with a sum constraint, and `arr[i] >= 1` so each end has at most one matching start.

**Move:** sliding window finds the unique target-sum window ending at each `r`. Keep `prefix[i]` = min window length ending strictly before `i`. For each window ending at `r` with start `s`, try `best[r] + prefix[s]`. Answer is the min, or -1.

- **1477** Find Two Non-overlapping Sub-arrays Each With Target Sum: positives give unique target window per end; pair each with the best fully-left via prefix-min.

---

## Pattern map (fill as we go)

sliding window · binary search on answer · prefix sums · hashing / two-sum family · heap / k-best · monotonic stack/queue · intervals · greedy (other) · DSU · BFS/DFS · topo · tree / LCA · linked list · binary search on index · DP 1D · DP knapsack · DP interval / partition · DP on trees · bitmask · math / gcd · string / KMP / trie · geometry

One problem can sit on two patterns. Put it where the *bottleneck insight* was.

## Subarray product mod k (tiny modulus)

**When:** you must count (or classify) contiguous subarrays by their product modulo a tiny `k` (often ≤5–10), and n is too large for O(n²).

**Move:** ending-at-i DP over remainders. For each new `a_i`, start a singleton `a_i % k`, and extend every previous ending remainder `r` to `(r * a_i) % k`. Accumulate into `result[0..k-1]`. O(n·k).

- **3524** Find X Value of Array I: count subarrays by product % k; extend ending remainder counts by ×(a_i % k).

## Segment tree: product + prefix remainder counts (tiny k)

**When:** point updates plus queries that ask how many prefixes of a suffix `[start..]` have product ≡ x (mod k), and k is tiny (≤5–10) while n,q are large.

**Move:** each segment stores `(prod mod k, pref[0..k-1])` — counts of prefixes of that segment by product remainder. Merge: copy left prefs; for each right rem r, add count into `(left.prod * r) % k`. Point-update leaf; query the folded merge of `[start, n-1]`.

- **3525** Find X Value of Array II: after persistent update, x-value = #prefixes of nums[start:] with product % k == x.


---

## Sliding window: longest middle = total−x (complement of prefix+suffix)

**When:** you may only remove from both ends, and you want the fewest removals whose values sum to exactly `x`.

**Move:** flip the question. Keeping a contiguous middle with sum `total − x` maximizes what you keep, so min ops = `n −` that length. One sliding window finds the longest such middle (`target < 0` → −1; `target == 0` → `n`).

- **1658** Minimum Operations to Reduce X to Zero — min prefix+suffix sum-to-x = n − longest middle sum-(total−x); sliding window.


## Digit-sum of value vs index

**When:** you need the (smallest) index where a digit aggregate of `nums[i]` equals `i` (or another index-tied digit property), and `n` / value range are tiny.

**Move:** left-to-right linear scan; compute digit sum with `%10`/`//10` (or `sum(map(int, str(v)))`); return first hit, else `-1`.

- **3550** Smallest Index With Digit Sum Equal to Index: first `i` with digit_sum(nums[i])==i.

## Recursive descent: brace union vs adjacent cartesian product

**When:** an expression grammar mixes `{...}` unions (comma) with adjacent concatenation (cartesian product of string sets), and you need the sorted unique words.

**Move:** recursive descent over sets of strings. Maintain a current product accumulator (start `{{""}}`). On `{`, recurse for the inner union; on `,`, push the current product into the union list and reset; on a letter, cartesian-concat that singleton; on `}`, union all parts and return. Top-level is the same parse. Sort the final set.

- **1096** Brace Expansion II: `,` = union inside braces; adjacency = cartesian concat of word sets; return sorted unique.


## Hash map + single scan (keyed substitution)

**When:** a string has non-nested `(key)` tokens to replace from a known key→value table (unknown → placeholder).

**Move:** build a dict from the knowledge pairs. Scan once; on `(`, take characters until `)`, append `map.get(key, '?')`, continue after `)`. Plain letters pass through. No nesting ⇒ one pass is enough.

- **1807** Evaluate the Bracket Pairs of a String: each knowledge key unique; unknown keys become `?`; O(n+m).
