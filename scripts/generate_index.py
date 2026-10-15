#!/usr/bin/env python3
"""Generate README indices from per-problem remind.md metadata (stdlib only)."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path
from urllib.parse import quote
from zoneinfo import ZoneInfo
from datetime import datetime
import re
import sys

PLATFORMS = ("Codeforces", "CSES", "UVA", "LeetCode", "Jisuanke", "Luogu")
BEGIN = "<!-- AUTO-INDEX:START -->"
END = "<!-- AUTO-INDEX:END -->"
MAX_PREVIEW = 5
REQUIRED = ("platform", "id", "title", "status", "tags")
STATUSES = {"AC", "WIP"}
# Level 1 is the easiest. 9 is used only when a note has not been migrated yet.
DIFFICULTY_LEVELS = (
    ("🔴", "啟蒙"),
    ("🟠", "基礎"),
    ("🟡", "初階"),
    ("🟢", "中階"),
    ("🩵", "進階"),
    ("🔵", "高階"),
    ("🟣", "專家"),
    ("⚫", "大師"),
)


def difficulty_level(raw: str) -> int:
    """Return 1..8, or 9 for unclassified/legacy values.

    Pre-upgrade values such as 'Beginner', 'Medium', and Codeforces ratings
    are intentionally NOT mapped to a subjective level automatically.
    """
    value = str(raw).strip()
    return int(value) if value in {str(n) for n in range(1, 9)} else 9


def difficulty_label(raw: str) -> str:
    level = difficulty_level(raw)
    if level == 9:
        return "⚪ 未分類"
    dot, name = DIFFICULTY_LEVELS[level - 1]
    return f"{dot} Lv.{level} {name}"


def difficulty_sort(p: 'Problem') -> tuple[int, int, str, str]:
    id_is_numeric = p.ident.isdigit()
    return (difficulty_level(p.difficulty), PLATFORMS.index(p.platform),
            f"{int(p.ident):012d}" if id_is_numeric else p.ident.casefold(),
            p.title.casefold())


@dataclass(frozen=True)
class Problem:
    platform: str
    ident: str
    title: str
    status: str
    tags: tuple[str, ...]
    difficulty: str
    solved: str
    review_date: str
    url: str
    folder: Path


def read_meta(filename: Path) -> dict[str, str]:
    lines = filename.read_text(encoding="utf-8-sig").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"{filename}: remind.md 必須以 --- 中繼資料開頭")
    try:
        ending = next(i for i, s in enumerate(lines[1:], 1) if s.strip() == "---")
    except StopIteration as exc:
        raise ValueError(f"{filename}: 找不到結束中繼資料的 ---") from exc
    meta: dict[str, str] = {}
    for raw in lines[1:ending]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if ":" not in raw:
            raise ValueError(f"{filename}: 格式錯誤：{raw!r}")
        key, value = raw.split(":", 1)
        key = key.strip()
        if not re.fullmatch(r"[a-z_]+", key) or key in meta:
            raise ValueError(f"{filename}: 中繼資料欄位無效或重複：{key!r}")
        # Support a deliberately small 'key: text' subset of YAML.
        meta[key] = value.strip().strip('"').strip("'")
    missing = [key for key in REQUIRED if not meta.get(key)]
    if missing:
        raise ValueError(f"{filename}: 缺少必要欄位：{', '.join(missing)}")
    return meta


def parse_optional_date(value: str, context: str) -> str:
    if not value or value in {"-", "—"}:
        return "-"
    try:
        date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{context}: 日期需使用 YYYY-MM-DD，收到 {value!r}") from exc
    return value


def canonical_id(s: str) -> str:
    return str(int(s)) if s.isdigit() else s.casefold()


def collect(root: Path) -> list[Problem]:
    basedir = root / "problems"
    entries: list[Problem] = []
    ids: set[tuple[str, str]] = set()
    for note in sorted(basedir.rglob("remind.md")):
        folder = note.parent.relative_to(root)
        bits = folder.parts
        if len(bits) < 3 or bits[0] != "problems" or bits[1] not in PLATFORMS:
            raise ValueError(f"{note}: 題目應存放於 problems/<平台>/<題目資料夾>/")
        data = read_meta(note)
        platform = data["platform"]
        if platform != bits[1]:
            raise ValueError(f"{note}: platform={platform!r} 與資料夾 {bits[1]!r} 不一致")
        if data["status"] not in STATUSES:
            raise ValueError(f"{note}: status 僅允許 AC 或 WIP")
        if not (note.parent / "solution.cpp").is_file():
            raise ValueError(f"{note}: 找不到同資料夾的 solution.cpp")
        key = (platform, canonical_id(data["id"]))
        if key in ids:
            raise ValueError(f"{note}: 重複題號：{platform} {data['id']}")
        ids.add(key)
        tags = tuple(dict.fromkeys(t.strip() for t in data["tags"].strip("[]").split(",") if t.strip()))
        if not tags:
            raise ValueError(f"{note}: tags 至少需要一個演算法標籤")
        solved = parse_optional_date(data.get("solved", "-"), str(note))
        review_date = parse_optional_date(data.get("review_date", "-"), str(note))
        if data["status"] == "AC" and solved == "-":
            raise ValueError(f"{note}: status=AC 時必須填 solved 日期")
        entries.append(Problem(platform, data["id"], data["title"], data["status"],
                               tags, data.get("difficulty", "-"), solved,
                               review_date, data.get("url", "-"), folder))
    return entries


def escape_cell(value: str) -> str:
    return value.replace("|", r"\|").replace("\n", " ").replace("`", r"\`")


def relink(path: Path) -> str:
    return quote(path.as_posix(), safe="/-._~")


def named_link(p: Problem) -> str:
    return f"[{escape_cell(p.platform)} {escape_cell(p.ident)} — {escape_cell(p.title)}]({relink(p.folder / 'remind.md')})"


def recent_first(items: list[Problem]) -> list[Problem]:
    """AC's newest solved date first; unsolved WIP last; ties deterministic."""
    return sorted(items, key=lambda p: (p.solved == "-",
                    -(date.fromisoformat(p.solved).toordinal() if p.solved != "-" else 0),
                    p.platform, p.ident.casefold(), p.title.casefold()))


