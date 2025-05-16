#!/usr/bin/env python3
import os
import sys
import datetime

# === Setup ===
base_path = os.path.abspath(os.path.dirname(__file__))
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

default_output = os.path.join(base_path, f"{timestamp}_output.txt")
default_log = os.path.join(base_path, f"{timestamp}_combine_log.txt")
search_path = os.path.abspath(os.path.join(base_path, "..", ".."))

# Optional arguments
if len(sys.argv) >= 2:
    suffix = sys.argv[1].strip()
    output_file = os.path.join(base_path, f"{timestamp}_{suffix}")
else:
    output_file = default_output

if len(sys.argv) >= 3:
    search_path = os.path.abspath(sys.argv[2])

log_file = default_log

# === Start log ===
with open(log_file, "w", encoding="utf-8") as log:
    log.write(f"Log start: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    log.write(f"Search path: {search_path}\n")

# === Validate directory ===
if not os.path.isdir(search_path):
    with open(log_file, "a", encoding="utf-8") as log:
        log.write(f'ERROR: Directory "{search_path}" does not exist.\n')
    print(f'ERROR: Directory "{search_path}" does not exist.')
    sys.exit(1)

# === Init output ===
with open(output_file, "w", encoding="utf-8") as out:
    out.write("Merged Python source files\n")
    out.write("=" * 30 + "\n\n")

# === File scanning ===
file_count = 0

for root, dirs, files in os.walk(search_path):
    for file in files:
        if file.endswith(".py"):
            file_path = os.path.join(root, file)
            with open(log_file, "a", encoding="utf-8") as log:
                log.write(f"Processing file: {file_path}\n")
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                with open(output_file, "a", encoding="utf-8") as out:
                    out.write(f"----- {file_path} -----\n")
                    out.write(content)
                    out.write("\n" + "=" * 30 + "\n\n")
                file_count += 1
            except Exception as e:
                with open(log_file, "a", encoding="utf-8") as log:
                    log.write(f"ERROR reading {file_path}: {e}\n")

# === Summary ===
with open(log_file, "a", encoding="utf-8") as log:
    if file_count > 0:
        log.write(f"SUCCESS: {file_count} Python files processed.\n")
        print(f"✅ {file_count} Python files processed.")
        print(f"Output written to: {output_file}")
        print(f"Log saved to: {log_file}")
    else:
        log.write(f'WARNING: No Python files found in "{search_path}".\n')
        print(f"⚠️ No Python files found in: {search_path}")

    log.write(f"Log end: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
