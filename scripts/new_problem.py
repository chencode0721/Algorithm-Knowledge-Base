#!/usr/bin/env python3
"""Create a new problem folder with solution.cpp and remind.md."""
import argparse
from datetime import datetime
from pathlib import Path
import re
import sys
import unicodedata
from zoneinfo import ZoneInfo

PLATFORMS = ("Codeforces", "CSES", "UVA", "LeetCode")
ROOT = Path(__file__).resolve().parents[1]


def slugify(label: str) -> str:
    normalized = unicodedata.normalize("NFKD", label)
    slug = re.sub(r"[^A-Za-z0-9]+", "-", normalized).strip("-")
    return slug or "Problem"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a problem and note pair")
    parser.add_argument("platform", choices=PLATFORMS)
    parser.add_argument("id", help="題號（例如 4A / 10038 / 0001）")
    parser.add_argument("title", help="題目名稱，例如 'Two Sum'")
    parser.add_argument("--tags", default="Uncategorized", help="逗號分隔，如 'Array, Hash Map'")
    parser.add_argument("--category", help="CSES 專用章節，如 'Introductory Problems'")
    parser.add_argument("--difficulty", default="-", help="如 Easy / Medium / Hard / 800")
    parser.add_argument("--status", choices=("WIP", "AC"), default="WIP")
    parser.add_argument("--solved", default="-", help="AC 時可填 YYYY-MM-DD，預設今天")
    parser.add_argument("--review", default="-", help="下次複習日期 YYYY-MM-DD")
    parser.add_argument("--url", default="-", help="題目網址")
    args = parser.parse_args()

    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.id):
        parser.error("題號只能包含英數字、底線或連字號")
    if any(c in args.title for c in "\n\r") or any(c in args.tags for c in "\n\r"):
        parser.error("標題與 tags 不能換行")
    if args.platform != "CSES" and args.category:
        parser.error("--category 僅供 CSES 使用")
    base = ROOT / "problems" / args.platform
    if args.platform == "CSES":
        base = base / slugify(args.category or "Uncategorized")
    destination = base / f"{args.id}-{slugify(args.title)}"
    if destination.exists():
        print(f"資料夾已存在，沒有覆蓋任何檔案：{destination}", file=sys.stderr)
        return 1

    solved = args.solved
    if args.status == "AC" and solved == "-":
        solved = datetime.now(ZoneInfo("Asia/Taipei")).date().isoformat()
    if args.status == "WIP" and solved != "-":
        parser.error("WIP 狀態請不要指定 solved 日期")
    for field, val in (("solved", solved), ("review", args.review)):
        if val != "-":
            try:
                datetime.strptime(val, "%Y-%m-%d")
            except ValueError:
                parser.error(f"{field} 日期請用 YYYY-MM-DD")
    # Reject line-injection into front matter, but ordinary colons/spaces in title/URL are OK.
    for key in ("title", "tags", "difficulty", "url"):
        if "\n" in getattr(args, key) or "\r" in getattr(args, key):
            parser.error(f"{key} 不可換行")
    substitutions = {
        "{{PLATFORM}}": args.platform,
        "{{ID}}": args.id,
        "{{TITLE}}": args.title,
        "{{TAGS}}": args.tags,
        "{{DIFFICULTY}}": args.difficulty,
        "{{STATUS}}": args.status,
        "{{SOLVED}}": solved,
        "{{REVIEW_DATE}}": args.review,
        "{{URL}}": args.url,
    }
    source = "solution-leetcode.cpp" if args.platform == "LeetCode" else "solution-main.cpp"
    files = {
        "remind.md": (ROOT / "templates" / "remind.md").read_text(encoding="utf-8"),
        "solution.cpp": (ROOT / "templates" / source).read_text(encoding="utf-8"),
    }
    base.mkdir(parents=True, exist_ok=True)
    destination.mkdir()
    for filename, content in files.items():
        for pattern, value in substitutions.items():
            content = content.replace(pattern, value)
        (destination / filename).write_text(content, encoding="utf-8")
    print(f"已建立：{destination.relative_to(ROOT)}")
    print("請完成 solution.cpp，並更新 remind.md 的 status、solved、review_date。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
