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

PLATFORMS = ("Codeforces", "CSES", "UVA", "LeetCode", "Jisuanke")
BEGIN = "<!-- AUTO-INDEX:START -->"
END = "<!-- AUTO-INDEX:END -->"
REQUIRED = ("platform", "id", "title", "status", "tags")
STATUSES = {"AC", "WIP"}


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


def render(entries: list[Problem], today: date) -> str:
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
    result += ["", "## 🗂️ 依平台查找", ""]
    for platform in PLATFORMS:
        group = sorted((p for p in entries if p.platform == platform),
                       key=lambda p: (0, int(p.ident), p.title.casefold()) if p.ident.isdigit() else (1, p.ident.casefold(), p.title.casefold()))
        result.append(f"### {platform}（{len(group)} 題）")
        result.append("")
        if not group:
            result += ["目前尚無題目。", ""]
            continue
        result += [
            "| 題號 | 題目 | 標籤 | 狀態 | 解答 | 筆記 |",
            "|:--|:--|:--|:--:|:--:|:--:|",
        ]
        for p in group:
            title_link = f"[{escape_cell(p.title)}]({relink(p.folder / 'remind.md')})"
            result.append(f"| {escape_cell(p.ident)} | {title_link} | {', '.join(escape_cell(t) for t in p.tags)} | {p.status} | "
                          f"[.cpp]({relink(p.folder / 'solution.cpp')}) | [.md]({relink(p.folder / 'remind.md')}) |")
        result.append("")
    result += ["## 🧠 依演算法查找", ""]
    tag_groups: dict[str, list[Problem]] = defaultdict(list)
    for p in entries:
        for t in p.tags:
            tag_groups[t].append(p)
    if not tag_groups:
        result += ["目前尚無可分類的題目。", ""]
    for tag in sorted(tag_groups, key=str.casefold):
        members = sorted(tag_groups[tag], key=lambda p: (PLATFORMS.index(p.platform), p.ident))
        result += [f"### {escape_cell(tag)}（{len(members)} 題）", ""]
        result += [f"- {named_link(p)} · `{p.status}`" for p in members]
        result.append("")
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
        return 0 if update_readme(args.root, render(entries, current), args.check) else 1
    except (ValueError, OSError) as exc:
        print(f"錯誤：{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
