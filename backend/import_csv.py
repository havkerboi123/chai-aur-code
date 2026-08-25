"""Import Chai aur Code Episode 1 submissions from the Google Forms CSV export.

Usage:
    python import_csv.py [path/to/csv]

Defaults to data/chai_aur_code_ep1_submissions.csv. Clears any existing
Episode 1 rows first, then loads everything from the CSV fresh.
"""

import csv
import sys
from pathlib import Path

from db import get_connection, init_db

DEFAULT_CSV = Path(__file__).parent / "data" / "chai_aur_code_ep1_submissions.csv"


def import_csv(path: Path) -> int:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    init_db()
    conn = get_connection()
    conn.execute("DELETE FROM projects WHERE episode = 'Episode 1'")

    count = 0
    for row in rows:
        name = (row.get("Project Name") or "").strip()
        description = (row.get("Project Description") or "").strip()
        github_url = (row.get("Github Repo") or "").strip()
        deployed_url = (row.get("Deployed Link") or "").strip()
        submitter = (row.get("Full Name") or "").strip()

        if not name or not github_url:
            continue

        conn.execute(
            """
            INSERT INTO projects (name, description, github_url, deployed_url, submitter, episode)
            VALUES (?, ?, ?, ?, ?, 'Episode 1')
            """,
            (name, description, github_url, deployed_url, submitter),
        )
        count += 1

    conn.commit()
    conn.close()
    return count


if __name__ == "__main__":
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CSV
    imported = import_csv(csv_path)
    print(f"Imported {imported} projects from {csv_path.name}")
