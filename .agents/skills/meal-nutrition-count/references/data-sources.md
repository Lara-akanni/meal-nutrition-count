# Data Sources

## USDA FoodData Central

**URL:** https://fdc.nal.usda.gov  
**Used for:** Nutrition values in `assets/foods.csv`

All calorie and macronutrient values (protein, carbs, fat, fiber) in the food lookup table are sourced from USDA FoodData Central standards. Values are accurate to within approximately one or two calories of the published figures. Any entry in `foods.csv` can be spot-checked directly at the URL above.

### Scope decisions based on this source
- Proteins (chicken, beef, salmon, etc.) are listed per 100g, consistent with how USDA and nutrition labels express them.
- No brand-specific or restaurant items are included, as those values vary by chain and fall outside what a standard reference database can reliably cover.
