#!/bin/sh
# Every kit script against the fixture, plus the negative controls and the wiring tests.
# Usage: sh tests/smoke.sh         (from anywhere)
# Runs against a temp copy of tests/fixture-project, so the tracked fixture stays clean.
set -e
KIT=$(cd "$(dirname "$0")/.." && pwd)
SC="${TMPDIR:-/tmp}/kit-smoke-$$"
FX="${TMPDIR:-/tmp}/kit-fixture-$$"
rm -rf "$FX"; cp -R "$KIT/tests/fixture-project" "$FX"
trap 'rm -rf "$FX" "$SC"' EXIT
unset CLAUDE_PROJECT_DIR LEARNING_PROJECT_ROOT
fail=0
ok()   { printf "  ok    %s\n" "$1"; }
bad()  { printf "  FAIL  %s\n" "$1"; fail=$((fail+1)); }
has()  { echo "$1" | grep -q "$2" && ok "$3" || bad "$3"; }

echo "== fixture"
python3 "$KIT/tests/make_fixture.py" "$FX" >/dev/null && ok "rebuilt with today's dates (temp copy)"
v=$(cat "$KIT/VERSION"); dv=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))['kit_version'])" "$KIT/kit/defaults.json")
[ "$v" = "$dv" ] && ok "defaults.json kit_version matches VERSION" || bad "defaults.json kit_version $dv != VERSION $v"

echo "== kit modules"
python3 - "$KIT" <<'PY' && ok "dates + mdtable assertions"
import sys, datetime as dt
sys.path.insert(0, sys.argv[1] + "/kit")
import dates, mdtable
M = {"pass": "✓", "shaky": "shaky", "fail": "fail"}; L = [2, 7, 16, 35, 90]
assert dates.week_of(dt.date(2026,11,1), "2026-11-02") == 0
assert dates.week_of(dt.date(2026,11,9), "2026-11-02") == 2
p, q = dates.split_retest("✓2026-10-20, +7d 2026-10-25", M)
assert p == [dt.date(2026,10,25)] and q == [dt.date(2026,10,20)]
assert dates.next_rung("✓2026-10-20, +7d 2026-10-25", M, L, dt.date(2026,10,25), "pass")[1] == "+16d"
assert dates.first_rung(dt.date(2026,11,2), L) == "2026-11-04, +7d 2026-11-09"
assert mdtable.split_row("| a \\| b | c |") == ["a \\| b", "c"]
# a fail drops the row back to the first rung (principles 1.6)
T = dt.date(2026,11,20)
cell = "✓2026-10-20, ✓2026-10-27, fail 2026-11-12, +1d 2026-11-13, ✓2026-11-13, +7d 2026-11-20"
assert dates.passes_since_fail(cell, M) == 1
assert dates.next_rung(cell, M, L, T, "pass")[1] == "+16d", dates.next_rung(cell, M, L, T, "pass")
assert dates.next_rung("✓2026-10-20, ✓2026-10-27, ✓2026-11-03", M, L, T, "pass")[1] == "+90d"
assert dates.next_rung("2026-11-20", M, L, T, "fail")[0] == "fail2026-11-20, +1d 2026-11-21"
PY

echo "== append_row"
out=$(python3 "$KIT/skills/session-log/scripts/append_row.py" "$FX/topics/alpha/error-log.md" --check)
has "$out" "profile=error_log" "error-log profile detected"
out=$(python3 "$KIT/skills/session-log/scripts/append_row.py" "$FX/topics/alpha/patterns.md" --check)
has "$out" "profile=patterns" "patterns profile detected"
if python3 "$KIT/skills/session-log/scripts/append_row.py" "$FX/topics/alpha/error-log.md" \
     2026-01-06 Q A C typo drill "2026-01-08" >/dev/null 2>&1; then
  bad "bad Cause rejected"
else
  ok "bad Cause rejected, nothing written"
