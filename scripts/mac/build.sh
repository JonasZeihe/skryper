#!/usr/bin/env bash
# (C) 2025 Jonas Zeihe, MIT License. Developer: Jonas Zeihe. Contact: JonasZeihe@gmail.com

set -e
cd "$(dirname "$0")"
cd ../../
python scripts/logic/build_app.py
echo "Build done."
read -n 1 -s
