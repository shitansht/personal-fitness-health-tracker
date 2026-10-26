"""
Personal Fitness & Health Tracker
Features:
- Register users and save profiles in users.csv
- Add and view daily fitness records in fitness_records.csv
- NumPy summaries for one user
- Matplotlib progress and all-user comparison charts

Run: py main.py
"""

import csv
from datetime import datetime
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

USERS_FILE = Path("users.csv")
RECORDS_FILE = Path("fitness_records.csv")

USER_HEADERS = ["User ID", "Name", "Age", "Fitness Goal"]
RECORD_HEADERS = [
    "User ID", "Date", "Steps", "Exercise Minutes", "Distance KM",
    "Calories Burned", "Water Litres", "Sleep Hours"
]


class FitnessUser:
    def __init__(self, user_id, name, age, goal):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.goal = goal

    def get_details(self):
        return [self.user_id, self.name, self.age, self.goal]


class FitnessRecord:
    def __init__(self, user_id, date, steps, exercise_minutes,
                 distance_km, calories, water_litres, sleep_hours):
        self.user_id = user_id
        self.date = date
        self.steps = steps
        self.exercise_minutes = exercise_minutes
        self.distance_km = distance_km
        self.calories = calories
        self.water_litres = water_litres
        self.sleep_hours = sleep_hours

    def get_details(self):
        return [
            self.user_id, self.date, self.steps, self.exercise_minutes,
            self.distance_km, self.calories, self.water_litres, self.sleep_hours
        ]


def create_files():
    """Create CSV files with headers if they do not already exist."""
    if not USERS_FILE.exists() or USERS_FILE.stat().st_size == 0:
        with USERS_FILE.open("w", newline="", encoding="utf-8") as file:
            csv.writer(file).writerow(USER_HEADERS)

    if not RECORDS_FILE.exists() or RECORDS_FILE.stat().st_size == 0:
        with RECORDS_FILE.open("w", newline="", encoding="utf-8") as file:
            csv.writer(file).writerow(RECORD_HEADERS)


