#!/usr/bin/env python3
"""Project config: find the project root, load learning.config.json over the kit defaults.

Root resolution order (never from __file__, which breaks under symlinks and
hardcodes how deep a skill script sits):

  1. an explicit path passed in (--project on a CLI): it must hold
     learning.config.json, or this is an error (never a silent fallback)
  2. $LEARNING_PROJECT_ROOT, then $CLAUDE_PROJECT_DIR, each used only if it
     holds learning.config.json (Claude Code is often opened one level above
     the project, where these point at a folder with no config)
  3. walk up from the current directory until learning.config.json is found

No config anywhere is an error. Loading the bare kit defaults would silently
change causes, ladders and paths, so a script stops instead.

Missing keys come from the kit defaults; unknown keys in the project file are
reported on stderr and otherwise ignored, so a typo degrades to a default
instead of crashing a session.
"""
import json
import os
import pathlib
import sys

CONFIG_NAME = "learning.config.json"
DEFAULTS_NAME = "defaults.json"


class ConfigError(Exception):
    pass


def _defaults_path():
    """defaults.json sits next to this file, in the kit or in <project>/.claude/kit/."""
    return pathlib.Path(__file__).resolve().parent / DEFAULTS_NAME


def walk_up(start):
    """The nearest folder at or above start that holds learning.config.json, or None."""
    here = pathlib.Path(start).expanduser().resolve()
    if here.is_file():
        here = here.parent
    for p in [here, *here.parents]:
        if (p / CONFIG_NAME).is_file():
            return p
    return None


def find_root(project=None):
    if project:
        p = pathlib.Path(project).expanduser().resolve()
        if (p / CONFIG_NAME).is_file():
            return p
        raise ConfigError(f"--project {p} has no {CONFIG_NAME}")
    for cand in (os.environ.get("LEARNING_PROJECT_ROOT"), os.environ.get("CLAUDE_PROJECT_DIR")):
        if cand:
            p = pathlib.Path(cand).expanduser().resolve()
            if (p / CONFIG_NAME).is_file():
                return p
    found = walk_up(pathlib.Path.cwd())
    if found:
        return found
    raise ConfigError(
        f"no {CONFIG_NAME} found. Pass --project <dir>, set $LEARNING_PROJECT_ROOT, "
        f"or run from inside a project."
    )


def _merge(base, over, path="", unknown=None):
    """Recursive dict merge. Lists and scalars are replaced, not merged."""
    out = dict(base)
    for k, v in over.items():
        full = f"{path}.{k}" if path else k
        if k not in base:
            if unknown is not None:
                unknown.append(full)
            out[k] = v
        elif isinstance(v, dict) and isinstance(base[k], dict):
            out[k] = _merge(base[k], v, full, unknown)
        else:
            out[k] = v
    return out


class Config:
    def __init__(self, root, data, unknown=()):
        self.root = pathlib.Path(root)
        self.data = data
        self.unknown = list(unknown)

    def get(self, dotted, default=None):
        """config.get('plan.start_date'). Raises on a key absent from the defaults."""
        cur = self.data
        for part in dotted.split("."):
            if not isinstance(cur, dict) or part not in cur:
                if default is not None:
                    return default
                raise ConfigError(f"unknown config key '{dotted}' (not in {DEFAULTS_NAME})")
            cur = cur[part]
        return cur

    def path(self, dotted):
        """A path key resolved against the project root."""
        return self.root / str(self.get(dotted))

    def table(self, name):
        """Column list for a table profile: error_log / glossary / patterns."""
        return list(self.get(f"layout.tables.{name}"))

    def file_name(self, name):
        return str(self.get(f"layout.files.{name}"))

    def topics_dir(self):
        return self.path("paths.topics_dir")

    def skip_prefix(self):
        return str(self.get("paths.skip_prefix"))

    def topic_of(self, path, topics_dir=None):
        """Topic name for a file under the topics dir, whatever its depth.

        The nearest folder above the file that holds the topic file (TOPIC.md)
        wins, so grouped layouts (topics/L0/js/error-log.md -> js) and nested
        records (grammar/learning-records/error-log.md -> grammar) both work.
        Without a topic file, the first folder under the topics dir is the topic.
        """
        topics = pathlib.Path(topics_dir or self.topics_dir()).resolve()
        path = pathlib.Path(path).resolve()
        topic_file = self.file_name("topic")
        for folder in path.parents:
            if folder == topics or topics not in folder.parents:
                break
            if (folder / topic_file).is_file():
                return folder.name
        try:
            parts = path.relative_to(topics).parts
        except ValueError:
            return path.parent.name
        return parts[0] if len(parts) > 1 else topics.name

    def skipped(self, path, topics_dir=None):
        """True for files under a skip-prefixed or hidden folder of the topics dir."""
        topics = pathlib.Path(topics_dir or self.topics_dir()).resolve()
        try:
            parts = pathlib.Path(path).resolve().relative_to(topics).parts[:-1]
        except ValueError:
            return False
        return any(p.startswith((self.skip_prefix(), ".")) for p in parts)

    def profile_for(self, header):
        """Which table profile a header row belongs to, or None."""
        norm = [h.strip().lower() for h in header]
        for name in self.get("layout.tables"):
            cols = [c.strip().lower() for c in self.table(name)]
            if norm == cols:
                return name
        # tolerate a renamed or extra column: match on the first column
        for name in self.get("layout.tables"):
            cols = [c.strip().lower() for c in self.table(name)]
            if norm and cols and norm[0] == cols[0]:
                return name
        return None


def load(project=None, quiet=False):
    root = find_root(project)
    with open(_defaults_path(), encoding="utf-8") as f:
        base = json.load(f)
    cfg_file = root / CONFIG_NAME
    unknown = []
    if cfg_file.is_file():
        with open(cfg_file, encoding="utf-8") as f:
            try:
                over = json.load(f)
            except json.JSONDecodeError as e:
                raise ConfigError(f"{cfg_file} is not valid JSON: {e}")
        data = _merge(base, over, "", unknown)
    else:
        data = base
    if unknown and not quiet:
        for k in unknown:
            print(f"warning: unknown config key '{k}' in {cfg_file} (ignored)", file=sys.stderr)
    return Config(root, data, unknown)


def add_args(ap):
    """Standard --project / --root flags for every kit script."""
    ap.add_argument("--project", default=None, help="project root (holds learning.config.json)")
    ap.add_argument("--root", default=None, help="override the topics dir for this run")
    return ap


def from_args(a):
    cfg = load_or_exit(getattr(a, "project", None))
    root_override = getattr(a, "root", None)
    topics = pathlib.Path(root_override).expanduser() if root_override else cfg.topics_dir()
    return cfg, topics


def load_or_exit(project=None, quiet=False):
    """load() for CLI scripts: a missing or broken config exits 2 with the reason."""
    try:
        return load(project, quiet)
    except ConfigError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(2)


def main():
    import argparse
    ap = argparse.ArgumentParser(description="print resolved config values")
    add_args(ap)
    ap.add_argument("keys", nargs="*", default=[])
    a = ap.parse_args()
    cfg = load_or_exit(a.project)
    print(f"root: {cfg.root}")
    print(f"topics: {cfg.topics_dir()}")
    for k in a.keys:
        print(f"{k}: {cfg.get(k)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
