#!/usr/bin/env python3
"""
nutrition_lookup.py

Looks up nutrition values for a list of food items and quantities,
then prints a formatted per-item breakdown and meal total.

Usage:
    python nutrition_lookup.py '<JSON>'

Input JSON format:
    [
        {"food": "egg", "qty": 2, "unit": "large"},
        {"food": "whole wheat bread", "qty": 2, "unit": "slice"},
        {"food": "peanut butter", "qty": 1, "unit": "tablespoon"}
    ]

The script exits with code 1 if the input is missing or malformed.
"""

import csv
import json
import sys
from pathlib import Path

CSV_PATH = Path(__file__).parent.parent / "assets" / "foods.csv"

NUTRIENTS = ["calories", "protein_g", "carbs_g", "fat_g", "fiber_g"]
HEADERS   = ["calories", "protein", "carbs", "fat", "fiber"]


def load_database(csv_path: Path) -> dict:
    db = {}
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = row["food_name"].strip().lower()
            db[key] = {
                "serving": row["serving_description"].strip(),
                "calories":   float(row["calories"]),
                "protein_g":  float(row["protein_g"]),
                "carbs_g":    float(row["carbs_g"]),
                "fat_g":      float(row["fat_g"]),
                "fiber_g":    float(row["fiber_g"]),
            }
    return db


def lookup(items: list, db: dict) -> tuple:
    found, unknown = [], []
    for item in items:
        key = item["food"].strip().lower()
        qty = float(item.get("qty", 1))
        if key not in db:
            unknown.append(item["food"])
            continue
        entry = db[key]
        found.append({
            "name":    item["food"],
            "qty":     qty,
            "serving": entry["serving"],
            **{n: round(entry[n] * qty, 1) for n in NUTRIENTS},
        })
    return found, unknown


def format_report(found: list, unknown: list) -> str:
    col_widths = [28, 6, 10, 9, 7, 7, 7]
    header_row = ["Item", "Qty"] + HEADERS
    divider = "  ".join("-" * w for w in col_widths)

    def row(cells):
        return "  ".join(str(c).ljust(col_widths[i]) for i, c in enumerate(cells))

    lines = [row(header_row), divider]

    totals = {n: 0.0 for n in NUTRIENTS}

    for f in found:
        lines.append(row([
            f["name"],
            f["qty"],
            f"{f['calories']} kcal",
            f"{f['protein_g']}g",
            f"{f['carbs_g']}g",
            f"{f['fat_g']}g",
            f"{f['fiber_g']}g",
        ]))
        for n in NUTRIENTS:
            totals[n] += f[n]

    lines.append(divider)
    lines.append(row([
        "TOTAL", "",
        f"{round(totals['calories'], 1)} kcal",
        f"{round(totals['protein_g'], 1)}g",
        f"{round(totals['carbs_g'], 1)}g",
        f"{round(totals['fat_g'], 1)}g",
        f"{round(totals['fiber_g'], 1)}g",
    ]))

    if unknown:
        lines.append("")
        lines.append("Unknown items (not in database): " + ", ".join(unknown))
    else:
        lines.append("")
        lines.append("Unknown items (not in database): none")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("Error: no input provided.\nUsage: python nutrition_lookup.py '<JSON>'", file=sys.stderr)
        sys.exit(1)

    try:
        items = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"Error: invalid JSON — {e}", file=sys.stderr)
        sys.exit(1)

    if not isinstance(items, list) or not items:
        print("Error: input must be a non-empty JSON array of food items.", file=sys.stderr)
        sys.exit(1)

    if not CSV_PATH.exists():
        print(f"Error: food database not found at {CSV_PATH}", file=sys.stderr)
        sys.exit(1)

    db = load_database(CSV_PATH)
    found, unknown = lookup(items, db)

    if not found and unknown:
        print("None of the requested foods were found in the database.")
        print("Unknown items: " + ", ".join(unknown))
        sys.exit(0)

    print(format_report(found, unknown))


if __name__ == "__main__":
    main()