def read_rows(filename):
    """Read a CSV file into a list of dictionaries."""
    with open(filename, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def register_user():
    user_id = input("Enter User ID: ").strip()
    name = input("Enter Name: ").strip()

    if not user_id or not name:
        print("User ID and name are required.")
        return

    users = read_rows(USERS_FILE)
    if any(u["User ID"].strip().lower() == user_id.lower() for u in users):
        print("User ID already exists.")
        return

    try:
        age = int(input("Enter Age: "))
        if not 1 <= age <= 120:
            print("Please enter an age from 1 to 120.")
            return
    except ValueError:
        print("Age must be a whole number.")
        return

    goal = input("Enter Fitness Goal: ").strip()
    if not goal:
        print("Fitness goal is required.")
        return

    user = FitnessUser(user_id, name, age, goal)
    with USERS_FILE.open("a", newline="", encoding="utf-8") as file:
        csv.writer(file).writerow(user.get_details())

    print("User registered successfully.")


def show_users():
    users = read_rows(USERS_FILE)
    if not users:
        print("No users registered.")
        return

    print("\n--- Registered Users ---")
    for user in users:
        print(
            f"ID: {user['User ID']} | Name: {user['Name']} | "
            f"Age: {user['Age']} | Goal: {user['Fitness Goal']}"
        )


def add_fitness_record():
    user_id = input("Enter User ID: ").strip()
    users = read_rows(USERS_FILE)
    user = next(
        (u for u in users if u["User ID"].strip().lower() == user_id.lower()),
        None
    )
    if user is None:
        print("User not found. Register the user first.")
        return

    date_text = input("Enter Date (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        print("Please enter a valid date in YYYY-MM-DD format.")
        return

    try:
        steps = int(input("Enter Steps: "))
        exercise = int(input("Enter Exercise Minutes: "))
        distance = float(input("Enter Distance (km): "))
        calories = float(input("Enter Estimated Calories Burned: "))
        water = float(input("Enter Water Intake (litres): "))
        sleep = float(input("Enter Sleep Hours (0-24): "))

        if steps < 0 or exercise < 0 or distance < 0 or calories < 0 or water < 0:
            print("Fitness values cannot be negative.")
            return
        if not 0 <= sleep <= 24:
            print("Sleep must be between 0 and 24 hours.")
            return
    except ValueError:
        print("Please enter valid numeric values.")
        return

    record = FitnessRecord(
        user_id, date_text, steps, exercise, distance, calories, water, sleep
    )
    with RECORDS_FILE.open("a", newline="", encoding="utf-8") as file:
        csv.writer(file).writerow(record.get_details())

    print("Fitness record saved successfully.")


def show_records():
    records = read_rows(RECORDS_FILE)
    users = read_rows(USERS_FILE)
    if not records:
        print("No fitness records available.")
        return

    names = {u["User ID"]: u["Name"] for u in users}
    print("\n--- Fitness Records ---")
    for record in records:
        print(
            f"User: {names.get(record['User ID'], 'Unknown')} "
            f"| ID: {record['User ID']} | Date: {record['Date']} "
            f"| Steps: {record['Steps']} "
            f"| Exercise (min): {record['Exercise Minutes']} "
            f"| Distance (km): {record['Distance KM']} "
            f"| Calories (estimated): {record['Calories Burned']} "
            f"| Water (L): {record['Water Litres']} "
            f"| Sleep (hours): {record['Sleep Hours']}"
        )


def _records_for_user(user_id):
    rows = read_rows(RECORDS_FILE)
    selected = [
        row for row in rows
        if row.get("User ID", "").strip().lower() == user_id.strip().lower()
    ]
    selected.sort(key=lambda row: row["Date"])
    return selected


def create_graphs(dates, steps, exercise, water, sleep, user_name):
    """Show six charts for a user's daily records."""
    # 1. Bar chart: daily steps
    plt.figure(figsize=(10, 5))
    plt.bar(dates, steps)
    plt.xlabel("Date")
    plt.ylabel("Steps")
    plt.title(f"Daily Steps - {user_name}")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()

    # 2. Line graph: step progress
    plt.figure(figsize=(10, 5))
    plt.plot(dates, steps, marker="o")
    plt.xlabel("Date")
    plt.ylabel("Steps")
    plt.title(f"Step Progress Over Time - {user_name}")
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()

    # 3. Pie chart: exercise-time share by date
    positive = [(d, m) for d, m in zip(dates, exercise) if m > 0]
    if positive:
        pie_dates, pie_minutes = zip(*positive)
        plt.figure(figsize=(7, 7))
        plt.pie(pie_minutes, labels=pie_dates, autopct="%1.1f%%", startangle=90)
        plt.title(f"Share of Exercise Time by Date - {user_name}")
        plt.tight_layout()
    else:
        print("Pie chart skipped: no exercise minutes recorded.")

    # 4. Box plot: supported by current Matplotlib versions
    plt.figure(figsize=(7, 4))
    plt.boxplot(steps, tick_labels=["Daily Steps"])
    plt.ylabel("Steps")
    plt.title(f"Distribution of Daily Steps - {user_name}")
    plt.tight_layout()

    # 5. Steps vs exercise minutes with separate axes
    fig, ax_steps = plt.subplots(figsize=(10, 5))
    ax_steps.bar(dates, steps, alpha=0.7)
    ax_steps.set_xlabel("Date")
    ax_steps.set_ylabel("Steps")
    ax_steps.tick_params(axis="x", rotation=35)
    ax_exercise = ax_steps.twinx()
    ax_exercise.plot(dates, exercise, marker="o")
    ax_exercise.set_ylabel("Exercise Minutes")
    ax_steps.set_title(f"Steps vs Exercise Minutes - {user_name}")
    fig.tight_layout()

    # 6. Water intake vs sleep with separate axes
    fig, ax_water = plt.subplots(figsize=(10, 5))
    ax_water.plot(dates, water, marker="o")
    ax_water.set_xlabel("Date")
    ax_water.set_ylabel("Water (litres)")
    ax_water.tick_params(axis="x", rotation=35)
    ax_sleep = ax_water.twinx()
    ax_sleep.plot(dates, sleep, marker="s", linestyle="--")
    ax_sleep.set_ylabel("Sleep (hours)")
    ax_water.set_title(f"Water Intake vs Sleep - {user_name}")
    fig.tight_layout()

    plt.show()


def analyse_fitness():
    user_id = input("Enter User ID to analyse: ").strip()
    users = read_rows(USERS_FILE)
    user = next(
        (u for u in users if u["User ID"].strip().lower() == user_id.lower()),
        None
    )
    if user is None:
        print("User not found. Register the user first.")
        return

    records = _records_for_user(user_id)
    if not records:
        print("No fitness records found for this user.")
        return

    dates = [r["Date"] for r in records]
    steps = np.array([float(r["Steps"]) for r in records])
    exercise = np.array([float(r["Exercise Minutes"]) for r in records])
    distance = np.array([float(r["Distance KM"]) for r in records])
    calories = np.array([float(r["Calories Burned"]) for r in records])
    water = np.array([float(r["Water Litres"]) for r in records])
    sleep = np.array([float(r["Sleep Hours"]) for r in records])

    print(f"\n--- Fitness Analysis: {user['Name']} ---")
    print("Number of recorded days:", len(records))
    print("Total steps:", int(np.sum(steps)))
    print("Average daily steps:", round(float(np.mean(steps)), 2))
    print("Minimum daily steps:", int(np.min(steps)))
    print("Maximum daily steps:", int(np.max(steps)))
    print("Total exercise minutes:", round(float(np.sum(exercise)), 2))
    print("Average exercise minutes:", round(float(np.mean(exercise)), 2))
    print("Total distance (km):", round(float(np.sum(distance)), 2))
    print("Total estimated calories:", round(float(np.sum(calories)), 2))
    print("Average water intake (litres):", round(float(np.mean(water)), 2))
    print("Average sleep (hours):", round(float(np.mean(sleep)), 2))

    create_graphs(dates, steps, exercise, water, sleep, user["Name"])


def compare_all_users():
    users = read_rows(USERS_FILE)
    records = read_rows(RECORDS_FILE)

    names = []
    average_steps = []
    total_steps = []
    total_exercise = []
    total_distance = []
    average_water = []
    average_sleep = []

    for user in users:
        own = [
            r for r in records
            if r["User ID"].strip().lower() == user["User ID"].strip().lower()
        ]
        if not own:
            continue

        steps = np.array([float(r["Steps"]) for r in own])
        exercise = np.array([float(r["Exercise Minutes"]) for r in own])
        distance = np.array([float(r["Distance KM"]) for r in own])
        water = np.array([float(r["Water Litres"]) for r in own])
        sleep = np.array([float(r["Sleep Hours"]) for r in own])

        names.append(user["Name"])
        average_steps.append(float(np.mean(steps)))
        total_steps.append(float(np.sum(steps)))
        total_exercise.append(float(np.sum(exercise)))
        total_distance.append(float(np.sum(distance)))
        average_water.append(float(np.mean(water)))
        average_sleep.append(float(np.mean(sleep)))

    if not names:
        print("No fitness records available for comparison.")
        return

    print("\n--- All-User Fitness Comparison ---")
    print("Users with records:", len(names))
    print("Total saved fitness records for registered users:", sum(
        1 for r in records
        if any(r["User ID"].strip().lower() == u["User ID"].strip().lower()
               for u in users)
    ))
    for i, name in enumerate(names):
        print(
            f"{name}: total steps={total_steps[i]:.0f}, "
            f"average steps/day={average_steps[i]:.0f}, "
            f"exercise minutes={total_exercise[i]:.0f}, "
            f"distance={total_distance[i]:.2f} km"
        )

    # 1. Average steps comparison
    plt.figure(figsize=(9, 5))
    plt.bar(names, average_steps)
    plt.title("Average Daily Steps: User Comparison")
    plt.xlabel("User")
    plt.ylabel("Average Steps")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    # 2. Total exercise minutes comparison
    plt.figure(figsize=(9, 5))
    plt.bar(names, total_exercise)
    plt.title("Total Exercise Minutes: User Comparison")
    plt.xlabel("User")
    plt.ylabel("Exercise Minutes")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    # 3. Pie chart: each user's share of all recorded steps
    if sum(total_steps) > 0:
        plt.figure(figsize=(7, 7))
        plt.pie(total_steps, labels=names, autopct="%1.1f%%", startangle=90)
        plt.title("Share of Total Recorded Steps by User")
        plt.tight_layout()

    # 4. Water and sleep comparison (different units, shown with clear labels)
    positions = np.arange(len(names))
    width = 0.35
    plt.figure(figsize=(10, 5))
    plt.bar(positions - width / 2, average_water, width, label="Water (litres/day)")
    plt.bar(positions + width / 2, average_sleep, width, label="Sleep (hours/day)")
    plt.xticks(positions, names, rotation=30, ha="right")
    plt.title("Average Water Intake and Sleep by User")
    plt.ylabel("Average value (units differ)")
    plt.legend()
    plt.tight_layout()

    plt.show()


def main():
    create_files()
    while True:
        print("\n===== PERSONAL FITNESS & HEALTH TRACKER =====")
        print("1. Register User")
        print("2. View Users")
        print("3. Add Fitness Record")
        print("4. View Fitness Records")
        print("5. Analyse One User's Fitness")
        print("6. Compare All Users")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            show_users()
        elif choice == "3":
            add_fitness_record()
        elif choice == "4":
            show_records()
        elif choice == "5":
            analyse_fitness()
        elif choice == "6":
            compare_all_users()
        elif choice == "7":
            print("Thank you for using the Fitness Tracker!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
