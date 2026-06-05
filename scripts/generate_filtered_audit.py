# scripts/generate_filtered_audit.py
"""Generate repository audit and Python dependency map, filtering out third‑party and generated artifacts.

Excludes the following directories (relative to repo root):
- venv/
- .venv/
- node_modules/
- dist/
- build/
- .next/
- .cache/
- __pycache__/
- .pytest_cache/
- data/qdrant/
- data/snapshots/
- frontend/node_modules/
- frontend/dist/

Outputs:
- docs/audits/repository_audit_filtered.md
- docs/audits/dependency_map_filtered.md
"""

import os
import hashlib
import re
from collections import defaultdict, Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # repo root
DOCS_DIR = os.path.join(ROOT, "docs")

EXCLUDE_DIRS = {
    "venv",
    ".venv",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".cache",
    "__pycache__",
    ".pytest_cache",
    os.path.join("data", "qdrant"),
    os.path.join("data", "snapshots"),
    os.path.join("frontend", "node_modules"),
    os.path.join("frontend", "dist"),
}

def is_excluded(path: str) -> bool:
    """Return True if the file resides in an excluded directory."""
    rel = os.path.relpath(path, ROOT)
    parts = rel.split(os.sep)
    # check any parent directory matches excluded set
    for i in range(1, len(parts) + 1):
        prefix = os.path.join(*parts[:i])
        if prefix in EXCLUDE_DIRS:
            return True
    return False

def all_files():
    for dirpath, _, filenames in os.walk(ROOT):
        # skip excluded directories early
        rel_dir = os.path.relpath(dirpath, ROOT)
        if rel_dir != '.' and any(rel_dir.startswith(ex) for ex in EXCLUDE_DIRS):
            continue
        for f in filenames:
            if f.startswith('.'):
                continue
            full_path = os.path.join(dirpath, f)
            if is_excluded(full_path):
                continue
            yield full_path

def count_files():
    totals = Counter()
    for path in all_files():
        ext = os.path.splitext(path)[1].lower()
        if ext == ".py":
            totals["python"] += 1
        elif ext in {".ts", ".tsx"}:
            totals["tsx"] += 1
        elif ext == ".md":
            totals["markdown"] += 1
        totals["all"] += 1
    return totals

def find_duplicate_markdowns():
    hash_map = defaultdict(list)
    for path in all_files():
        if path.endswith('.md'):
            try:
                with open(path, 'rb') as f:
                    content = f.read()
                h = hashlib.md5(content).hexdigest()
                hash_map[h].append(path)
            except Exception:
                continue
    return {h: ps for h, ps in hash_map.items() if len(ps) > 1}

def list_largest_directories(n=20):
    dir_counts = Counter()
    for path in all_files():
        dirpath = os.path.dirname(path)
        dir_counts[dirpath] += 1
    return dir_counts.most_common(n)

def find_markdown_outside_docs():
    md_files = []
    for path in all_files():
        if path.endswith('.md') and not path.startswith(DOCS_DIR):
            md_files.append(os.path.relpath(path, ROOT))
    return md_files

def build_dependency_map():
    dep_map = defaultdict(set)
    import_regex = re.compile(r'^(?:from|import)\s+([\w\.]+)')
    for path in all_files():
        if not path.endswith('.py'):
            continue
        rel_path = os.path.relpath(path, ROOT)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    m = import_regex.search(line)
                    if m:
                        mod = m.group(1)
                        dep_map[mod].add(rel_path)
        except Exception:
            continue
    return dep_map

def is_high_impact(module, importers):
    high_dirs = ('api/', 'retrieval/', 'tests/', '.github/')
    if len(importers) > 3:
        return True
    for imp in importers:
        if any(imp.startswith(d) for d in high_dirs):
            return True
    return False

def main():
    totals = count_files()
    dup = find_duplicate_markdowns()
    largest_dirs = list_largest_directories()
    markdown_outside = find_markdown_outside_docs()

    # Repository audit filtered
    audit_path = os.path.join(DOCS_DIR, "audits", "repository_audit_filtered.md")
    with open(audit_path, "w", encoding="utf-8") as out:
        out.write("# Repository Audit (Filtered)\n\n")
        out.write(f"* Total first‑party files: {totals['all']}\n")
        out.write(f"* First‑party Python files: {totals['python']}\n")
        out.write(f"* First‑party TS/TSX files: {totals['tsx']}\n")
        out.write(f"* First‑party Markdown files: {totals['markdown']}\n\n")
        out.write("## Duplicate Markdown Reports\n")
        if dup:
            for h, paths in dup.items():
                out.write(f"- Duplicate set (hash {h[:8]}):\n")
                for p in paths:
                    out.write(f"  - {os.path.relpath(p, ROOT)}\n")
        else:
            out.write("None found.\n")
        out.write("\n## Top 20 Largest Directories (by file count)\n")
        for d, cnt in largest_dirs:
            out.write(f"- {os.path.relpath(d, ROOT)} : {cnt} files\n")
        out.write("\n## Markdown Files Outside docs/\n")
        if markdown_outside:
            for p in markdown_outside:
                out.write(f"- {p}\n")
        else:
            out.write("None found.\n")

    # Dependency map filtered
    dep_map = build_dependency_map()
    dep_path = os.path.join(DOCS_DIR, "audits", "dependency_map_filtered.md")
    with open(dep_path, "w", encoding="utf-8") as out:
        out.write("# Dependency Map (Filtered)\n\n")
        out.write("Module → Imported By\n")
        out.write("---\n")
        for mod, importers in sorted(dep_map.items(), key=lambda x: (-len(x[1]), x[0])):
            mod_path = os.path.join(ROOT, *mod.split('.')) + '.py'
            if not os.path.exists(mod_path) or is_excluded(mod_path):
                continue
            high = is_high_impact(mod, importers)
            header = f"**{mod}**" if high else mod
            out.write(f"{header} | {', '.join(sorted(importers))}\n")
            if high:
                out.write("> **HIGH IMPACT – DO NOT MOVE**\n\n")
    print("Filtered audit and dependency map generated.")

if __name__ == "__main__":
    main()
