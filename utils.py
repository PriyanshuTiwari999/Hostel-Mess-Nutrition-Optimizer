"""Input helpers and formatting utilities for the Hostel Mess Optimizer."""
from datetime import date, datetime


def clean_text(value):
    """E4: remove outside spaces and normalize repeated internal spaces."""
    return " ".join(str(value).replace("\\t", " ").strip().split())


def get_number(prompt, kind=float, low=None, high=None):
    """E3/E5: keep asking until a valid number in the allowed range is entered."""
    while True:
        raw = input(prompt).strip()
        try:
            # E4: isdigit is useful for integer input; float conversion handles decimals.
            if kind is int and not raw.isdigit():
                raise ValueError
            value = kind(raw)
        except ValueError:
            print("Invalid number. Please try again.")
            continue
        if low is not None and value < low:
            print(f"Value must be at least {low}.")
            continue
        if high is not None and value > high:
            print(f"Value must be at most {high}.")
            continue
        return value


def get_text(prompt):
    while True:
        value = clean_text(input(prompt))
        if value:
            return value
        print("This field cannot be empty.")


def get_choice(prompt, options):
    """E4/E6: clean text and use membership testing for validation."""
    lookup = {clean_text(option).lower(): option for option in options}
    while True:
        value = clean_text(input(prompt)).lower()
        if value in lookup:
            return lookup[value]
        print("Choose one of: " + ", ".join(options))


def get_yes_no(prompt):
    return get_choice(prompt + " (y/n): ", ["y", "n"]) == "y"


def get_date(prompt):
    while True:
        raw = input(prompt + " [YYYY-MM-DD, Enter=today]: ").strip()
        if not raw:
            return date.today()
        try:
            return datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date. Example: 2026-11-15")


def money(amount):
    return f"Rs. {amount:,.2f}"