def preview_footer(group: list[Problem], limit: int | None) -> list[str]:
    if limit is not None and len(group) > limit:
        return [f"[查看全部 {len(group)} 題](docs/FULL_INDEX.md)", ""]
    return []


def render(entries: list[Problem], today: date, limit: int | None = MAX_PREVIEW) -> str:
    ac = sum(p.status == "AC" for p in entries)
    result = [
        "> 此區由 `python scripts/generate_index.py` 自動產生。只需修改各題的 `remind.md`；**不要直接改此區**。",
        "",
        "## 📊 刷題統計",
        "",
        f"**總收錄：{len(entries)} 題｜已 AC：{ac} 題｜進行中：{len(entries) - ac} 題**",
        "",
        "| 平台 | AC | WIP | 總題數 |",
        "|:--|--:|--:|--:|",
    ]
    for platform in PLATFORMS:
        group = [p for p in entries if p.platform == platform]
        success = sum(p.status == "AC" for p in group)
        result.append(f"| {platform} | {success} | {len(group) - success} | {len(group)} |")
    result += [
        "", "## 🎨 八級難度統計（由易到難）", "",
        "> 全部平台共用的個人評分，非各判題網站官方難度。`difficulty: 1` 到 `8`；舊值與 `-` 暫列未分類。", "",
        "| 難度 | 題目數 | AC | WIP |", "|:--|--:|--:|--:|",
    ]
    for level in range(1, 10):
        group = [p for p in entries if difficulty_level(p.difficulty) == level]
        success = sum(p.status == "AC" for p in group)
        label = difficulty_label(str(level)) if level <= 8 else "⚪ 未分類"
        result.append(f"| {label} | {len(group)} | {success} | {len(group)-success} |")

    result += ["", "## 🪜 依難度查找（由易到難）", ""]
    for level in range(1, 10):
        group = recent_first([p for p in entries if difficulty_level(p.difficulty) == level])
        if not group:
            continue
        label = difficulty_label(str(level)) if level <= 8 else "⚪ 未分類"
        result += [f"### {label}（{len(group)} 題）", ""]
        result += [f"- {named_link(p)} · `{p.status}` · {', '.join(escape_cell(t) for t in p.tags)}" for p in group[:limit]]
        result.append("")
        result += preview_footer(group, limit)
    if not entries:
        result += ["尚未收錄題目。", ""]

    result += ["## 🗂️ 依平台查找（最新完成優先）", ""]
    for platform in PLATFORMS:
        group = recent_first([p for p in entries if p.platform == platform])
        result.append(f"### {platform}（{len(group)} 題）")
        result.append("")
        if not group:
            result += ["目前尚無題目。", ""]
            continue
        result += [
            "| 難度 | 題號 | 題目 | 標籤 | 狀態 | 解答 | 筆記 |",
            "|:--|:--|:--|:--|:--:|:--:|:--:|",
        ]
        for p in group[:limit]:
            title_link = f"[{escape_cell(p.title)}]({relink(p.folder / 'remind.md')})"
            result.append(f"| {difficulty_label(p.difficulty)} | {escape_cell(p.ident)} | {title_link} | {', '.join(escape_cell(t) for t in p.tags)} | {p.status} | "
                          f"[.cpp]({relink(p.folder / 'solution.cpp')}) | [.md]({relink(p.folder / 'remind.md')}) |")
        result.append("")
        result += preview_footer(group, limit)
    result += ["## 🧠 依演算法查找", ""]
    tag_groups: dict[str, list[Problem]] = defaultdict(list)
    for p in entries:
        for t in p.tags:
            tag_groups[t].append(p)
    if not tag_groups:
        result += ["目前尚無可分類的題目。", ""]
    for tag in sorted(tag_groups, key=str.casefold):
        members = recent_first(tag_groups[tag])
        result += [f"### {escape_cell(tag)}（{len(members)} 題）", ""]
        result += [f"- {difficulty_label(p.difficulty)} · {named_link(p)} · `{p.status}`" for p in members[:limit]]
        result.append("")
        result += preview_footer(members, limit)
    result += ["## 🔁 複習清單（台灣時間）", ""]
    due = sorted((p for p in entries if p.status == "AC" and p.review_date != "-" and p.review_date <= today.isoformat()),
                 key=lambda p: (p.review_date, p.platform, p.ident))
    upcoming = sorted((p for p in entries if p.status == "AC" and p.review_date != "-" and today.isoformat() < p.review_date <= (today + timedelta(days=7)).isoformat()),
                      key=lambda p: (p.review_date, p.platform, p.ident))
    result += ["### 已到期", ""]
    result += ([f"- {p.review_date} · {named_link(p)}" for p in due] if due else ["無到期題目。"])
    result += ["", "### 接下來 7 天", ""]
    result += ([f"- {p.review_date} · {named_link(p)}" for p in upcoming] if upcoming else ["無排定題目。"])
    result += ["", "<sub>提醒：複習後請自行更新該題 `review_date`；系統只負責產生清單，不會自動判定你已經複習。</sub>"]
    return "\n".join(result).rstrip() + "\n"


