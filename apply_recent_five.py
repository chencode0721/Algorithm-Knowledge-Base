#!/usr/bin/env python3
"""Apply 'latest five per category' patch to Algorithm-Knowledge-Base.
Usage: python apply_recent_five.py /path/to/Algorithm-Knowledge-Base
"""
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
source = root / 'scripts' / 'generate_index.py'
s = source.read_text(encoding='utf-8')
if 'MAX_PREVIEW = 5' in s:
    print('Already patched.')
    raise SystemExit(0)

def replace_one(old, new):
    global s
    n = s.count(old)
    if n != 1:
        raise RuntimeError(f'Expected one exact original section; found {n}: {old[:90]!r}')
    s = s.replace(old, new, 1)

replace_one('END = "<!-- AUTO-INDEX:END -->"', 'END = "<!-- AUTO-INDEX:END -->"\nMAX_PREVIEW = 5')
replace_one('def render(entries: list[Problem], today: date) -> str:', '''def recent_first(items: list[Problem]) -> list[Problem]:
    """AC's newest solved date first; unsolved WIP last; ties deterministic."""
    return sorted(items, key=lambda p: (p.solved == "-",
                    -(date.fromisoformat(p.solved).toordinal() if p.solved != "-" else 0),
                    p.platform, p.ident.casefold(), p.title.casefold()))


def preview_footer(group: list[Problem], limit: int | None) -> list[str]:
    if limit is not None and len(group) > limit:
        return [f"[查看全部 {len(group)} 題](docs/FULL_INDEX.md)", ""]
    return []


def render(entries: list[Problem], today: date, limit: int | None = MAX_PREVIEW) -> str:''')
replace_one('''        group = sorted((p for p in entries if difficulty_level(p.difficulty) == level),
                       key=difficulty_sort)''', '''        group = recent_first([p for p in entries if difficulty_level(p.difficulty) == level])''')
replace_one('''        result += [f"- {named_link(p)} · `{p.status}` · {', '.join(escape_cell(t) for t in p.tags)}" for p in group]
        result.append("")''', '''        result += [f"- {named_link(p)} · `{p.status}` · {', '.join(escape_cell(t) for t in p.tags)}" for p in group[:limit]]
        result.append("")
        result += preview_footer(group, limit)''')
replace_one('''    result += ["## 🗂️ 依平台查找（同平台按難度排序）", ""]''', '''    result += ["## 🗂️ 依平台查找（最新完成優先）", ""]''')
replace_one('''        group = sorted((p for p in entries if p.platform == platform),
                       key=difficulty_sort)''', '''        group = recent_first([p for p in entries if p.platform == platform])''')
replace_one('''        for p in group:
            title_link''', '''        for p in group[:limit]:
            title_link''')
replace_one('''        result.append("")
    result += ["## 🧠 依演算法查找", ""]''', '''        result.append("")
        result += preview_footer(group, limit)
    result += ["## 🧠 依演算法查找", ""]''')
replace_one('''        members = sorted(tag_groups[tag], key=difficulty_sort)''', '''        members = recent_first(tag_groups[tag])''')
replace_one('''        result += [f"- {difficulty_label(p.difficulty)} · {named_link(p)} · `{p.status}`" for p in members]
        result.append("")''', '''        result += [f"- {difficulty_label(p.difficulty)} · {named_link(p)} · `{p.status}`" for p in members[:limit]]
        result.append("")
        result += preview_footer(members, limit)''')
# For the full index, remove the capped headings and supply correct links from docs/.
replace_one('''def update_readme(root: Path, block: str, check: bool) -> bool:''', '''def update_full_index(root: Path, block: str, check: bool) -> bool:
    target = root / "docs" / "FULL_INDEX.md"
    content = "# 完整題目索引\\n\\n[← 返回首頁](../README.md)\\n\\n" + block.replace("](problems/", "](../problems/")
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


def update_readme(root: Path, block: str, check: bool) -> bool:''')
replace_one('''        return 0 if update_readme(args.root, render(entries, current), args.check) else 1''', '''        home_ok = update_readme(args.root, render(entries, current), args.check)
        full_ok = update_full_index(args.root, render(entries, current, limit=None), args.check)
        return 0 if home_ok and full_ok else 1''')
# list[:None] is legal and yields the whole list, allowing one rendering function for both variants.
source.write_text(s, encoding='utf-8')
print('Patched scripts/generate_index.py. Run python scripts/generate_index.py to refresh README and full index.')
