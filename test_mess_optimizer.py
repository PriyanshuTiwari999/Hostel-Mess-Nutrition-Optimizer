"""Run with: python test_mess_optimizer.py"""
from datetime import date
import budget_tracker
import data_manager
import nutrition_analysis
import optimizer

FOODS = data_manager.load_foods()
CAL, PROT = 2300.0, 70.0


def test_food_database_loaded_and_clean():
    assert len(FOODS) == 68
    assert all(food["name"] == food["name"].strip() for food in FOODS)


def test_normal_plan_within_budget():
    plan = optimizer.build_daily_plan(FOODS, 110, CAL, PROT)
    assert plan is not None and plan["feasible"] and plan["cost"] <= 110


def test_budget_below_cheapest_menu_is_infeasible():
    plan = optimizer.build_daily_plan(FOODS, 50, CAL, PROT)
    assert plan is not None and plan["feasible"] is False


def test_no_food_repeats_in_a_day():
    plan = optimizer.build_daily_plan(FOODS, 110, CAL, PROT)
    names = [food["name"] for _slot, food in plan["items"]]
    assert len(names) == len(set(names))


def test_vegetarian_plan_contains_only_veg_food():
    plan = optimizer.build_daily_plan(FOODS, 110, CAL, PROT, diet="veg")
    assert all(food["diet"] == "V" for _slot, food in plan["items"])


def test_week_has_seven_days_and_budget_limit():
    week = optimizer.build_weekly_plan(FOODS, 110, CAL, PROT)
    assert len(week) == 7
    assert all(day["cost"] <= 110 for day in week)


def test_search_is_case_insensitive_and_partial():
    assert nutrition_analysis.find_food(FOODS, "  DAL TADKA ")["name"] == "Dal Tadka"
    assert nutrition_analysis.find_food(FOODS, "not-a-food") is None


def test_meal_analysis_reports_unknown_food():
    _matched, unknown, _totals, _advice = nutrition_analysis.analyse_meal(
        FOODS, ["Tea", "not a food"], 110, CAL, PROT)
    assert unknown == ["not a food"]


def test_rank_is_descending_by_protein_per_rupee():
    _label, ranked = nutrition_analysis.rank_foods(FOODS, "1")
    values = [food["protein"] / food["cost"] for food in ranked]
    assert values == sorted(values, reverse=True)


def test_collection_sets_are_consistent():
    groups = nutrition_analysis.compare_diet_groups(FOODS)
    assert groups["both"] | groups["veg_only"] | groups["nonveg_only"] == groups["all"]


def test_budget_alert_for_projected_overspend():
    expenses = [{"date": date(2026, 11, day), "category": "Vegetables",
                 "amount": 30000.0, "note": ""} for day in range(1, 11)]
    summary = budget_tracker.summarize_month(expenses, 2026, 11, 200, 3300)
    assert any("over budget" in alert for alert in summary["alerts"])


def test_empty_month_returns_none():
    assert budget_tracker.summarize_month([], 2026, 11, 200, 3300) is None


if __name__ == "__main__":
    tests = [(name, fn) for name, fn in sorted(globals().items()) if name.startswith("test_")]
    passed = 0
    for name, function in tests:
        try:
            function()
            print(f"PASS  {name}")
            passed += 1
        except Exception as error:
            print(f"FAIL  {name}: {error}")
    print(f"\n{passed} of {len(tests)} tests passed")
    if passed != len(tests):
        raise SystemExit(1)
