#!/usr/bin/env python3
"""Install the learning kit into a project, or audit an installation.

Usage:
  init_project.py <project-dir> [flags]

  --dry-run           print every action, write nothing
  --update            refresh an existing installation (needs its manifest; refuses otherwise)
  --check             read-only audit: local drift, behind-the-kit files, config keys, hook
  --link              symlink skill dirs instead of copying them (see docs/WIRING.md)
  --force             overwrite a locally modified kit-owned file (prints each one)
  --seed-topics a,b,c create those topic folders from the templates
  --git-init          git init -b main if the project is not a repo (never commits)
  --title "..."       the project title written into a fresh config and the templates

Ownership:
  kit-owned     .claude/kit/**, .claude/skills/<kit skill>/**, scripts/validate.py,
                docs/AI-SYSTEM-GUIDE.md, docs/principles.md
                -> replaced only when the file still matches the manifest hash; a locally
                   edited file, or an existing file with no manifest entry (first install
                   over a hand-made copy), is kept and the new version lands as <file>.kit-new
  shared        .claude/settings.json -> JSON merge, backup first, never replaced
  project       learning.config.json, CLAUDE.md, PLAN.md, STATUS.md, ABOUT-ME.md,
                .gitignore, topics/** -> created if absent, then never touched again
  untouched     any other .claude/skills/<name>/ the project has of its own
"""
import argparse
import datetime as dt
import difflib
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys

KIT = pathlib.Path(__file__).resolve().parent
MANIFEST = ".claude/.kit-manifest.json"
CONFIG = "learning.config.json"
HOOK_MARK = "due_reviews.py"

PROJECT_FILES = {  # template -> destination
    "templates/learning.config.json": CONFIG,
    "templates/CLAUDE.md": "CLAUDE.md",
    "templates/PLAN.md": "PLAN.md",
    "templates/STATUS.md": "STATUS.md",
    "templates/ABOUT-ME.md": "ABOUT-ME.md",
    "templates/gitignore": ".gitignore",
}
KIT_FILES = {  # kit path -> destination
    "scripts/validate.py": "scripts/validate.py",
    "docs/AI-SYSTEM-GUIDE.md": "docs/AI-SYSTEM-GUIDE.md",
    "docs/principles.md": "docs/principles.md",
}


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


class Report:
    def __init__(self, dry):
        self.dry = dry
        self.rows = []

    def add(self, kind, path, note=""):
        self.rows.append((kind, str(path), note))
        prefix = "would " if self.dry else ""
        line = f"  {prefix}{kind:<14} {path}"
        print(line + (f"   ({note})" if note else ""))

    def count(self, kind):
        return sum(1 for k, _, _ in self.rows if k == kind)


def load_json(path):
    try:
        return json.loads(pathlib.Path(path).read_text(encoding="utf-8")), None
    except FileNotFoundError:
        return None, "missing"
    except json.JSONDecodeError as e:
        return None, str(e)


def substitutions(project, cfg, title):
    defaults, _ = load_json(KIT / "kit" / "defaults.json")
    paths = defaults["paths"]
    layout = defaults["layout"]
    grading = defaults["grading"]
    review = defaults["review"]
    if cfg:
        paths = {**paths, **cfg.get("paths", {})}
        grading = {**grading, **cfg.get("grading", {})}
        review = {**review, **cfg.get("review", {})}
    start = (cfg or {}).get("plan", {}).get("start_date") or next_monday()
    name = (cfg or {}).get("project", {}).get("name") or project.name
    ttl = title or (cfg or {}).get("project", {}).get("title") or project.name
    return {
        "KIT_VERSION": (KIT / "VERSION").read_text().strip(),
        "PROJECT_NAME": name,
        "PROJECT_TITLE": ttl,
        "START_DATE": start,
        "TOPICS_DIR": paths["topics_dir"],
        "PLAN_FILE": paths["plan_file"],
        "STATUS_FILE": paths["status_file"],
        "ABOUT_FILE": paths["about_file"],
        "CAUSES": ", ".join(f"`{c}`" for c in grading["causes"]),
        "LADDER": ", ".join(f"+{d}d" for d in review["ladder_days"]),
        "GAP_EXAMPLE": "<one real gap from this project, phrased as a testable sentence>",
        "TABLE": render_table(layout["tables"]["error_log"]),
    }


def render_table(header):
    return "| " + " | ".join(header) + " |\n|" + "|".join("---" for _ in header) + "|\n"


def next_monday():
    today = dt.date.today()
    return (today + dt.timedelta(days=(7 - today.weekday()) % 7 or 7)).isoformat()


