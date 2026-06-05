# scripts/generate_repo_audit_and_dependency_map.py
"""Generate repository audit and Python dependency map.
Produces two markdown files in the docs/ folder:
- docs/audits/repository_audit.md
- docs/audits/dependency_map.md
The script is safe to run on the existing repository; it does not move any files.
"""
import os
import hashlib
import re
from collections import defaultdict, Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # repo root (scripts/ -> repo)
DOCS_DIR = os.path.join(ROOT, "docs")

def all_files():
    for dirpath, _, filenames in os.walk(ROOT):
        for f in filenames:
            if f.startswith('.'):
                continue
            yield os.path.join(dirpath, f)

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
        elif ext in {".js", ".jsx"}:
            totals["js"] += 1
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

def list_largest_directories(n=5):
    dir_counts = Counter()
    for path in all_files():
        dirpath = os.path.dirname(path)
        dir_counts[dirpath] += 1
    return dir_counts.most_common(n)

def find_generated_artifacts():
    generated = []
    for path in all_files():
        rel = os.path.relpath(path, ROOT)
        if rel.startswith('docs/') and any(word in os.path.basename(path).lower() for word in ['report', 'benchmark', 'accuracy', 'score', 'audit']):
            generated.append(rel)
    return generated

def find_experimental_files():
    experimental = []
    pattern = re.compile(r"(EXPERIMENTAL|TODO|FIXME|DEPRECATED|WIP)", re.IGNORECASE)
    for path in all_files():
        if path.endswith('.py') or path.endswith('.md'):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if pattern.search(content):
                    experimental.append(os.path.relpath(path, ROOT))
            except Exception:
                continue
    return experimental

def find_legacy_files():
    legacy = []
    for path in all_files():
        name = os.path.basename(path).lower()
        if 'legacy' in name:
            legacy.append(os.path.relpath(path, ROOT))
    return legacy

def find_orphan_py_files():
    modules = {}
    for path in all_files():
        if path.endswith('.py'):
            rel = os.path.relpath(path, ROOT)
            mod = rel[:-3].replace(os.sep, '.')
            modules[mod] = rel
    imported = defaultdict(set)
    import_pattern = re.compile(r"^(?:from|import)\s+([\w\.]+)")
    for path in all_files():
        if path.endswith('.py'):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    for line in f:
                        m = import_pattern.search(line)
                        if m:
                            imported_mod = m.group(1)
                            imported[imported_mod].add(os.path.relpath(path, ROOT))
            except Exception:
                continue
    orphan = []
    for mod, rel in modules.items():
        if mod not in imported:
            orphan.append(rel)
    return orphan

def build_dependency_map():
    dep_map = defaultdict(set)
    import_regex = re.compile(r"^(?:from|import)\s+([\w\.]+)")
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
    generated = find_generated_artifacts()
    experimental = find_experimental_files()
    legacy = find_legacy_files()
    orphan = find_orphan_py_files()

    audit_path = os.path.join(DOCS_DIR, "audits", "repository_audit.md")
    with open(audit_path, "w", encoding="utf-8") as out:
        out.write("# Repository Audit\n\n")
        out.write(f"* Total files: {totals['all']}\n")
        out.write(f"* Python files: {totals['python']}\n")
        out.write(f"* TypeScript/TSX files: {totals['tsx']}\n")
        out.write(f"* Markdown files: {totals['markdown']}\n\n")
        out.write("## Duplicate Markdown Reports\n")
        if dup:
            for h, paths in dup.items():
                out.write(f"- Duplicate set (hash {h[:8]}):\n")
                for p in paths:
                    out.write(f"  - {os.path.relpath(p, ROOT)}\n")
        else:
            out.write("None found.\n")
        out.write("\n## Orphaned Python Files (no imports)\n")
        if orphan:
            for p in orphan:
                out.write(f"- {p}\n")
        else:
            out.write("None detected.\n")
        out.write("\n## Experimental Files\n")
        for p in experimental:
            out.write(f"- {p}\n")
        out.write("\n## Legacy Files\n")
        for p in legacy:
            out.write(f"- {p}\n")
        out.write("\n## Largest Directories (by file count)\n")
        for d, cnt in largest_dirs:
            out.write(f"- {os.path.relpath(d, ROOT)} : {cnt} files\n")
        out.write("\n## Generated Artifacts (heuristic)\n")
        for p in generated:
            out.write(f"- {p}\n")
        out.write("\n---\nGenerated by audit script.\n")

    dep_map = build_dependency_map()
    dep_path = os.path.join(DOCS_DIR, "audits", "dependency_map.md")
    with open(dep_path, "w", encoding="utf-8") as out:
        out.write("# Dependency Map\n\n")
        out.write("Module → Imported By\n")
        out.write("---\n")
        for mod, importers in sorted(dep_map.items(), key=lambda x: (-len(x[1]), x[0])):
            # verify module file exists
            mod_path = os.path.join(ROOT, *mod.split('.')) + '.py'
            if not os.path.exists(mod_path):
                continue
            high = is_high_impact(mod, importers)
            header = f"**{mod}**" if high else mod
            out.write(f"{header} | {', '.join(sorted(importers))}\n")
            if high:
                out.write("> **HIGH IMPACT – DO NOT MOVE**\n\n")
    print("Audit and dependency map generated.")

if __name__ == "__main__":
    main()