fi
AR="$KIT/skills/session-log/scripts/append_row.py"
# write tests run on a copy under a skip-prefixed folder, so validate still sees a clean fixture
mkdir -p "$FX/topics/_scratch"; cp "$FX/topics/alpha/error-log.md" "$FX/topics/_scratch/error-log.md"
EL="$FX/topics/_scratch/error-log.md"
printf '\n## Parking lot\n\n- parked idea\n' >> "$EL"
before=$(grep -c '^|' "$EL")
out=$(python3 "$AR" "$EL" 2026-01-06 "Smoke question one" A C concept drill "2026-01-08")
has "$out" "ok: appended" "append_row appends a valid row"
[ "$(grep -c '^|' "$EL")" = "$((before+1))" ] && ok "exactly one row added" || bad "exactly one row added"
tail -1 "$EL" | grep -q "parked idea" && ok "Parking lot stays below the table" || bad "Parking lot stays below the table"
out=$(python3 "$AR" "$EL" 2026-01-06 "smoke QUESTION one" A C concept drill "2026-01-08")
has "$out" "skip" "duplicate (Date + Question, any case) skipped"
out=$(python3 "$AR" "$EL" --retest "Smoke question one" pass --today 2026-01-08)
has "$out" "+7d" "--retest pass climbs the ladder"
grep -q "✓2026-01-08, +7d 2026-01-15" "$EL" && ok "--retest wrote only the Re-test cell" || bad "--retest cell"
out=$(python3 "$AR" "$EL" --retest "Smoke question one" fail --today 2026-01-15)
has "$out" "+1d" "--retest fail"
out=$(python3 "$AR" "$EL" --retest "Smoke question one" pass --today 2026-01-16)
has "$out" "+7d" "pass after a fail restarts at the first rung"
if python3 "$AR" "$EL" --retest "zzz-no-such-row" pass >/dev/null 2>&1; then bad "--retest no match exits 2"; else ok "--retest no match exits 2"; fi
python3 "$AR" "$FX/topics/_scratch/patterns.md" --init >/dev/null && grep -q "^| Trigger" "$FX/topics/_scratch/patterns.md" \
  && ok "--init creates a table file with its header" || bad "--init"

echo "== root lookup"
NC="${TMPDIR:-/tmp}/kit-noconfig-$$"; mkdir -p "$NC"
if (cd "$NC" && python3 "$KIT/skills/active-revise/scripts/due_reviews.py" >/dev/null 2>&1); then
  bad "no config anywhere exits non-zero"
else
  ok "no config anywhere exits non-zero"
fi
if python3 "$KIT/skills/active-revise/scripts/due_reviews.py" --project "$NC" >/dev/null 2>&1; then
  bad "--project without config exits non-zero"
else
  ok "--project without config exits non-zero"
fi
out=$(cd "$FX/topics" && CLAUDE_PROJECT_DIR="$NC" python3 "$KIT/skills/active-revise/scripts/due_reviews.py" --summary 2>&1)
has "$out" "Re-tests as of" "CLAUDE_PROJECT_DIR without config falls through to the walk-up"
rm -rf "$NC"

echo "== nested layouts"
NL="${TMPDIR:-/tmp}/kit-nested-$$"; mkdir -p "$NL/grammar/learning-records" "$NL/_skip/x" "$NL/topics/L0/js"
printf '{"paths": {"topics_dir": "."}}\n' > "$NL/learning.config.json"
hdr='| Date | Question | My answer | Correct | Cause | Fix drill | Re-test |\n|---|---|---|---|---|---|---|\n'
printf "# g\n\n$hdr| 2026-01-01 | nested q | a | c | concept | d | 2026-01-03 |\n" > "$NL/grammar/learning-records/error-log.md"
printf "# s\n\n$hdr| 2026-01-01 | skipped q | a | c | concept | d | 2026-01-03 |\n" > "$NL/_skip/x/error-log.md"
printf "# js\n\n$hdr| 2026-01-01 | grouped q | a | c | concept | d | 2026-01-03 |\n" > "$NL/topics/L0/js/error-log.md"
printf "| State | active |\n" > "$NL/topics/L0/js/TOPIC.md"
out=$(python3 "$KIT/skills/active-revise/scripts/due_reviews.py" --project "$NL" --summary)
has "$out" "grammar" "topics_dir '.' + nested learning-records -> topic 'grammar'"
has "$out" "js" "grouped layout -> nearest TOPIC.md folder 'js'"
if echo "$out" | grep -qE "learning-records|_skip|L0"; then bad "no record/skip/group folder named as a topic"; else ok "no record/skip/group folder named as a topic"; fi
rm -rf "$NL"

