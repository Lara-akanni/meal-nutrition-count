# Skill Test Prompts

Three prompts used to demonstrate the meal-nutrition-count skill in a live agent session.

---

## Prompt 1 — Normal Case

**Input:**
> I had two scrambled eggs, a cup of oatmeal, a tablespoon of butter, and a glass of whole milk for breakfast. What are the macros?

**What this tests:** All items present in the database, quantities clearly specified, straightforward lookup and arithmetic.

**Script called with:**
```json
[
  {"food": "egg", "qty": 2},
  {"food": "oatmeal cooked", "qty": 1},
  {"food": "butter", "qty": 1},
  {"food": "whole milk", "qty": 1}
]
```

**Output:**

| Item | Qty | Calories | Protein | Carbs | Fat | Fiber |
|---|---|---|---|---|---|---|
| Egg | 2 | 144 kcal | 12.6g | 0.8g | 9.6g | 0g |
| Oatmeal (cooked) | 1 cup | 166 kcal | 5.9g | 28.1g | 3.6g | 4g |
| Butter | 1 tbsp | 102 kcal | 0.1g | 0g | 11.5g | 0g |
| Whole milk | 1 cup | 149 kcal | 7.7g | 11.7g | 8g | 0g |
| **TOTAL** | | **561 kcal** | **26.3g** | **40.6g** | **32.7g** | **4g** |

Unknown items: none

---

## Prompt 2 — Edge Case (Unknown Food)

**Input:**
> I had 100g of salmon, a cup of brown rice, and a miso soup for dinner. Give me the nutrition breakdown.

**What this tests:** Mix of known and unknown foods. The skill should return results for known items and flag the unknown one without guessing.

**Script called with:**
```json
[
  {"food": "salmon cooked", "qty": 1, "unit": "100g"},
  {"food": "brown rice cooked", "qty": 1, "unit": "cup"},
  {"food": "miso soup", "qty": 1, "unit": "bowl"}
]
```

**Output:**

| Item | Qty | Calories | Protein | Carbs | Fat | Fiber |
|---|---|---|---|---|---|---|
| Salmon (cooked) | 100g | 206 kcal | 22g | 0g | 12g | 0g |
| Brown rice (cooked) | 1 cup | 216 kcal | 5g | 45g | 1.8g | 3.5g |
| **TOTAL** | | **422 kcal** | **27g** | **45g** | **13.8g** | **3.5g** |

Unknown items: **miso soup** — flagged, not estimated.

---

## Prompt 3 — Out of Scope (Partial Decline)

**Input:**
> I've been eating about 2000 calories a day this week. Am I on track for my weight loss goal?

**What this tests:** Request that falls outside the skill's defined scope. The agent should decline the out-of-scope parts and explain what the skill can and cannot do.

**Script called:** Not called — no specific meal or food items were provided.

**Response:** The skill declined to answer because the request required:
- Tracking meals across multiple days (not supported)
- Evaluating intake against a personal weight loss goal (not supported)
- Making a health judgement (explicitly out of scope)

The agent offered to instead break down any specific meal the user describes in that session.
