# Experiential Learning Activities Integration

This project has been updated to apply the Python concepts taught in the uploaded E3–E7 experiential learning materials. The examples below refer to the actual implementation in this repository.

## E3 — Module Review

**Course concepts:** variables, `input()`, type conversion, arithmetic/comparison operators, `if/elif/else`, validation, boundary testing and debugging.

**Where applied:**
- `utils.py`: reads user input, converts numeric text to `int`/`float`, and checks minimum/maximum values.
- `main.py`: uses conditional branches to process menu selections and display different results.
- `optimizer.py`: compares menu cost with the budget and checks calorie/protein targets.
- `budget_tracker.py`: compares spending and projections with the monthly budget to generate alerts.
- `test_mess_optimizer.py`: tests normal and boundary cases such as a budget below the cheapest possible menu.

The code uses inclusive range checks where the boundary is allowed, for example `low <= value <= high` in the input-validation design.

## E4 — String Slicing and String Methods

**Course concepts:** `strip()`, `lower()`, `upper()`, `title()`, `split()`, `find()`/substring checks, `replace()`, `isdigit()` and string immutability.

**Where applied:**
- `utils.py`: `clean_text()` trims and normalizes text; `get_choice()` uses `.strip().lower()` before comparing an answer.
- `data_manager.py`: cleans CSV fields, splits meal values on `"|"`, and normalizes category/diet text.
- `main.py`: splits a comma-separated list of foods into individual names and strips each name.
- `nutrition_analysis.py`: performs case-insensitive exact and partial food-name searches.
- `utils.py`: integer input is checked before conversion; invalid text is rejected rather than crashing.

String methods return new strings, so the updated value is stored or used directly in the comparison.

## E5 — Loop Control Statements

**Course concepts:** `break`, `continue`, `pass`, `for`/`while`, early exit, skipping unwanted values and debugging loop behaviour.

**Where applied:**
- `utils.py`: validation loops continue after invalid input and return only after valid input is received.
- `data_manager.py`: invalid CSV rows are skipped with `continue`, allowing later valid rows to be processed.
- `optimizer.py`: the improvement loop ends with `break` when no better menu swap exists; candidate foods already used are skipped with `continue`.
- `main.py`: the interactive menu uses `break` to exit and `continue` after an invalid menu selection.

`pass` is taught as a placeholder that does nothing. It is not inserted into a working project path because it would not improve the actual application; it is appropriate while sketching an unfinished function or branch.

## E6 — Membership, `enumerate()` and `zip()`

**Course concepts:** `in`, `not in`, positions with `enumerate()`, and parallel iteration with `zip()`.

**Where applied:**
- `main.py`: checks whether a new food name is already present before adding it.
- `optimizer.py`: uses membership checks against the `used` set and recent-food sets to prevent repetition.
- `main.py`: uses `enumerate(..., start=1)` to number food items, ranked foods and report rows.
- `main.py`: uses `zip()` to display weekly day names and corresponding plan records together.

## E7 — Integrated Collection Processing

**Course concepts:** strings, lists, dictionaries, sets, loops, functions, `sorted()`, collection aggregation and clear function responsibilities.

**Where applied:**
- Lists store food records, menu items, meal names and expense rows.
- Dictionaries represent each food, settings, nutrient totals and monthly spending by category.
- Sets represent allowed meals, already-used foods and unique vegetarian/non-vegetarian food names.
- Functions such as `build_daily_plan()`, `analyse_meal()` and `summarize_month()` each perform a focused task and return reusable results.
- `show_collection_insights()` builds category counts and uses set union/intersection to summarize the database.
- `budget_tracker.py` uses dictionary accumulation to calculate category totals and daily totals.

## Self-check before submission

1. Run `python main.py` and try each menu option.
2. Enter invalid menu choices, blank names and out-of-range numeric values to check validation.
3. Test food search with different capitalization and extra spaces.
4. Test a very low budget and a budget that can support the cheapest menu.
5. Run `python test_mess_optimizer.py` and record the actual result.
6. Check that the generated weekly report and chart are created when requested.

The uploaded E7 activity emphasizes comparing actual output with expected output and reviewing code rather than assuming it works. Use the test results from your own final run in the submission.
