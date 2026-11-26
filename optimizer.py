"""Daily and weekly menu planning using a greedy local-search approach."""
SLOTS = [
    ("Breakfast", "Main"), ("Breakfast", "Side"), ("Breakfast", "Beverage"),
    ("Lunch", "Staple"), ("Lunch", "Dal"), ("Lunch", "Curry"),
    ("Snack", "Snack"),
    ("Dinner", "Staple"), ("Dinner", "Dal"), ("Dinner", "Curry"), ("Dinner", "Side"),
]
WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
PROTEIN_WEIGHT, CALORIE_UPPER, FAT_SHARE = 2.0, 1.10, 0.30


def sum_nutrients(foods):
    totals = {key: 0.0 for key in ("cost", "calories", "protein", "carbs", "fat")}
    for food in foods:
        for key in totals:
            totals[key] += food[key]
    return totals


def plan_score(foods, calorie_target, protein_target):
    totals = sum_nutrients(foods)
    score = 0.0
    if totals["calories"] < calorie_target:
        score += (calorie_target - totals["calories"]) / calorie_target
    elif totals["calories"] > CALORIE_UPPER * calorie_target:
        score += (totals["calories"] - CALORIE_UPPER * calorie_target) / calorie_target
    if totals["protein"] < protein_target:
        score += PROTEIN_WEIGHT * (protein_target - totals["protein"]) / protein_target
    max_fat = FAT_SHARE * calorie_target / 9
    if totals["fat"] > max_fat:
        score += (totals["fat"] - max_fat) / max_fat
    return score


def get_candidates(foods, slot, diet="any", avoid_names=None):
    meal, category = slot
    options = [food for food in foods
               if meal in food["meals"] and food["category"] == category
               and (diet == "any" or food["diet"] == "V")]
    if avoid_names:
        different = [food for food in options if food["name"] not in avoid_names]
        if different:
            options = different
    return options


def build_daily_plan(foods, budget, calorie_target, protein_target, diet="any", avoid=None):
    avoid = avoid or {}
    candidates = {}
    for slot in SLOTS:
        options = get_candidates(foods, slot, diet, avoid.get(slot))
        if not options:
            return None
        candidates[slot] = options

    chosen, used = {}, set()
    for slot in SLOTS:
        for food in sorted(candidates[slot], key=lambda item: item["cost"]):
            if food["name"] not in used:
                chosen[slot] = food
                used.add(food["name"])
                break
        else:
            return None

    cost = sum_nutrients(chosen.values())["cost"]
    feasible = cost <= budget
    while feasible:
        current = plan_score(chosen.values(), calorie_target, protein_target)
        best_move, best_ratio = None, 0.0
        for slot in SLOTS:
            for food in candidates[slot]:
                if food["name"] in used:
                    continue
                new_cost = cost - chosen[slot]["cost"] + food["cost"]
                if new_cost > budget:
                    continue
                trial = dict(chosen)
                trial[slot] = food
                gain = current - plan_score(trial.values(), calorie_target, protein_target)
                if gain <= 1e-9:
                    continue
                extra = max(food["cost"] - chosen[slot]["cost"], 1.0)
                if gain / extra > best_ratio:
                    best_ratio, best_move = gain / extra, (slot, food)
        if best_move is None:
            break
        slot, food = best_move
        used.discard(chosen[slot]["name"])
        cost += food["cost"] - chosen[slot]["cost"]
        chosen[slot] = food
        used.add(food["name"])

    plan = sum_nutrients(chosen.values())
    plan["items"] = [(slot, chosen[slot]) for slot in SLOTS]
    plan["feasible"] = feasible
    plan["score"] = plan_score(chosen.values(), calorie_target, protein_target)
    return plan


def targets_met(plan, calorie_target, protein_target):
    return (0.90 * calorie_target <= plan["calories"] <= CALORIE_UPPER * calorie_target
            and plan["protein"] >= protein_target)


def build_weekly_plan(foods, budget, calorie_target, protein_target, diet="any"):
    week, history = [], []
    for day in WEEK_DAYS:
        plan = None
        for window in (2, 1, 0):
            recent = history[-window:] if window else []
            avoid = {slot: {past[slot] for past in recent} for slot in SLOTS}
            plan = build_daily_plan(foods, budget, calorie_target, protein_target, diet, avoid)
            if plan is not None and plan["feasible"]:
                break
        if plan is None or not plan["feasible"]:
            return []
        plan["day"] = day
        week.append(plan)
        history.append({slot: food["name"] for slot, food in plan["items"]})
    return week


def compare_budgets(foods, budgets, calorie_target, protein_target, diet="any"):
    return [(budget, build_daily_plan(foods, budget, calorie_target, protein_target, diet))
            for budget in budgets]
