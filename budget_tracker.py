"""Monthly spending analysis, projections and rule-based alerts."""
import calendar


def summarize_month(expenses, year, month, students, monthly_budget_per_student):
    rows = [row for row in expenses if row["date"].year == year and row["date"].month == month]
    if not rows:
        return None
    total = sum(row["amount"] for row in rows)
    by_category, by_day = {}, {}
    for row in rows:
        category = row["category"]
        by_category[category] = by_category.get(category, 0.0) + row["amount"]
        by_day[row["date"]] = by_day.get(row["date"], 0.0) + row["amount"]
    days_in_month = calendar.monthrange(year, month)[1]
    days_elapsed = max(day.day for day in by_day)
    budget = students * monthly_budget_per_student
    projected = total / days_elapsed * days_in_month
    peak_day = max(by_day, key=by_day.get)
    summary = {
        "year": year, "month": month, "total": total, "budget": budget,
        "percent_used": total / budget * 100, "days_elapsed": days_elapsed,
        "days_in_month": days_in_month, "projected": projected,
        "actual_per_student_day": total / (students * days_elapsed),
        "planned_per_student_day": monthly_budget_per_student / days_in_month,
        "by_category": by_category, "peak_day": peak_day, "peak_amount": by_day[peak_day],
    }
    summary["alerts"] = make_alerts(summary)
    return summary


def make_alerts(summary):
    alerts = []
    elapsed_pct = summary["days_elapsed"] / summary["days_in_month"] * 100
    if summary["percent_used"] >= 100:
        alerts.append("CRITICAL: The monthly budget has already been exceeded.")
    elif summary["projected"] > summary["budget"]:
        over = summary["projected"] - summary["budget"]
        alerts.append(f"WARNING: At the current rate the month will end Rs. {over:,.0f} over budget.")
    if elapsed_pct < 100 and elapsed_pct + 10 < summary["percent_used"] < 100:
        alerts.append(f"WARNING: {summary['percent_used']:.0f}% of budget used, but only {elapsed_pct:.0f}% of month passed.")
    for category, amount in sorted(summary["by_category"].items(), key=lambda item: item[1], reverse=True):
        share = amount / summary["total"] * 100
        if share > 35:
            alerts.append(f"NOTE: '{category}' takes {share:.0f}% of spending. Check for savings.")
    return alerts or ["OK: Spending is on track for the month."]
