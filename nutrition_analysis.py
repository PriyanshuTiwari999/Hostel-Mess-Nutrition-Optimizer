"""Food search, value ranking and analysis of a student's meal."""
from optimizer import sum_nutrients, FAT_SHARE, CALORIE_UPPER

RANK_CRITERIA = {
    "1": ("Protein per rupee (g/Rs.)", lambda food: food["protein"] / food["cost"]),
    "2": ("Calories per rupee (kcal/Rs.)", lambda food: food["calories"] / food["cost"]),
    "3": ("Lowest cost first (Rs.)", lambda food: -food["cost"]),
}


def find_food(foods, text):
    """E4: clean a search string; use find-like exact/partial matching."""
    text = text.strip().lower()
    if not text:
        return None
    for food in foods:
        if food["name"].strip().lower() == text:
            return food
    for food in foods:
        if text in food["name"].strip().lower():
            return food
    return None


def rank_foods(foods, criterion_key, diet="any"):
    label, key_function = RANK_CRITERIA[criterion_key]
    pool = [food for food in foods if diet == "any" or food["diet"] == "V"]
    return label, sorted(pool, key=key_function, reverse=True)


def analyse_meal(foods, names, budget, calorie_target, protein_target):
    matched, unknown = [], []
    for name in names:
        food = find_food(foods, name)
        if food is None:
            unknown.append(name)
            continue
        matched.append(food)

    totals = sum_nutrients(matched)
    advice = []
    if matched:
        if totals["calories"] < 0.90 * calorie_target:
            advice.append(f"Calories are low ({totals['calories']:.0f} of {calorie_target:.0f} kcal). Add rice or roti.")
        elif totals["calories"] > CALORIE_UPPER * calorie_target:
            advice.append("Calories are above 110% of target. Reduce fried items or large portions.")
        if totals["protein"] < protein_target:
            eaten_names = {food["name"] for food in matched}
            best = [food for food in rank_foods(foods, "1")[1] if food["name"] not in eaten_names][:3]
            advice.append("Protein is low. Best-value options: " + ", ".join(f["name"] for f in best) + ".")
        max_fat = FAT_SHARE * calorie_target / 9
        if totals["fat"] > max_fat:
            advice.append(f"Fat is high ({totals['fat']:.0f} g; limit about {max_fat:.0f} g). Choose boiled or steamed items.")
        if totals["cost"] > budget:
            advice.append(f"Cost Rs. {totals['cost']:.0f} is above the daily budget Rs. {budget:.0f}.")
        if not advice:
            advice.append("Well balanced! All targets are met within the budget.")
    return matched, unknown, totals, advice


def compare_diet_groups(foods):
    """E7: build unique category sets and return shared/diet-specific categories."""
    veg_categories = {food["category"] for food in foods if food["diet"] == "V"}
    nonveg_categories = {food["category"] for food in foods if food["diet"] == "N"}
    return {
        "both": veg_categories & nonveg_categories,
        "veg_only": veg_categories - nonveg_categories,
        "nonveg_only": nonveg_categories - veg_categories,
        "all": veg_categories | nonveg_categories,
    }


def meal_nutrition_by_name(foods, names):
    """E6: zip requested food names with matched records for a compact comparison."""
    rows = []
    for name in names:
        food = find_food(foods, name)
        if food is not None:
            rows.append((name, food["calories"], food["protein"]))
    return rows
