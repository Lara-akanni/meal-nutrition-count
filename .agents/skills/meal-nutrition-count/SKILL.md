---
name: meal-nutrition-count
description: Looks up calories and macronutrients (protein, carbs, fat, fiber) for a meal described in plain language. Returns a per-item breakdown and a totaled summary using a fixed CSV lookup table so numbers are always accurate and never hallucinated. Use when the user describes a meal and wants to know its nutritional content.
---

## When to use this skill

Use this skill when the user describes a meal or list of foods in natural language and wants a calorie and macronutrient breakdown — per item and as a total.

Examples:
- "What are the macros for two slices of whole wheat toast, a tablespoon of peanut butter, a medium banana, and black coffee?"
- "How many calories in my lunch: grilled chicken, brown rice, and a salad?"

## When NOT to use this skill

Do not use this skill when the user wants to:
- Track meals across multiple days
- Set or compare against daily nutrition goals
- Get food or diet suggestions
- Receive a health judgement on their meal
- Calculate nutrition for raw recipe ingredients
- Get nutrition for a vaguely described food without a quantity — ask for the quantity first instead of assuming a serving size

## Expected inputs

A natural language meal description that includes:
- Each food item in the meal
- A quantity for each item (e.g. "two slices", "1 tablespoon", "a medium banana")

If a quantity is missing for any item, ask the user to specify it before running the script. Do not assume or estimate portion sizes.

## Step-by-step instructions

1. Parse the user's meal description and extract a structured list of food items with their quantities.
2. Normalize each food name to match entries in the skill's CSV lookup table (e.g. "whole wheat toast" → "whole_wheat_toast").
3. Call the script at `scripts/nutrition_lookup.py`, passing the structured item list as input.
4. The script reads the bundled CSV, finds each food item, multiplies its nutrition values by the quantity, and sums everything up for the total.
5. If a food is not found in the CSV, the script flags it as unknown — do not guess or fill in values for it.
6. Present the structured report to the user.

## Expected output format

```
Item                     Qty      Calories  Protein  Carbs   Fat    Fiber
---                      ---      --------  -------  -----   ---    -----
Whole wheat toast        2 sl     138       6g       24g     2g     4g
Peanut butter            1 tbsp   94        4g       3g      8g     1g
Banana (medium)          1        105       1g       27g     0g     3g
Black coffee             1 cup    2         0g       0g      0g     0g

TOTAL                             339       11g      54g     10g    8g

Unknown items (not in database): none
```

If any items are unknown, list them clearly at the bottom rather than silently omitting them.

## Limitations and important checks

- Only foods present in the bundled CSV are supported. The skill never estimates or hallucinates nutrition values — this is the core reason the script exists, since language models produce inconsistent nutrition numbers.
- The user must specify quantities. The skill will not assume a default serving size.
- The skill does not handle compound dishes not in the CSV (e.g. "homemade lasagna") or nutrition for raw recipe ingredients.
- Nutrition values reflect standard reference amounts and may not match a specific brand or restaurant preparation.
- The script handles all multiplication and summation. Do not attempt to compute nutrition values in prose — use the script.
