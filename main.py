"""Hostel Mess Nutrition & Budget Optimizer.

Run: python main.py
The application integrates the Python concepts from Experiential Activities E3-E7.
"""
from datetime import date
import budget_tracker
import data_manager
import nutrition_analysis
import optimizer
import report_generator
from utils import get_choice, get_date, get_number, get_text, money

CATEGORIES = ["Main", "Side", "Beverage", "Staple", "Dal", "Curry", "Snack"]
MEALS = ["Breakfast", "Lunch", "Dinner", "Snack"]
EXPENSE_CATEGORIES = ["Vegetables", "Grains & Pulses", "Dairy", "Egg & Meat", "Gas & Fuel", "Wages & Other"]


def daily_budget(settings):
    return settings["monthly_budget_per_student"] / 30


def view_foods(foods):
    print(f"\n{'No.':<4}{'Name':<27}{'Category':<10}{'Diet':<5}{'Rs.':>6}{'kcal':>7}{'Prot':>7}")
    print("-" * 68)
    for number, food in enumerate(sorted(foods, key=lambda item: (item["category"], item["name"])), start=1):
        print(f"{number:<4}{food['name']:<27}{food['category']:<10}{food['diet']:<5}"
              f"{food['cost']:>6.0f}{food['calories']:>7.0f}{food['protein']:>7.0f}")
    print(f"\nTotal food items: {len(foods)}")


def add_food(foods):
    print("\n--- Add a new food item ---")
    name = get_text("Food name: ")
    # E6: membership check prevents duplicate names.
    existing_names = {food["name"].lower() for food in foods}
    if name.lower() in existing_names:
        print("That food already exists.")
        return
    category = get_choice(f"Category {CATEGORIES}: ", CATEGORIES)
    meal = get_choice(f"Meal {MEALS}: ", MEALS)
    diet = get_choice("Diet (V/N): ", ["V", "N"])
    food = {
        "name": name, "category": category, "meals": {meal}, "diet": diet,
        "cost": get_number("Cost per serving (Rs.): ", float, 0.5, 1000),
        "calories": get_number("Calories: ", float, 0, 3000),
        "protein": get_number("Protein (g): ", float, 0, 200),
        "carbs": get_number("Carbohydrates (g): ", float, 0, 500),
        "fat": get_number("Fat (g): ", float, 0, 300),
    }
    foods.append(food)
    data_manager.save_food(food)
    print(f"Saved {name} to food_items.csv.")


def rank_menu(foods, settings):
    print("\n--- Rank foods by value ---")
    for key, (label, _function) in nutrition_analysis.RANK_CRITERIA.items():
        print(f"{key}. {label}")
    choice = get_choice("Choose criterion (1-3): ", list(nutrition_analysis.RANK_CRITERIA))
    count = get_number("Number of foods to show (1-20): ", int, 1, 20)
    label, ranked = nutrition_analysis.rank_foods(foods, choice, settings["diet"])
    print(f"\nTop {count}: {label}")
    for rank, food in enumerate(ranked[:count], start=1):
        print(f"{rank}. {food['name']}: Rs.{food['cost']:.0f}, "
              f"{food['protein'] / food['cost']:.2f} g protein/Rs.")


def show_plan(plan, title, settings, budget):
    if plan is None:
        print("Cannot build a menu: one or more meal slots have no matching food.")
        return
    if not plan["feasible"]:
        print(f"The cheapest possible menu costs {money(plan['cost'])}, above the budget {money(budget)}.")
        return
    print("\n" + report_generator.format_plan(
        plan, title, settings["calorie_target"], settings["protein_target"], budget))
    if optimizer.targets_met(plan, settings["calorie_target"], settings["protein_target"]):
        print(f"All nutrition targets met. Unspent: {money(budget - plan['cost'])}")
    else:
        print("The menu is within budget, but one or more nutrition targets are not met.")


def today_menu(foods, settings):
    budget = daily_budget(settings)
    raw = input(f"Daily budget per student [Enter={budget:.2f}]: ").strip()
    if raw:
        try:
            budget = float(raw)
            if budget <= 0:
                raise ValueError
        except ValueError:
            print("Invalid budget; using the default.")
            budget = daily_budget(settings)
    plan = optimizer.build_daily_plan(foods, budget, settings["calorie_target"],
                                      settings["protein_target"], settings["diet"])
    show_plan(plan, "OPTIMIZED DAILY MENU", settings, budget)


def weekly_menu(foods, settings):
    budget = daily_budget(settings)
    week = optimizer.build_weekly_plan(foods, budget, settings["calorie_target"],
                                       settings["protein_target"], settings["diet"])
    if not week:
        print("Could not create a complete weekly menu within the daily budget.")
        return
    print(f"\n{'Day':<13}{'Breakfast':<24}{'Lunch':<35}{'Rs.':>6}{'kcal':>7}{'Prot':>7}")
    print("-" * 90)
    for day_no, plan in enumerate(week, start=1):
        names = {slot: food["name"] for slot, food in plan["items"]}
        lunch = names[("Lunch", "Staple")] + " + " + names[("Lunch", "Dal")]
        print(f"{day_no}. {plan['day']:<10}{names[('Breakfast', 'Main')][:22]:<24}"
              f"{lunch[:33]:<35}{plan['cost']:>6.0f}{plan['calories']:>7.0f}{plan['protein']:>7.0f}")
    # E6: zip demonstrates parallel processing of day labels and plan records.
    print("\nDaily cost cross-check:")
    for day, plan in zip([p["day"] for p in week], week):
        print(f"{day}: {money(plan['cost'])}")
    print(f"Weekly cost per student: {money(sum(p['cost'] for p in week))}")


