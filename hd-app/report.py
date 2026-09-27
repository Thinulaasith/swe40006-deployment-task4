import csv
import sys
from pathlib import Path

input_file = Path("/data/tasks.csv")
output_file = Path("/data/summary.txt")

try:
    with input_file.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if not {"task", "minutes"}.issubset(reader.fieldnames or []):
            raise ValueError("CSV must contain task and minutes columns")

        tasks = []
        for row in reader:
            minutes = int(row["minutes"])
            if minutes < 0:
                raise ValueError("Minutes cannot be negative")
            tasks.append((row["task"], minutes))

    if not tasks:
        raise ValueError("CSV contains no tasks")

    total = sum(minutes for _, minutes in tasks)
    lines = ["STUDY TIME SUMMARY", "=================="]
    lines.extend(f"{task}: {minutes} minutes" for task, minutes in tasks)
    lines.extend(["", f"Number of tasks: {len(tasks)}", f"Total study time: {total} minutes"])
    report = "\n".join(lines) + "\n"

    output_file.write_text(report, encoding="utf-8")
    print(report, end="")
    print(f"Report saved to {output_file}")

except (OSError, ValueError, KeyError) as error:
    print(f"Report failed: {error}", file=sys.stderr)
    sys.exit(1)