echo "== due_reviews"
out=$(python3 "$KIT/skills/active-revise/scripts/due_reviews.py" --project "$FX")
has "$out" "DUE" "due rows listed"
has "$out" "COLD pool" "cold pool listed"
sum=$(python3 "$KIT/skills/active-revise/scripts/due_reviews.py" --project "$FX" --summary)
has "$sum" "Re-tests as of" "summary line"
if echo "$sum" | grep -q "Correct"; then bad "summary withholds answers"; else ok "summary withholds answers"; fi

echo "== collect_errors / status_derive / brief_context"
out=$(python3 "$KIT/skills/error-diagnose/scripts/collect_errors.py" --project "$FX" --days 14)
has "$out" "By cause:" "cause histogram"
out=$(python3 "$KIT/skills/coach/scripts/status_derive.py" --project "$FX")
has "$out" "DRIFT" "drift section"
has "$out" "none: STATUS.md matches" "fixture has no drift"
for m in today status weekly; do
  out=$(python3 "$KIT/skills/coach/scripts/brief_context.py" "$m" --project "$FX")
  if echo "$out" | grep -qE "Traceback|failed:"; then bad "brief_context $m"; else ok "brief_context $m"; fi
done
out=$(python3 "$KIT/skills/coach/scripts/brief_context.py" topic alpha --project "$FX")
has "$out" "topics/alpha/TOPIC.md" "brief_context topic"

echo "== validate"
out=$(python3 "$KIT/scripts/validate.py" --project "$FX")
has "$out" "0 errors, 0 warnings" "fixture is clean"
cp "$FX/topics/beta/error-log.md" "$FX/topics/beta/error-log.md.bak"
sed -i.tmp 's/| 20[0-9][0-9]-[0-9][0-9]-[0-9][0-9] |$/| soon |/' "$FX/topics/beta/error-log.md"
if python3 "$KIT/scripts/validate.py" --project "$FX" >/dev/null; then
  bad "negative: Re-test with no date"
else
  ok "negative: Re-test with no date exits 1"
