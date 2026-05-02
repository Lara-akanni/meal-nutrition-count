# meal-nutrition-count

## Demo Video

[Watch the demo](#) <!-- Replace # with your video link -->

---

## What the skill does

This skill takes a natural language description of a meal and returns a per-item nutrition breakdown plus a totaled summary. For each food item, it reports calories, protein, carbs, fat, and fiber. If a food is not in the lookup table, it flags it as unknown rather than guessing.

Example input: *"two slices of whole wheat toast, a tablespoon of peanut butter, a medium banana, and black coffee."*

---

## Why I chose it

Nutrition lookup is a task where language models fail in a predictable and measurable way — they hallucinate calorie counts and make arithmetic errors when multiplying across servings. This made it a clear case for offloading the work to a script with a fixed data source. It follows the same shape as the dice-roll example from the assignment: structured input goes in, deterministic numbers come out, and the model handles only the natural language parsing on either end.

---

## How to use it

1. Describe your meal in plain language, including a quantity for each item.
2. The skill parses your description into a structured list of foods and amounts.
3. It calls the lookup script, which checks each item against the food database.
4. You receive a clean nutrition report for the full meal.

If you leave out a quantity for any item, the skill will ask you to specify it before proceeding. It will not assume a serving size.

---

## What the script does

The script (`scripts/nutrition_lookup.py`) receives a structured list of food items and quantities, looks each one up in `assets/foods.csv` (an 80-item database sourced from USDA FoodData Central), multiplies the per-unit nutrition values by the quantity provided, and sums everything into a total row. Foods not found in the CSV are collected and returned as unknown — no values are estimated or filled in.

---

## What worked well

- Separating the language parsing (handled by the model) from the arithmetic and lookup (handled by the script) kept each part clean and testable.
- Using a fixed CSV with USDA-sourced values means the numbers are consistent and verifiable — no variation between runs.
- The unknown-item flag path works naturally for edge cases like uncommon foods, giving useful feedback instead of silent errors.

---

## Limitations that remain

- Only the 80 foods in the bundled CSV are supported. Users asking about less common foods will hit the unknown-item path frequently.
- Protein entries are listed per 100g, which works well for people who weigh food but is less intuitive for casual users who think in "one chicken breast."
- The skill cannot handle compound dishes (e.g. "homemade lasagna") or brand-specific items where nutrition varies by source.
- Portion sizes must always be user-supplied — the skill has no fallback defaults.

---

## Project Structure

```
hw5-RofiahAkanni/
├─ .agents/
│  └─ skills/
│     └─ meal-nutrition-count/
│        ├─ SKILL.md
│        ├─ scripts/
│        │  └─ nutrition_lookup.py
│        ├─ assets/
│        │  └─ foods.csv
│        └─ references/
│           └─ data-sources.md
└─ README.md
```
