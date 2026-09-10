#!/usr/bin/env python3
"""Generate dark-theme matplotlib PNGs for LeetCode explainers."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

OUT = Path(__file__).resolve().parent / "docs" / "leetcode" / "assets"
OUT.mkdir(parents=True, exist_ok=True)

BG = "#0f1115"
PANEL = "#171a21"
TEXT = "#e8eaed"
MUTED = "#9aa0a6"
ACCENT = "#7aa2ff"
ACCENT2 = "#5bd6a2"
BORDER = "#2a2f3a"
WARN = "#ffb86b"
CRIT = "#ff6b8a"


def style_ax(ax, title=None):
    ax.set_facecolor(BG)
    for spine in ax.spines.values():
        spine.set_color(BORDER)
    ax.tick_params(colors=MUTED)
    ax.xaxis.label.set_color(TEXT)
    ax.yaxis.label.set_color(TEXT)
    if title:
        ax.set_title(title, color=TEXT, fontsize=13, pad=10)


def save(fig, name: str):
    fig.patch.set_facecolor(BG)
    path = OUT / name
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=BG, edgecolor="none")
    plt.close(fig)
    size = path.stat().st_size
    print(f"wrote {path.name} ({size} bytes)")
    return size


# ── 115 DP heatmap ──────────────────────────────────────────────────────────
def plot_115():
    s, t = "rabbbit", "rabbit"
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = 1
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i - 1][j]
            if s[i - 1] == t[j - 1]:
                dp[i][j] += dp[i - 1][j - 1]
    arr = np.array(dp, dtype=float)

    fig, ax = plt.subplots(figsize=(8, 7))
    cmap = LinearSegmentedColormap.from_list(
        "darkblue", ["#0f1115", "#1a2744", "#2d4a8a", ACCENT]
    )
    im = ax.imshow(arr, cmap=cmap, aspect="equal")
    for i in range(m + 1):
        for j in range(n + 1):
            val = int(arr[i, j])
            color = TEXT if val > arr.max() * 0.45 else MUTED
            ax.text(j, i, str(val), ha="center", va="center", color=color, fontsize=11)

    ax.set_xticks(range(n + 1))
    ax.set_yticks(range(m + 1))
    ax.set_xticklabels([""] + list(t), color=ACCENT2, fontsize=12)
    ax.set_yticklabels([""] + list(s), color=ACCENT2, fontsize=12)
    ax.set_xlabel("t (cols)", color=MUTED)
    ax.set_ylabel("s (rows)", color=MUTED)
    style_ax(ax, f"115 · DP heatmap  s='{s}'  t='{t}'  → {dp[m][n]}")
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.yaxis.set_tick_params(color=MUTED)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color=MUTED)
    save(fig, "115_dp_heatmap.png")


# ── 940 ends[] bars evolving ────────────────────────────────────────────────
def plot_940():
    s = "aba"
    ends_hist = []
    ends = [0] * 26
    for ch in s:
        i = ord(ch) - ord("a")
        ends[i] = sum(ends) + 1
        # snapshot letters that appear
        ends_hist.append((ch, ends.copy()))

    letters = sorted({ch for ch in s})
    idxs = [ord(c) - ord("a") for c in letters]
    n_steps = len(ends_hist)

    fig, axes = plt.subplots(1, n_steps, figsize=(3.2 * n_steps, 4), sharey=True)
    if n_steps == 1:
        axes = [axes]
    for step, (ax, (ch, ends_snap)) in enumerate(zip(axes, ends_hist)):
        vals = [ends_snap[i] for i in idxs]
        colors = [ACCENT2 if letters[k] == ch else ACCENT for k in range(len(letters))]
        bars = ax.bar(letters, vals, color=colors, edgecolor=BORDER, width=0.65)
        for b, v in zip(bars, vals):
            ax.text(
                b.get_x() + b.get_width() / 2,
                v + 0.15,
                str(v),
                ha="center",
                va="bottom",
                color=TEXT,
                fontsize=11,
            )
        style_ax(ax, f"after '{ch}'  Σ={sum(ends_snap)}")
        ax.set_ylim(0, max(8, max(vals) + 2))
        ax.set_xlabel("ends[c]", color=MUTED)
        if step == 0:
            ax.set_ylabel("count", color=MUTED)
    fig.suptitle(f"940 · ends[] evolving for s='{s}'  → {sum(ends)}", color=TEXT, fontsize=13)
    fig.tight_layout()
    save(fig, "940_ends_bars.png")


# ── 2058 critical points ────────────────────────────────────────────────────
def plot_2058():
    arr = [3, 1, 2, 2, 3, 2, 2, 1, 4]
    # critical indices (1-based in problem for linked list; here 0-based array indices)
    crit = []
    for i in range(1, len(arr) - 1):
        if (arr[i] > arr[i - 1] and arr[i] > arr[i + 1]) or (
            arr[i] < arr[i - 1] and arr[i] < arr[i + 1]
        ):
            crit.append(i)
    min_d = min(crit[j + 1] - crit[j] for j in range(len(crit) - 1)) if len(crit) >= 2 else -1
    max_d = crit[-1] - crit[0] if len(crit) >= 2 else -1

    fig, ax = plt.subplots(figsize=(10, 4.5))
    xs = list(range(len(arr)))
    ax.plot(xs, arr, "-o", color=ACCENT, linewidth=2, markersize=9, label="arr", zorder=2)
    for i in crit:
        ax.plot(i, arr[i], "o", color=ACCENT2, markersize=14, zorder=3)
        kind = "max" if arr[i] > arr[i - 1] else "min"
        ax.annotate(
            f"crit@{i}\n{kind}",
            xy=(i, arr[i]),
            xytext=(0, 18),
            textcoords="offset points",
            ha="center",
            color=ACCENT2,
            fontsize=9,
            fontweight="bold",
        )
    if len(crit) >= 2:
        # min gap between consecutive
        best_pair = min(range(len(crit) - 1), key=lambda j: crit[j + 1] - crit[j])
        a, b = crit[best_pair], crit[best_pair + 1]
        ax.annotate(
            "",
            xy=(b, arr[b]),
            xytext=(a, arr[a]),
            arrowprops=dict(arrowstyle="<->", color=WARN, lw=1.8),
        )
        ax.text(
            (a + b) / 2,
            max(arr[a], arr[b]) + 0.55,
            f"min={min_d}",
            color=WARN,
            ha="center",
            fontsize=10,
        )
        # max = first to last
        ax.annotate(
            "",
            xy=(crit[-1], arr[crit[-1]] - 0.35),
            xytext=(crit[0], arr[crit[0]] - 0.35),
            arrowprops=dict(arrowstyle="<->", color=CRIT, lw=1.5, linestyle="--"),
        )
        ax.text(
            (crit[0] + crit[-1]) / 2,
            min(arr[crit[0]], arr[crit[-1]]) - 0.9,
            f"max={max_d}",
            color=CRIT,
            ha="center",
            fontsize=10,
        )
    style_ax(ax, f"2058 · critical points  arr={arr}  → [{min_d}, {max_d}]")
    ax.set_xticks(xs)
    ax.set_xlabel("index", color=MUTED)
    ax.set_ylabel("value", color=MUTED)
    ax.set_ylim(0, max(arr) + 1.8)
    ax.grid(axis="y", alpha=0.15, color=MUTED)
    save(fig, "2058_critical.png")


# ── 2091 ends / deletion plans ──────────────────────────────────────────────
def plot_2091():
    nums = [2, 10, 7, 5, 4, 1, 8, 6]
    n = len(nums)
    i_min = int(np.argmin(nums))
    i_max = int(np.argmax(nums))
    a, b = sorted((i_min, i_max))
    both_l = b + 1
    both_r = n - a
    split = a + 1 + n - b
    best = min(both_l, both_r, split)

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(10, 6.5), gridspec_kw={"height_ratios": [2.2, 1.2]}
    )
    colors = []
    for i in range(n):
        if i == i_min:
            colors.append(ACCENT2)
        elif i == i_max:
            colors.append(ACCENT)
        else:
            colors.append("#3a4050")
    bars = ax1.bar(range(n), nums, color=colors, edgecolor=BORDER, width=0.7)
    for i, v in enumerate(nums):
        ax1.text(i, v + 0.25, str(v), ha="center", color=TEXT, fontsize=10)
    ax1.annotate(
        f"min@{i_min}",
        xy=(i_min, nums[i_min]),
        xytext=(i_min, nums[i_min] + 2.2),
        ha="center",
        color=ACCENT2,
        fontsize=10,
        arrowprops=dict(arrowstyle="->", color=ACCENT2),
    )
    ax1.annotate(
        f"max@{i_max}",
        xy=(i_max, nums[i_max]),
        xytext=(i_max, nums[i_max] + 1.5),
        ha="center",
        color=ACCENT,
        fontsize=10,
        arrowprops=dict(arrowstyle="->", color=ACCENT),
    )
    style_ax(ax1, f"2091 · nums={nums}")
    ax1.set_xticks(range(n))
    ax1.set_ylabel("value", color=MUTED)

    plans = ["both L", "both R", "split"]
    costs = [both_l, both_r, split]
    pcolors = [ACCENT2 if c == best else ACCENT for c in costs]
    ax2.barh(plans, costs, color=pcolors, edgecolor=BORDER, height=0.55)
    for y, c in enumerate(costs):
        ax2.text(c + 0.15, y, str(c), va="center", color=TEXT, fontsize=11)
    style_ax(ax2, f"deletion plans  → min = {best}")
    ax2.set_xlabel("deletions", color=MUTED)
    ax2.set_xlim(0, max(costs) + 2)
    fig.tight_layout()
    save(fig, "2091_ends.png")


# ── 2948 clusters + result ──────────────────────────────────────────────────
def plot_2948_clusters():
    nums = [1, 5, 3, 9, 8]
    limit = 2
    n = len(nums)
    ids = sorted(range(n), key=nums.__getitem__)
    clusters = []
    i = 0
    while i < n:
        j = i + 1
        while j < n and nums[ids[j]] - nums[ids[j - 1]] <= limit:
            j += 1
        clusters.append(ids[i:j])
        i = j

    cluster_of = [0] * n
    for cid, members in enumerate(clusters):
        for idx in members:
            cluster_of[idx] = cid
    palette = [ACCENT, ACCENT2, WARN, CRIT, "#c3a6ff"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    # original bars
    colors = [palette[cluster_of[i] % len(palette)] for i in range(n)]
    ax1.bar(range(n), nums, color=colors, edgecolor=BORDER, width=0.65)
    for i, v in enumerate(nums):
        ax1.text(i, v + 0.2, str(v), ha="center", color=TEXT, fontsize=11)
    style_ax(ax1, f"original  nums={nums}  limit={limit}")
    ax1.set_xticks(range(n))
    ax1.set_xlabel("index", color=MUTED)

    # scatter by value with cluster color
    for cid, members in enumerate(clusters):
        vals = [nums[i] for i in members]
        xs = [cid] * len(vals)
        ax2.scatter(
            xs,
            vals,
            s=180,
            color=palette[cid % len(palette)],
            edgecolor="white",
            linewidth=1.2,
            zorder=3,
            label=f"cluster {cid}",
        )
        for x, v, idx in zip(xs, vals, members):
            ax2.text(x + 0.12, v, f"{v}@{idx}", color=MUTED, fontsize=9, va="center")
    # gap lines between sorted values
    sorted_vals = [nums[i] for i in ids]
    for a, b in zip(sorted_vals, sorted_vals[1:]):
        gap = b - a
        ax2.annotate(
            "",
            xy=( -0.3, b),
            xytext=(-0.3, a),
            arrowprops=dict(
                arrowstyle="-",
                color=ACCENT2 if gap <= limit else CRIT,
                lw=2,
            ),
        )
    style_ax(ax2, "value clusters (gap ≤ limit)")
    ax2.set_xticks(range(len(clusters)))
    ax2.set_xticklabels([f"C{c}" for c in range(len(clusters))], color=MUTED)
    ax2.set_ylabel("value", color=MUTED)
    ax2.set_xlim(-0.6, len(clusters) - 0.2)
    ax2.legend(facecolor=PANEL, edgecolor=BORDER, labelcolor=TEXT, fontsize=9)
    fig.suptitle("2948 · sort + cluster by gap", color=TEXT, fontsize=13)
    fig.tight_layout()
    save(fig, "2948_clusters.png")


def plot_2948_result():
    nums = [1, 5, 3, 9, 8]
    limit = 2
    n = len(nums)
    ids = sorted(range(n), key=nums.__getitem__)
    ans = [0] * n
    clusters = []
    i = 0
    while i < n:
        j = i + 1
        while j < n and nums[ids[j]] - nums[ids[j - 1]] <= limit:
            j += 1
        pos = ids[i:j]
        pos_sorted = sorted(pos)
        for k, p in enumerate(pos_sorted):
            ans[p] = nums[ids[i + k]]
        clusters.append((pos, pos_sorted, [nums[ids[i + k]] for k in range(j - i)]))
        i = j

    palette = [ACCENT, ACCENT2, WARN, CRIT, "#c3a6ff"]
    cluster_of = [0] * n
    for cid, (pos, _, _) in enumerate(clusters):
        for idx in pos:
            cluster_of[idx] = cid

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    c1 = [palette[cluster_of[i] % len(palette)] for i in range(n)]
    ax1.bar(range(n), nums, color=c1, edgecolor=BORDER, width=0.65, alpha=0.45)
    for i, v in enumerate(nums):
        ax1.text(i, v + 0.2, str(v), ha="center", color=MUTED, fontsize=10)
    style_ax(ax1, "before")
    ax1.set_xticks(range(n))

    c2 = [palette[cluster_of[i] % len(palette)] for i in range(n)]
    ax2.bar(range(n), ans, color=c2, edgecolor=BORDER, width=0.65)
    for i, v in enumerate(ans):
        ax2.text(i, v + 0.2, str(v), ha="center", color=TEXT, fontsize=11, fontweight="bold")
    style_ax(ax2, f"after redistribute  → {ans}")
    ax2.set_xticks(range(n))
    fig.suptitle("2948 · zip sorted values onto sorted indices per cluster", color=TEXT, fontsize=13)
    fig.tight_layout()
    save(fig, "2948_result.png")


# ── 3568 classroom grid ─────────────────────────────────────────────────────
def plot_3568():
    grid = ["S.#L", ".R.L", "...."]
    rows, cols = len(grid), len(grid[0])
    color_map = {
        "S": ACCENT2,
        ".": "#2a2f3a",
        "#": "#1a1d24",
        "L": ACCENT,
        "R": WARN,
    }
    labels = {
        "S": "Start",
        ".": "empty",
        "#": "wall",
        "L": "litter",
        "R": "reset",
    }

    fig, ax = plt.subplots(figsize=(7, 5))
    for r in range(rows):
        for c in range(cols):
            ch = grid[r][c]
            rect = mpatches.FancyBboxPatch(
                (c, rows - 1 - r),
                0.92,
                0.92,
                boxstyle="round,pad=0.02,rounding_size=0.08",
                facecolor=color_map[ch],
                edgecolor=BORDER,
                linewidth=1.5,
            )
            ax.add_patch(rect)
            ax.text(
                c + 0.46,
                rows - 1 - r + 0.46,
                ch,
                ha="center",
                va="center",
                color=TEXT if ch != "#" else MUTED,
                fontsize=18,
                fontweight="bold",
            )
    ax.set_xlim(-0.15, cols)
    ax.set_ylim(-0.15, rows)
    ax.set_aspect("equal")
    ax.axis("off")
    style_ax(ax, "3568 · classroom grid  S.#L / .R.L / ....")
    # legend
    handles = [
        mpatches.Patch(facecolor=color_map[k], edgecolor=BORDER, label=f"{k} = {v}")
        for k, v in labels.items()
    ]
    ax.legend(
        handles=handles,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.02),
        ncol=5,
        facecolor=PANEL,
        edgecolor=BORDER,
        labelcolor=TEXT,
        fontsize=9,
    )
    save(fig, "3568_grid.png")


# ── 3875 parity plans ───────────────────────────────────────────────────────
def plot_3875():
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    style_ax(ax, "3875 · two parity plans → always True")

    boxes = [
        (0.4, 1.2, 4.2, 3.6, ACCENT, "Plan A: all even", "Keep or a−b\nneeds 0 or ≥2 odds"),
        (5.2, 1.2, 4.2, 3.6, ACCENT2, "Plan B: all odd", "Keep or a−b\nneeds ≥1 odd"),
    ]
    for x, y, w, h, color, title, body in boxes:
        rect = mpatches.FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.05,rounding_size=0.15",
            facecolor=PANEL,
            edgecolor=color,
            linewidth=2.5,
        )
        ax.add_patch(rect)
        ax.text(x + w / 2, y + h - 0.55, title, ha="center", va="top", color=color, fontsize=13, fontweight="bold")
        ax.text(x + w / 2, y + h / 2 - 0.2, body, ha="center", va="center", color=TEXT, fontsize=11)

    ax.annotate(
        "",
        xy=(5.0, 3.0),
        xytext=(4.7, 3.0),
        arrowprops=dict(arrowstyle="->", color=MUTED, lw=2),
    )
    # conclusion banner
    banner = mpatches.FancyBboxPatch(
        (2.0, 0.15),
        6.0,
        0.85,
        boxstyle="round,pad=0.04,rounding_size=0.1",
        facecolor="#1d3a2f",
        edgecolor=ACCENT2,
        linewidth=2,
    )
    ax.add_patch(banner)
    ax.text(
        5.0,
        0.55,
        "blockers cannot both fire  →  return True",
        ha="center",
        va="center",
        color=ACCENT2,
        fontsize=12,
        fontweight="bold",
    )
    save(fig, "3875_parity.png")


# ── 3904 pref max / suf min ─────────────────────────────────────────────────
def plot_3904():
    nums = [3, 1, 5, 2, 4]
    k = 2
    n = len(nums)
    pref = [0] * n
    suf = [0] * n
    pref[0] = nums[0]
    for i in range(1, n):
        pref[i] = max(pref[i - 1], nums[i])
    suf[-1] = nums[-1]
    for i in range(n - 2, -1, -1):
        suf[i] = min(suf[i + 1], nums[i])
    score = [pref[i] - suf[i] for i in range(n)]
    first = next((i for i in range(n) if score[i] <= k), -1)

    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(n)
    w = 0.2
    ax.bar(x - 1.5 * w, nums, w, color="#3a4050", edgecolor=BORDER, label="nums")
    ax.bar(x - 0.5 * w, pref, w, color=ACCENT, edgecolor=BORDER, label="pref max")
    ax.bar(x + 0.5 * w, suf, w, color=ACCENT2, edgecolor=BORDER, label="suf min")
    ax.bar(x + 1.5 * w, score, w, color=WARN, edgecolor=BORDER, label="score")
    ax.axhline(k, color=CRIT, linestyle="--", linewidth=1.5, label=f"k={k}")
    if first >= 0:
        ax.axvline(first, color=ACCENT2, linestyle=":", linewidth=2, alpha=0.8)
        ax.annotate(
            f"first stable i={first}",
            xy=(first, score[first]),
            xytext=(first + 0.6, max(score) + 0.8),
            color=ACCENT2,
            fontsize=11,
            fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=ACCENT2),
        )
    for i in range(n):
        ax.text(i + 1.5 * w, score[i] + 0.15, str(score[i]), ha="center", color=WARN, fontsize=9)
    style_ax(ax, f"3904 · nums={nums}  k={k}  → {first}")
    ax.set_xticks(x)
    ax.set_xlabel("index i", color=MUTED)
    ax.set_ylabel("value", color=MUTED)
    ax.legend(facecolor=PANEL, edgecolor=BORDER, labelcolor=TEXT, fontsize=9, ncol=5, loc="upper left")
    ax.set_ylim(0, max(max(nums), max(score), k) + 2.5)
    ax.grid(axis="y", alpha=0.12, color=MUTED)
    save(fig, "3904_prefsuf.png")


# ── 3871 threshold contributions ────────────────────────────────────────────
def plot_3871():
    n = 2_000_000
    thresholds = []
    t = 1000
    while t <= n:
        thresholds.append(t)
        t *= 1000
    contribs = [n - T + 1 for T in thresholds]
    total = sum(contribs)

    def fmt_T(T):
        if T >= 1_000_000_000:
            return f"{T // 1_000_000_000}e9"
        if T >= 1_000_000:
            return f"{T // 1_000_000}e6"
        return f"{T:,}"

    labels = [fmt_T(T) for T in thresholds]
    colors = [ACCENT, ACCENT2, WARN, "#c792ea"][: len(thresholds)]

    fig, ax = plt.subplots(figsize=(9, 5.2))
    x = np.arange(len(thresholds))
    bars = ax.bar(x, contribs, color=colors, edgecolor=BORDER, width=0.55, zorder=3)
    for bar, c in zip(bars, contribs):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            c + max(contribs) * 0.02,
            f"{c:,}\n= n−T+1",
            ha="center",
            va="bottom",
            color=TEXT,
            fontsize=10,
            fontweight="bold",
        )
    ax.annotate(
        f"total = {' + '.join(f'{c:,}' for c in contribs)} = {total:,}",
        xy=(0.5, 0.92),
        xycoords="axes fraction",
        ha="center",
        va="top",
        color=ACCENT2,
        fontsize=11,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.4", facecolor=PANEL, edgecolor=BORDER),
    )
    style_ax(ax, f"3871 · threshold contributions  n={n:,}")
    ax.set_xticks(x)
    ax.set_xticklabels([f"T={lab}" for lab in labels], color=TEXT, fontsize=12)
    ax.set_xlabel("threshold T ∈ {1000, 1e6, 1e9, …}", color=MUTED)
    ax.set_ylabel("commas added  (n − T + 1)", color=MUTED)
    ax.set_ylim(0, max(contribs) * 1.22)
    ax.grid(axis="y", alpha=0.12, color=MUTED, zorder=0)
    save(fig, "3871_thresholds.png")





# ── 2265 post-order (sum, size) tree ────────────────────────────────────────
def plot_2265():
    # Example root = [4,8,5,0,1,null,6]
    # Matching nodes: 4,5,0,1,6 (5 total). Node 8: floor(9/3)=3 ≠ 8.
    nodes = {
        "4": {"val": 4, "pos": (0.0, 3.0), "sum": 24, "size": 6, "match": True, "parent": None},
        "8": {"val": 8, "pos": (-1.6, 2.0), "sum": 9, "size": 3, "match": False, "parent": "4"},
        "5": {"val": 5, "pos": (1.6, 2.0), "sum": 11, "size": 2, "match": True, "parent": "4"},
        "0": {"val": 0, "pos": (-2.4, 1.0), "sum": 0, "size": 1, "match": True, "parent": "8"},
        "1": {"val": 1, "pos": (-0.8, 1.0), "sum": 1, "size": 1, "match": True, "parent": "8"},
        "6": {"val": 6, "pos": (2.4, 1.0), "sum": 6, "size": 1, "match": True, "parent": "5"},
    }

    fig, ax = plt.subplots(figsize=(10, 7.2))
    ax.set_facecolor(BG)

    for nid, n in nodes.items():
        if n["parent"] is None:
            continue
        p = nodes[n["parent"]]
        ax.plot(
            [p["pos"][0], n["pos"][0]],
            [p["pos"][1], n["pos"][1]],
            color=BORDER,
            linewidth=2.2,
            zorder=1,
            solid_capstyle="round",
        )

    r = 0.32
    for nid, n in nodes.items():
        x, y = n["pos"]
        face = ACCENT2 if n["match"] else PANEL
        edge = ACCENT2 if n["match"] else ACCENT
        lw = 2.8 if n["match"] else 2.0
        circ = mpatches.Circle((x, y), r, facecolor=face, edgecolor=edge, linewidth=lw, zorder=3)
        ax.add_patch(circ)
        val_color = BG if n["match"] else TEXT
        ax.text(
            x, y, str(n["val"]), ha="center", va="center", color=val_color,
            fontsize=16, fontweight="bold", zorder=4,
        )
        label = f"({n['sum']},{n['size']})"
        label_color = ACCENT2 if n["match"] else MUTED
        ax.text(
            x, y - r - 0.18, label, ha="center", va="top", color=label_color,
            fontsize=11, fontfamily="monospace", zorder=4,
        )

    ax.axis("off")
    ax.set_title(
        "2265 · post-order (sum, size)  ·  root=[4,8,5,0,1,null,6]  →  5 matches",
        color=TEXT, fontsize=13, pad=14,
    )

    legend_items = [
        mpatches.Patch(facecolor=ACCENT2, edgecolor=ACCENT2, label="match: val == ⌊sum/size⌋"),
        mpatches.Patch(facecolor=PANEL, edgecolor=ACCENT, label="no match (node 8: ⌊9/3⌋=3)"),
    ]
    ax.legend(
        handles=legend_items,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.02),
        frameon=True,
        facecolor=PANEL,
        edgecolor=BORDER,
        labelcolor=TEXT,
        fontsize=10,
        ncol=2,
    )
    ax.annotate(
        "8 ≠ 3",
        xy=(-1.6, 2.0 + r),
        xytext=(-2.9, 2.55),
        color=WARN,
        fontsize=11,
        fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=WARN, lw=1.4),
        zorder=5,
    )
    ax.set_xlim(-3.6, 3.6)
    ax.set_ylim(0.35, 3.7)
    ax.set_aspect("equal")
    ax.text(
        0.5, 0.02,
        "each label is (subtree_sum, subtree_size) returned by post-order DFS",
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        color=MUTED,
        fontsize=9,
    )
    save(fig, "2265_postorder.png")


def main():
    plot_115()
    plot_940()
    plot_2058()
    plot_2091()
    plot_2948_clusters()
    plot_2948_result()
    plot_3568()
    plot_3875()
    plot_3904()
    plot_3871()
    plot_2265()
    print("---")
    for p in sorted(OUT.glob("*.png")):
        print(f"{p.stat().st_size:8d}  {p.name}")


if __name__ == "__main__":
    main()
