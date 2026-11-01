#!/bin/sh
# Every kit script against the fixture, plus the negative controls and the wiring tests.
# Usage: tests/smoke.sh            (from anywhere)
set -e
KIT=$(cd "$(dirname "$0")/.." && pwd)
FX="$KIT/tests/fixture-project"
SC="${TMPDIR:-/tmp}/kit-smoke-$$"
fail=0
ok()   { printf "  ok    %s\n" "$1"; }
bad()  { printf "  FAIL  %s\n" "$1"; fail=$((fail+1)); }
has()  { echo "$1" | grep -q "$2" && ok "$3" || bad "$3"; }

echo "== fixture"
python3 "$KIT/tests/make_fixture.py" >/dev/null && ok "rebuilt with today's dates"

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

echo
if [ "$fail" = "0" ]; then echo "all smoke tests pass"; else echo "$fail FAILED"; fi
exit "$fail"