def analyse_my_day(foods, settings):
    print("\nEnter food names eaten today, separated by commas.")
    raw = input("Foods: ")
    # E4: split makes a list; strip cleans each entry.
    names = [part.strip() for part in raw.split(",") if part.strip()]
    if not names:
        print("No food names entered.")
        return
    budget = daily_budget(settings)
    matched, unknown, totals, advice = nutrition_analysis.analyse_meal(
        foods, names, budget, settings["calorie_target"], settings["protein_target"])
    print("\nMatched foods:")
    for index, food in enumerate(matched, start=1):
        print(f"{index}. {food['name']}")
    if unknown:
        print("Not found:", ", ".join(unknown))
    print(f"Total: Rs.{totals['cost']:.2f} | {totals['calories']:.0f} kcal | "
          f"{totals['protein']:.1f} g protein | {totals['fat']:.1f} g fat")
    for message in advice:
        print("-", message)


def record_expense():
    print("\n--- Record a mess expense ---")
    expense_date = get_date("Date")
    category = get_choice("Category: ", EXPENSE_CATEGORIES)
    amount = get_number("Amount (Rs.): ", float, 0.01, 10000000)
    note = input("Note (optional): ").strip()
    data_manager.add_expense(expense_date, category, amount, note)
    print("Expense saved.")


def monthly_summary(settings):
    year = get_number("Year: ", int, 2000, 2100)
    month = get_number("Month (1-12): ", int, 1, 12)
    summary = budget_tracker.summarize_month(
        data_manager.load_expenses(), year, month, settings["students"],
        settings["monthly_budget_per_student"])
    if summary is None:
        print("No expenses found for that month.")
        return
    print(f"\nMONTHLY SUMMARY {year}-{month:02d}")
    print(f"Spent: {money(summary['total'])} / {money(summary['budget'])}")
    print(f"Budget used: {summary['percent_used']:.1f}%")
    print(f"Projected month total: {money(summary['projected'])}")
    print("Spending by category:")
    for number, (category, amount) in enumerate(
            sorted(summary["by_category"].items(), key=lambda item: item[1], reverse=True), start=1):
        print(f"{number}. {category}: {money(amount)}")
    print("Alerts:")
    for alert in summary["alerts"]:
        print("-", alert)


def save_reports(foods, settings):
    budget = daily_budget(settings)
    week = optimizer.build_weekly_plan(foods, budget, settings["calorie_target"],
                                       settings["protein_target"], settings["diet"])
    if not week:
        print("Could not create a weekly report.")
        return
    report_generator.save_weekly_report(week, settings, "weekly_menu_report.txt")
    chart_ok = report_generator.plot_weekly(week, budget, "weekly_menu_chart.png")
    print("Saved weekly_menu_report.txt")
    print("Saved weekly_menu_chart.png" if chart_ok else "Matplotlib not installed; chart skipped.")


def show_collection_insights(foods):
    """E7: use dictionaries and sets to summarize a collection of food records."""
    category_counts = {}
    vegetarian_names = set()
    nonveg_names = set()
    for food in foods:
        category_counts[food["category"]] = category_counts.get(food["category"], 0) + 1
        if food["diet"] == "V":
            vegetarian_names.add(food["name"])
        else:
            nonveg_names.add(food["name"])
    print("\nFOOD DATABASE INSIGHTS")
    for category, count in sorted(category_counts.items()):
        print(f"{category}: {count} items")
    print(f"Unique food names: {len(vegetarian_names | nonveg_names)}")
    print(f"Vegetarian/non-vegetarian name overlap: {len(vegetarian_names & nonveg_names)}")


MENU = """
================ HOSTEL MESS NUTRITION & BUDGET OPTIMIZER ================
1. View food database          6. Analyse what I ate today
2. Add a food item             7. Record a mess expense
3. Rank foods by value         8. Monthly budget summary
4. Optimized menu for today    9. Save weekly report and chart
5. Optimized weekly menu      10. Food database insights
0. Exit
"""


def main():
    foods = data_manager.load_foods()
    settings = data_manager.load_settings()
    if not foods:
        print("No food data available. Check food_items.csv.")
        return
    actions = {
        "1": lambda: view_foods(foods),
        "2": lambda: add_food(foods),
        "3": lambda: rank_menu(foods, settings),
        "4": lambda: today_menu(foods, settings),
        "5": lambda: weekly_menu(foods, settings),
        "6": lambda: analyse_my_day(foods, settings),
        "7": record_expense,
        "8": lambda: monthly_summary(settings),
        "9": lambda: save_reports(foods, settings),
        "10": lambda: show_collection_insights(foods),
    }
    while True:
        print(MENU)
        print(f"Daily budget: {money(daily_budget(settings))} | "
              f"Targets: {settings['calorie_target']:.0f} kcal, {settings['protein_target']:.0f} g")
        choice = input("Choose 0-10: ").strip()
        if choice == "0":
            print("Thank you for using the Mess Optimizer. Goodbye!")
            break
        if choice not in actions:
            print("Invalid choice. Enter a number from 0 to 10.")
            continue
        try:
            actions[choice]()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting safely.")
            break


if __name__ == "__main__":
    main()