fi
mv "$FX/topics/beta/error-log.md.bak" "$FX/topics/beta/error-log.md"; rm -f "$FX"/topics/beta/*.tmp
cp "$FX/topics/beta/TOPIC.md" "$FX/topics/beta/TOPIC.md.bak"
sed -i.tmp 's/| State | locked |/| State | active |/' "$FX/topics/beta/TOPIC.md"
if python3 "$KIT/scripts/validate.py" --project "$FX" >/dev/null; then
  bad "negative: prerequisite not passed"
else
  ok "negative: prerequisite not passed exits 1"
fi
mv "$FX/topics/beta/TOPIC.md.bak" "$FX/topics/beta/TOPIC.md"; rm -f "$FX"/topics/beta/*.tmp

echo "== lesson style"
CL="$KIT/skills/create-lesson/assets"
for s in skeleton-lesson skeleton-reference; do
  grep -q 'data-theme="light"' "$CL/$s.html" && ok "$s opens light" || bad "$s opens light"
done
# every dark-scheme media query must guard against an explicit light page
unguarded=$(awk '/prefers-color-scheme: *dark/{getline n; if (n !~ /not\(\[data-theme="light"\]\)/) print NR}' "$CL/lesson.css")
[ -z "$unguarded" ] && ok "lesson.css dark is opt-in only" || bad "lesson.css unguarded dark at line $unguarded"

echo "== wiring"
rm -rf "$SC"; mkdir -p "$SC"
python3 "$KIT/init_project.py" "$SC" --dry-run --title smoke >/dev/null
[ "$(find "$SC" | wc -l | tr -d ' ')" = "1" ] && ok "dry run writes nothing" || bad "dry run writes nothing"
python3 "$KIT/init_project.py" "$SC" --title smoke --seed-topics one >/dev/null
python3 "$KIT/init_project.py" "$SC" --check >/dev/null && ok "check is clean after install" || bad "check after install"
out=$(python3 "$KIT/init_project.py" "$SC" --title smoke)
has "$out" "created 0, updated 0" "re-run is idempotent"
echo "# local" >> "$SC/.claude/skills/teach/SKILL.md"
out=$(python3 "$KIT/init_project.py" "$SC" --update)
has "$out" "MODIFIED keep" "local edit kept, .kit-new written"
[ -f "$SC/.claude/skills/teach/SKILL.md.kit-new" ] && ok ".kit-new present" || bad ".kit-new present"
printf '{ "hooks": { oops' > "$SC/.claude/settings.json"
if python3 "$KIT/init_project.py" "$SC" >/dev/null 2>&1; then
  bad "malformed settings.json exits 2"
else
  ok "malformed settings.json exits 2, nothing written"
fi
grep -q "oops" "$SC/.claude/settings.json" && ok "malformed settings.json untouched" || bad "settings untouched"
rm -rf "$SC"

echo "== installer: first install, --update, --check behind"
mkdir -p "$SC/.claude/skills/teach"
echo "# hand-made copy" > "$SC/.claude/skills/teach/SKILL.md"
if python3 "$KIT/init_project.py" "$SC" --update --title smoke >/dev/null 2>&1; then
  bad "--update without a manifest refuses"
else
  ok "--update without a manifest refuses"
fi
python3 "$KIT/init_project.py" "$SC" --title smoke >/dev/null
grep -q "hand-made copy" "$SC/.claude/skills/teach/SKILL.md" && ok "first install keeps an existing file" || bad "first install overwrote an existing file"
[ -f "$SC/.claude/skills/teach/SKILL.md.kit-new" ] && ok "first install writes .kit-new beside it" || bad "first install .kit-new"
out=$(python3 "$KIT/init_project.py" "$SC" --check || true)
has "$out" "BEHIND" "--check reports a kept file as behind the kit"
rm -rf "$SC"; mkdir -p "$SC"
python3 "$KIT/init_project.py" "$SC" --title smoke >/dev/null
out=$(python3 "$KIT/init_project.py" "$SC" --check)
has "$out" "up to date" "--check up to date after a clean install"
# simulate an older install: the file and its recorded hash both differ from the kit's file
echo "# older kit text" >> "$SC/.claude/skills/teach/SKILL.md"
python3 - "$SC" <<'PY'
import hashlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1]); p = root / ".claude/.kit-manifest.json"; m = json.loads(p.read_text())
k = next(k for k in m["files"] if k.endswith("teach/SKILL.md"))
m["files"][k] = hashlib.sha256((root / k).read_bytes()).hexdigest()
p.write_text(json.dumps(m))
PY
out=$(python3 "$KIT/init_project.py" "$SC" --check || true)
has "$out" "BEHIND" "--check reports an older installed file as behind"
if echo "$out" | grep -q "1 drifted"; then bad "older file is not local drift"; else ok "older file is not local drift"; fi
touch "$SC/.claude/skills/teach/.kit-ignore"
out=$(python3 "$KIT/init_project.py" "$SC" --check)
has "$out" "up to date" "--check skips a .kit-ignore skill"
rm -rf "$SC"

echo
if [ "$fail" = "0" ]; then echo "all smoke tests pass"; else echo "$fail FAILED"; fi
exit "$fail"
