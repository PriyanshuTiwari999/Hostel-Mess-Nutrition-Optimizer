# Hostel Mess Nutrition & Budget Optimizer

A menu-driven Python project that helps hostel mess teams plan meals within a per-student budget, review nutrition totals, and monitor monthly spending.

## Features

- Food database with 68 sample food items stored in `food_items.csv`
- Daily menu optimization across breakfast, lunch, snack and dinner
- Seven-day menu planning with a variety rule
- Calorie, protein, carbohydrate and fat calculations
- Food ranking by protein per rupee, calories per rupee and cost
- Analysis of food names entered by a student
- Monthly expense summaries, projections and budget alerts
- Weekly text report and optional Matplotlib chart
- Automated tests for key project behaviour

> Food prices and nutrition values are sample/approximate values for academic demonstration. They are not medical or dietary advice.

## Requirements

- Python 3.10 or later
- Matplotlib is optional; install it to generate charts.

```bash
python -m pip install -r requirements.txt
```

## Run

Keep all `.py`, `.csv` and `.txt` files in the same project folder, then run:

```bash
python main.py
```

## Run tests

```bash
python test_mess_optimizer.py
```

## Project files

- `main.py` — menu-driven interface and user actions
- `data_manager.py` — reads/writes CSV and settings files
- `optimizer.py` — daily and weekly greedy menu optimizer
- `nutrition_analysis.py` — food search, ranking and meal analysis
- `budget_tracker.py` — monthly expense analysis and alerts
- `report_generator.py` — text reports and optional charts
- `utils.py` — input validation, string cleaning and formatting
- `test_mess_optimizer.py` — automated tests
- `food_items.csv` — food database
- `expenses.csv` — sample mess expenses
- `settings.txt` — default project settings

## Experiential Learning Activities applied

See [`EXPERIENTIAL_LEARNING_MAP.md`](EXPERIENTIAL_LEARNING_MAP.md) for a module-by-module explanation of how E3, E4, E5, E6 and E7 concepts are used in the project.

## Academic context

Computational Thinking and Programming — 2026CSAE100  
Bennett University, School of Computer Science Engineering and Technology  
Academic Year: 2026–27

## Team

- Abhinav Bhandari
- Shivalik Sharma
- Vaibhav Dwivedi
- Priyanshu Tiwari
- Prithvi Singh

Please confirm team roles/contributions with all members before publishing them.
