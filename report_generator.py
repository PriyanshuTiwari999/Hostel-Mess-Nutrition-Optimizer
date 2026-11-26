"""Text reports and optional Matplotlib charts."""
from datetime import date
from utils import money


def format_plan(plan, title, calorie_target, protein_target, budget):
    lines = [title, "-" * 78,
             f"{'Meal':<10}{'Item':<28}{'Rs.':>6}{'kcal':>7}{'Prot(g)':>9}{'Fat(g)':>8}",
             "-" * 78]
    last_meal = ""
    for (meal, _category), food in plan["items"]:
        shown_meal = meal if meal != last_meal else ""
        last_meal = meal
        lines.append(f"{shown_meal:<10}{food['name']:<28}{food['cost']:>6.0f}"
                     f"{food['calories']:>7.0f}{food['protein']:>9.0f}{food['fat']:>8.0f}")
    lines += ["-" * 78,
              f"{'TOTAL':<38}{plan['cost']:>6.0f}{plan['calories']:>7.0f}"
              f"{plan['protein']:>9.0f}{plan['fat']:>8.0f}",
              f"{'TARGET':<38}{budget:>6.0f}{calorie_target:>7.0f}{protein_target:>9.0f}"]
    return "\n".join(lines)


def save_weekly_report(week, settings, filename):
    budget = settings["monthly_budget_per_student"] / 30
    lines = ["HOSTEL MESS WEEKLY MENU REPORT", f"Generated on: {date.today()}",
             f"Students: {settings['students']} | Diet: {settings['diet']}",
             f"Daily budget per student: {money(budget)}", ""]
    for plan in week:
        lines.extend([format_plan(plan, plan["day"], settings["calorie_target"],
                                  settings["protein_target"], budget), ""])
    weekly_cost = sum(plan["cost"] for plan in week)
    avg_cal = sum(plan["calories"] for plan in week) / len(week)
    avg_prot = sum(plan["protein"] for plan in week) / len(week)
    lines += ["WEEK SUMMARY", "-" * 78,
              f"Cost per student for the week: {money(weekly_cost)}",
              f"Cost for all {settings['students']} students: {money(weekly_cost * settings['students'])}",
              f"Average calories per day: {avg_cal:.0f} kcal",
              f"Average protein per day: {avg_prot:.0f} g"]
    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(lines) + "\n")


def plot_weekly(week, budget, filename):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return False
    days = [plan["day"][:3] for plan in week]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(days, [plan["cost"] for plan in week], label="Cost per student (Rs.)")
    ax.axhline(budget, linestyle="--", label=f"Budget Rs. {budget:.0f}")
    ax.set_ylabel("Rupees")
    ax2 = ax.twinx()
    ax2.plot(days, [plan["protein"] for plan in week], marker="o", label="Protein (g)")
    ax2.set_ylabel("Protein (g)")
    ax.set_title("Weekly Mess Menu: Cost and Protein")
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="best")
    fig.tight_layout()
    fig.savefig(filename, dpi=120)
    plt.close(fig)
    return True


def plot_expenses(summary, filename):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return False
    items = sorted(summary["by_category"].items(), key=lambda item: item[1], reverse=True)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar([item[0] for item in items], [item[1] for item in items])
    ax.set_ylabel("Rupees")
    ax.set_title(f"Mess Spending by Category ({summary['year']}-{summary['month']:02d})")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    fig.savefig(filename, dpi=120)
    plt.close(fig)
    return True
