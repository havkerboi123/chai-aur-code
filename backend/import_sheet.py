"""Import project submissions from a published Google Sheet into the local DB.

Usage:
    python import_sheet.py "<google sheet url>"

Accepts either a normal Google Sheets share URL (https://docs.google.com/spreadsheets/d/<ID>/edit...)
or a direct CSV export URL. Column headers are matched loosely (case-insensitive,
substring match) so it's fine if the Google Form's exact wording differs a bit.
"""

import csv
import io
import re
import sys

import requests

from db import get_connection, init_db

COLUMN_MATCHERS = {
    "name": ["project name", "project title", "title"],
    "description": ["description", "about", "what does it do", "summary"],
    "github_url": ["github", "repo", "repository", "source code"],
    "deployed_url": ["deployed", "live link", "live url", "demo", "hosted"],
    "submitter": ["full name", "your name", "submitted by", "team"],
}


def sheet_url_to_csv(url: str) -> str:
    if "/export?format=csv" in url or "output=csv" in url:
        return url
    match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", url)
    if not match:
        raise ValueError("Could not find a spreadsheet ID in that URL.")
    sheet_id = match.group(1)
    gid_match = re.search(r"[?&#]gid=(\d+)", url)
    gid = gid_match.group(1) if gid_match else "0"
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"


def match_column(headers: list[str], keys: list[str]) -> str | None:
    lower_headers = {h.lower().strip(): h for h in headers}
    for key in keys:
        for lower_h, original in lower_headers.items():
            if key in lower_h:
                return original
    return None


def import_from_sheet(url: str) -> int:
    csv_url = sheet_url_to_csv(url)
    resp = requests.get(csv_url, timeout=15)
    resp.raise_for_status()

    reader = csv.DictReader(io.StringIO(resp.text))
    headers = reader.fieldnames or []

    col_map = {field: match_column(headers, keys) for field, keys in COLUMN_MATCHERS.items()}
    if not col_map["name"] or not col_map["description"] or not col_map["github_url"]:
        raise ValueError(
            f"Couldn't find required columns (name/description/github link) in headers: {headers}"
        )

    init_db()
    conn = get_connection()
    count = 0
    for row in reader:
        name = (row.get(col_map["name"]) or "").strip()
        description = (row.get(col_map["description"]) or "").strip()
        github_url = (row.get(col_map["github_url"]) or "").strip()
        deployed_url = (row.get(col_map["deployed_url"]) or "").strip() if col_map["deployed_url"] else ""
        submitter = (row.get(col_map["submitter"]) or "").strip() if col_map["submitter"] else ""

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
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    imported = import_from_sheet(sys.argv[1])
    print(f"Imported {imported} projects.")
