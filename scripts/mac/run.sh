#!/usr/bin/env bash
# (C) 2025 Jonas Zeihe, MIT License. Developer: Jonas Zeihe. Contact: JonasZeihe@gmail.com

set -e
cd "$(dirname "$0")"
cd ../../
if [ ! -f "venv/bin/activate" ]; then
  echo "No virtual environment found."
  read -n 1 -s
  exit 1
fi
source venv/bin/activate
python scripts/logic/run_logic.py "$@"
echo "Done."
read -n 1 -s
deactivate
