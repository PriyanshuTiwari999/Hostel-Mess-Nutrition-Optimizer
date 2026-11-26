"""CSV and settings file handling. Uses strings, lists, dictionaries and validation."""
import csv
import os
from datetime import datetime
from utils import clean_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOOD_FILE = os.path.join(BASE_DIR, "food_items.csv")
EXPENSE_FILE = os.path.join(BASE_DIR, "expenses.csv")
SETTINGS_FILE = os.path.join(BASE_DIR, "settings.txt")
FOOD_FIELDS = ["name", "category", "meal", "diet", "cost", "calories", "protein", "carbs", "fat"]
NUMERIC_FIELDS = ["cost", "calories", "protein", "carbs", "fat"]
DEFAULT_SETTINGS = {
    "students": 200,
    "monthly_budget_per_student": 3300.0,
    "calorie_target": 2300.0,
    "protein_target": 70.0,
    "diet": "any",
}


def load_foods():
    foods = []
    try:
        with open(FOOD_FILE, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for line_no, row in enumerate(reader, start=2):
                try:
                    name = clean_text(row["name"])
                    category = clean_text(row["category"]).title()
                    meal_text = clean_text(row["meal"])
                    meals = {clean_text(m).title() for m in meal_text.split("|") if clean_text(m)}
                    diet = clean_text(row["diet"]).upper()
                    food = {"name": name, "category": category, "meals": meals, "diet": diet}
                    for field in NUMERIC_FIELDS:
                        raw = clean_text(row[field])
                        food[field] = float(raw)
                        if food[field] < 0:
                            raise ValueError("negative value")
                    if not name or not meals or food["cost"] <= 0 or diet not in ("V", "N"):
                        raise ValueError("invalid food row")
                    foods.append(food)
                except (KeyError, ValueError, TypeError, AttributeError):
                    print(f"Warning: skipped invalid food row {line_no}.")
                    continue
    except FileNotFoundError:
        print("food_items.csv was not found.")
    return foods


def save_food(food):
    new_file = not os.path.exists(FOOD_FILE)
    with open(FOOD_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if new_file:
            writer.writerow(FOOD_FIELDS)
        writer.writerow([food["name"], food["category"], "|".join(sorted(food["meals"])),
                         food["diet"], food["cost"], food["calories"], food["protein"],
                         food["carbs"], food["fat"]])


def load_settings():
    settings = dict(DEFAULT_SETTINGS)
    try:
        with open(SETTINGS_FILE, encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = clean_text(key)
                if key not in settings:
                    continue
                try:
                    settings[key] = type(DEFAULT_SETTINGS[key])(clean_text(value))
                except ValueError:
                    continue
    except FileNotFoundError:
        save_settings(settings)
    return settings


def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
        for key, value in settings.items():
            file.write(f"{key}={value}\n")


def load_expenses():
    expenses = []
    try:
        with open(EXPENSE_FILE, newline="", encoding="utf-8") as file:
            for line_no, row in enumerate(csv.DictReader(file), start=2):
                try:
                    amount = float(clean_text(row["amount"]))
                    if amount < 0:
                        raise ValueError("negative amount")
                    expenses.append({
                        "date": datetime.strptime(clean_text(row["date"]), "%Y-%m-%d").date(),
                        "category": clean_text(row["category"]).title(),
                        "amount": amount,
                        "note": clean_text(row.get("note", "")),
                    })
                except (KeyError, ValueError):
                    print(f"Warning: skipped invalid expense row {line_no}.")
                    continue
    except FileNotFoundError:
        pass
    return expenses


def add_expense(expense_date, category, amount, note):
    new_file = not os.path.exists(EXPENSE_FILE)
    with open(EXPENSE_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if new_file:
            writer.writerow(["date", "category", "amount", "note"])
        writer.writerow([expense_date.isoformat(), category, amount, note])