def update_full_index(root: Path, block: str, check: bool) -> bool:
    target = root / "docs" / "FULL_INDEX.md"
    content = "# 完整題目索引\n\n[← 返回首頁](../README.md)\n\n" + block.replace("](problems/", "](../problems/")
    old = target.read_text(encoding="utf-8") if target.exists() else None
    if check:
        if old != content:
            print("docs/FULL_INDEX.md 尚未同步", file=sys.stderr)
        return old == content
    target.parent.mkdir(parents=True, exist_ok=True)
    if old != content:
        target.write_text(content, encoding="utf-8")
    print(f"docs/FULL_INDEX.md {'已更新' if old != content else '已是最新'}")
    return True


def update_readme(root: Path, block: str, check: bool) -> bool:
    readme = root / "README.md"
    old = readme.read_text(encoding="utf-8")
    if old.count(BEGIN) != 1 or old.count(END) != 1 or old.index(BEGIN) > old.index(END):
        raise ValueError("README.md 需要各有一個 AUTO-INDEX:START / END 標記，順序正確")
    first, rest = old.split(BEGIN, 1)
    _, last = rest.split(END, 1)
    new = first + BEGIN + "\n" + block + END + last
    changed = new != old
    if check:
        if changed:
            print("README.md 尚未同步：請執行 python scripts/generate_index.py", file=sys.stderr)
        return not changed
    if changed:
        readme.write_text(new, encoding="utf-8")
    print(f"README.md {'已更新' if changed else '已是最新'}")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="Build platform, tag and review indices in README.md")
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="Repository root")
    ap.add_argument("--check", action="store_true", help="Exit nonzero if README is stale; do not write")
    ap.add_argument("--today", help="YYYY-MM-DD (for deterministic tests)")
    args = ap.parse_args()
    try:
        current = date.fromisoformat(args.today) if args.today else datetime.now(ZoneInfo("Asia/Taipei")).date()
        entries = collect(args.root)
        print(f"已讀取 {len(entries)} 題，AC {sum(p.status == 'AC' for p in entries)} 題")
        home_ok = update_readme(args.root, render(entries, current), args.check)
        full_ok = update_full_index(args.root, render(entries, current, limit=None), args.check)
        return 0 if home_ok and full_ok else 1
    except (ValueError, OSError) as exc:
        print(f"錯誤：{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