def fill(text, subs):
    for k, v in subs.items():
        text = text.replace("{{" + k + "}}", str(v))
    return text


def copy_kit_file(src, dst, manifest, rep, dry, force):
    """Copy a kit-owned file, protecting local edits. Returns the new hash or None."""
    dst = pathlib.Path(dst)
    if dst.exists():
        current = sha(dst)
        recorded = manifest.get("files", {}).get(manifest_key(dst, manifest))
        if current == sha(src):
            rep.add("unchanged", dst)
            return current
        # never recorded = a file the kit did not write; treat it as a local edit
        if recorded != current and not force:
            new = dst.with_suffix(dst.suffix + ".kit-new")
            rep.add("MODIFIED keep", dst, f"new version -> {new.name}")
            if not dry:
                shutil.copy2(src, new)
            return current
        rep.add("update", dst)
    else:
        rep.add("create", dst)
    if not dry:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        return sha(dst)
    return None


def manifest_key(path, manifest):
    root = pathlib.Path(manifest.get("_root", ""))
    try:
        return str(pathlib.Path(path).resolve().relative_to(root))
    except Exception:
        return str(path)


def walk(src):
    for p in sorted(pathlib.Path(src).rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts and p.name != ".DS_Store":
            yield p


def merge_settings(project, rep, dry):
    """Add the SessionStart hook without disturbing anything already there."""
    path = project / ".claude" / "settings.json"
    block, _ = load_json(KIT / "templates" / "settings.json")
    entry = block["hooks"]["SessionStart"][0]
    if not path.exists():
        rep.add("create", path, "SessionStart hook")
        if not dry:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(block, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return True
    data, err = load_json(path)
    if data is None:
        print(f"\nerror: {path} is not valid JSON ({err}). Nothing written.")
        print("Add this to hooks.SessionStart yourself:\n")
        print(json.dumps(entry, indent=2, ensure_ascii=False))
        return False
    before = json.dumps(data, indent=2, ensure_ascii=False)
    hooks = data.setdefault("hooks", {}).setdefault("SessionStart", [])
    if any(HOOK_MARK in json.dumps(h) for h in hooks):
        rep.add("hook present", path)
        return True
    hooks.append(entry)
    after = json.dumps(data, indent=2, ensure_ascii=False)
    rep.add("merge", path, "appended the SessionStart hook")
    diff = "\n".join(difflib.unified_diff(before.splitlines(), after.splitlines(),
                                          "settings.json", "settings.json (new)", lineterm=""))
    print("\n".join("    " + l for l in diff.splitlines()))
    if not dry:
        stamp = dt.datetime.now().strftime("%Y-%m-%d-%H%M%S")
        shutil.copy2(path, path.with_name(f"settings.json.bak-{stamp}"))
        path.write_text(after + "\n", encoding="utf-8")
    return True


def seed_topic(project, name, subs, cfg, rep, dry):
    topics = project / subs["TOPICS_DIR"] / name
    if topics.exists():
        rep.add("skip (exists)", topics)
        return
    rep.add("seed topic", topics)
    if dry:
        return
    topics.mkdir(parents=True, exist_ok=True)
    tables = {"error-log.md": "error_log", "glossary.md": "glossary", "patterns.md": "patterns"}
    layout, _ = load_json(KIT / "kit" / "defaults.json")
    tdef = {**layout["layout"]["tables"], **(cfg or {}).get("layout", {}).get("tables", {})}
    for tpl in walk(KIT / "templates" / "topic"):
        if tpl.name == "patterns.md" or tpl.name == "deep-dive.md":
            continue  # created lazily by the skills
        local = dict(subs)
        local["TITLE"] = name
        local["STATE"] = "locked"
        local.update({"NEEDS": "-", "UNLOCKS": "-", "BAR": "-", "WEEKS": "-", "EST_HOURS": "-",
                      "NEXT_ACTION": "-", "SUBTOPICS": "| | - | no | |", "EXIT_BAR": "<see PLAN.md §3>",
                      "SOURCES": "- <where the material is>"})
        if tpl.name in tables:
            local["TABLE"] = render_table(tdef[tables[tpl.name]])
        (topics / tpl.name).write_text(fill(tpl.read_text(encoding="utf-8"), local), encoding="utf-8")


def check(project):
    """Read-only audit. Exit 1 on drift."""
    bad = 0
    man, err = load_json(project / MANIFEST)
    if man is None:
        print(f"manifest: {err} - this project has no kit installation")
        return 1
    print(f"kit {man.get('kit_version')} from {man.get('kit_path')} ({man.get('mode')}), "
          f"installed {man.get('installed_at')}")
    drift, missing = [], []
    for rel, want in man.get("files", {}).items():
        p = project / rel
        if not p.exists():
            missing.append(rel)
        elif sha(p) != want:
            drift.append(rel)
    print(f"manifest: {len(drift)} drifted, {len(missing)} missing")
    for rel in drift + missing:
        print(f"  - {rel}")
    bad += len(drift) + len(missing)

    # behind the kit: installed (as recorded) differs from what the kit ships now
    kit_now = (KIT / "VERSION").read_text().strip()
    behind = [rel for rel, src in kit_sources(project)
              if rel in man.get("files", {}) and not ignored(project, rel)
              and sha(src) != man["files"][rel]]
    new = [rel for rel, src in kit_sources(project)
           if rel not in man.get("files", {}) and not ignored(project, rel)]
    if man.get("mode") == "link":
        print(f"kit: linked, version {kit_now}")
    elif behind or new or man.get("kit_version") != kit_now:
        print(f"kit: BEHIND - installed {man.get('kit_version')}, kit is {kit_now}: "
              f"{len(behind)} changed, {len(new)} new file(s). Run --update.")
        for rel in (behind + new)[:20]:
            print(f"  - {rel}")
        bad += 1
    else:
        print(f"kit: up to date ({kit_now})")

    settings, serr = load_json(project / ".claude" / "settings.json")
    if settings is None:
        print(f"hook: settings.json {serr}")
        bad += 1
    else:
        found = HOOK_MARK in json.dumps(settings)
        print(f"hook: {'present' if found else 'MISSING'}")
        bad += 0 if found else 1

    cfg, cerr = load_json(project / CONFIG)
    if cfg is None:
        print(f"config: {cerr}")
        bad += 1
    else:
        sys.path.insert(0, str(KIT / "kit"))
        import config as kcfg
        loaded = kcfg.load(str(project), quiet=True)
        print(f"config: {len(loaded.unknown)} unknown keys")
        for k in loaded.unknown:
            print(f"  - {k}")
        bad += len(loaded.unknown)

    try:
        v = subprocess.run(["python3", "-V"], capture_output=True, text=True).stdout.strip()
        print(f"python3: {v}")
    except Exception as e:
        print(f"python3: NOT FOUND ({e}) - the SessionStart hook will fail silently")
        bad += 1
    print("\nOK" if not bad else f"\n{bad} problem(s)")
    return 1 if bad else 0


def kit_sources(project):
    """(project-relative destination, kit source) for every kit-owned file."""
    out = [(str(pathlib.Path(".claude/kit") / s.relative_to(KIT / "kit")), s) for s in walk(KIT / "kit")]
    for skill in sorted(p for p in (KIT / "skills").iterdir() if p.is_dir()):
        out += [(str(pathlib.Path(".claude/skills") / skill.name / s.relative_to(skill)), s) for s in walk(skill)]
    out += [(dest, KIT / src) for src, dest in KIT_FILES.items()]
    return out


def ignored(project, rel):
    parts = pathlib.Path(rel).parts
    return len(parts) > 2 and parts[:2] == (".claude", "skills") and \
        (project / ".claude" / "skills" / parts[2] / ".kit-ignore").exists()


def main():
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("project")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--update", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--link", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--seed-topics", default="")
    ap.add_argument("--git-init", action="store_true")
    ap.add_argument("--title", default="")
    ap.add_argument("-h", "--help", action="store_true")
    a = ap.parse_args()
    if a.help:
        print(__doc__)
        return 0

    project = pathlib.Path(a.project).expanduser().resolve()
    if KIT == project or KIT in project.parents:
        sys.exit(f"error: {project} is inside the kit itself")
    if not project.exists():
        if a.dry_run:
            print(f"(dry run: {project} does not exist yet)")
        else:
            sys.exit(f"error: {project} does not exist. Create it first, then re-run.")

    if a.check:
        return check(project)

    dry = a.dry_run
    rep = Report(dry)
    manifest, _ = load_json(project / MANIFEST)
    if a.update and not manifest:
        sys.exit(f"error: --update needs an installation, and {project / MANIFEST} is missing.\n"
                 f"Run without --update for a first install (existing files are kept, "
                 f"new versions land as .kit-new).")
    manifest = manifest or {}
    manifest["_root"] = str(project)
    files = {}

    cfg, _ = load_json(project / CONFIG)
    subs = substitutions(project, cfg, a.title)
    print(f"learning-kit {subs['KIT_VERSION']} -> {project}\n")

    # 1. project files: create if absent, never touched again
    for tpl, dest in PROJECT_FILES.items():
        dst = project / dest
        if dst.exists():
            rep.add("skip (exists)", dst)
            continue
        rep.add("create", dst)
        if not dry:
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_text(fill((KIT / tpl).read_text(encoding="utf-8"), subs), encoding="utf-8")
    if not dry and not cfg:
        cfg, _ = load_json(project / CONFIG)
        subs = substitutions(project, cfg, a.title)

    # 2. the kit module dir, always refreshed
    for src in walk(KIT / "kit"):
        dst = project / ".claude" / "kit" / src.relative_to(KIT / "kit")
        h = copy_kit_file(src, dst, manifest, rep, dry, force=True)
        if h:
            files[str(dst.relative_to(project))] = h

    # 3. skills, one dir at a time
    for skill in sorted((KIT / "skills").iterdir()):
        if not skill.is_dir():
            continue
        dst_dir = project / ".claude" / "skills" / skill.name
        if (dst_dir / ".kit-ignore").exists():
            rep.add("skip (ignored)", dst_dir, ".kit-ignore present")
            continue
        if a.link:
            if dst_dir.is_symlink() or not dst_dir.exists():
                rep.add("link", dst_dir, "-> " + os.path.relpath(skill, dst_dir.parent))
                if not dry:
                    dst_dir.parent.mkdir(parents=True, exist_ok=True)
                    if dst_dir.is_symlink():
                        dst_dir.unlink()
                    dst_dir.symlink_to(os.path.relpath(skill, dst_dir.parent))
            else:
                rep.add("skip (real dir)", dst_dir, "remove it first to link")
            continue
        for src in walk(skill):
            dst = dst_dir / src.relative_to(skill)
            h = copy_kit_file(src, dst, manifest, rep, dry, a.force)
            if h:
                files[str(dst.relative_to(project))] = h

    # 4. kit-owned docs and scripts
    for src_rel, dest in KIT_FILES.items():
        h = copy_kit_file(KIT / src_rel, project / dest, manifest, rep, dry, a.force)
        if h:
            files[str(dest)] = h

    # 5. topics
    for name in [n.strip() for n in a.seed_topics.split(",") if n.strip()]:
        seed_topic(project, name, subs, cfg, rep, dry)
    topics_dir = project / subs["TOPICS_DIR"]
    if not topics_dir.exists():
        rep.add("create", topics_dir)
        if not dry:
            topics_dir.mkdir(parents=True, exist_ok=True)

    # 6. the hook
    ok = merge_settings(project, rep, dry)

    # 7. manifest
    if not dry:
        man = {"kit_version": subs["KIT_VERSION"], "kit_path": str(KIT),
               "kit_commit": git_commit(KIT), "mode": "link" if a.link else "copy",
               "installed_at": dt.datetime.now().isoformat(timespec="seconds"),
               "files": {**manifest.get("files", {}), **files}}
        p = project / MANIFEST
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(man, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # 8. git
    if a.git_init and not (project / ".git").exists():
        rep.add("git init", project, "branch main, no commit")
        if not dry:
            subprocess.run(["git", "init", "-b", "main"], cwd=project, check=False,
                           capture_output=True)

    print(f"\ncreated {rep.count('create')}, updated {rep.count('update')}, "
          f"unchanged {rep.count('unchanged')}, kept-modified {rep.count('MODIFIED keep')}, "
          f"skipped {rep.count('skip (exists)')}")
    if not ok:
        return 2
    print(f"""
Next:
  1. fill in {CONFIG}, PLAN.md and ABOUT-ME.md (the templates mark every blank)
  2. python3 scripts/validate.py --project .
  3. python3 .claude/skills/coach/scripts/brief_context.py today --project .
  4. open Claude Code here: the SessionStart line reports due re-tests""")
    return 0


def git_commit(path):
    """Short HEAD of the kit, with -dirty when its tree has uncommitted changes."""
    try:
        r = subprocess.run(["git", "-C", str(path), "rev-parse", "--short", "HEAD"],
                           capture_output=True, text=True)
        head = r.stdout.strip()
        if not head:
            return None
        d = subprocess.run(["git", "-C", str(path), "status", "--porcelain", "--untracked-files=no"],
                           capture_output=True, text=True)
        return head + ("-dirty" if d.stdout.strip() else "")
    except Exception:
        return None


if __name__ == "__main__":
    sys.exit(main())
