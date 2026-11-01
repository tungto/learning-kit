#!/bin/sh
# Thin wrapper: learning-kit/bin/init-project.sh <project-dir> [flags]
exec python3 "$(dirname "$0")/../init_project.py" "$@"
