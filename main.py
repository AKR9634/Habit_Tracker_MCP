from fastmcp import FastMCP
import json
import pathlib
from datetime import date, datetime, timedelta
import os

mcp = FastMCP(name="Habit Tracker", instructions="Track daily habits, log completions, and view streaks and weekly summarize!!!")

BASE_DIR = pathlib.Path(__file__).parent
DATA_FILE = BASE_DIR / "habits.json"

# HELPERS

def load() -> dict:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {"habits":{}, "logs":{}}

def save(data: dict):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    DATA_FILE.write_text(json.dumps(data, indent=2))

def today() -> str:
    return date.today().isoformat()

def compute_streak(logs: list[str]) -> int:
    """Count consecutive days ending today (or yesterday)."""
    if not logs:
        return 0
    dates = sorted(set(logs), reverse=True)
    anchor = date.today()
    # Allow streak to include yesterday if not yet logged today
    if dates[0] != anchor.isoformat():
        anchor = anchor - timedelta(days=1)
    streak = 0
    for d in dates:
        if d == anchor.isoformat():
            streak += 1
            anchor -= timedelta(days=1)
        elif d < anchor.isoformat():
            break
    return streak



# TOOLS

@mcp.tool()
def add_habit(name: str, description: str = "") -> str:
    """Adds a new habit to track!!!"""
    data = load()
    key = name.strip().lower()
    if key in data["habits"]:
        return f"Habit '{name}' already exists."
    data["habits"][key] = {
        "name": name.strip(),
        "description": description,
        "created": today()
    }
    save(data)
    return f"Habit '{name}' added successfully."


@mcp.tool()
def log_done(habit_name: str, log_date: str = "") -> str:
    """Mark a habit as done for today (or a specific date).

    Args:
        habit_name: Name of the habit to mark complete.
        log_date: Optional date in YYYY-MM-DD format. Defaults to today.
    """
    data = load()
    key = habit_name.strip().lower()
    if key not in data["habits"]:
        return f"Habit '{habit_name}' not found. Use add_habit to create it first."
    target = log_date.strip() if log_date else today()
    try:
        datetime.strptime(target, "%Y-%m-%d")
    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD."
    if key not in data["logs"]:
        data["logs"][key] = []
    if target in data["logs"][key]:
        return f"'{habit_name}' was already logged for {target}."
    data["logs"][key].append(target)
    save(data)
    streak = compute_streak(data["logs"][key])
    return f"Logged '{habit_name}' for {target}. Current streak: {streak} day{'s' if streak != 1 else ''}."


@mcp.tool()
def get_streaks() -> str:
    """Get current streaks for all habits."""
    data = load()
    if not data["habits"]:
        return "No habits found. Add some with add_habit."
    lines = ["Current streaks:\n"]
    for key, habit in data["habits"].items():
        logs = data["logs"].get(key, [])
        streak = compute_streak(logs)
        total = len(logs)
        done_today = today() in logs
        status = "✓" if done_today else "○"
        lines.append(
            f"  {status} {habit['name']}: {streak} day streak  ({total} total completions)"
        )
    return "\n".join(lines)


@mcp.tool()
def list_habits() -> str:
    """List all tracked habits with their details."""
    data = load()
    if not data["habits"]:
        return "No habits tracked yet. Use add_habit to get started."
    lines = ["Your habits:\n"]
    for key, habit in data["habits"].items():
        desc = f" — {habit['description']}" if habit.get("description") else ""
        logs = data["logs"].get(key, [])
        lines.append(f"  • {habit['name']}{desc}  (since {habit['created']}, {len(logs)} completions)")
    return "\n".join(lines)


@mcp.tool()
def weekly_summary() -> str:
    """Show which habits were completed over the last 7 days."""
    data = load()
    if not data["habits"]:
        return "No habits found."
    days = [(date.today() - timedelta(days=i)).isoformat() for i in range(6, -1, -1)]
    day_labels = [(date.today() - timedelta(days=i)).strftime("%a %d") for i in range(6, -1, -1)]

    lines = ["Weekly summary (last 7 days):\n"]
    header = "  {:20s} ".format("Habit") + "  ".join(f"{d:6s}" for d in day_labels)
    lines.append(header)
    lines.append("  " + "-" * (len(header) - 2))

    for key, habit in data["habits"].items():
        logs = set(data["logs"].get(key, []))
        row = "  {:20s} ".format(habit["name"][:20])
        row += "  ".join("  ✓   " if d in logs else "  ○   " for d in days)
        lines.append(row)

    total_possible = len(data["habits"]) * 7
    total_done = sum(
        sum(1 for d in days if d in set(data["logs"].get(k, [])))
        for k in data["habits"]
    )
    lines.append(f"\n  Completion rate: {total_done}/{total_possible} ({round(total_done/total_possible*100) if total_possible else 0}%)")
    return "\n".join(lines)


@mcp.tool()
def remove_habit(habit_name: str) -> str:
    """Remove a habit and all its logs permanently.

    Args:
        habit_name: Name of the habit to remove.
    """
    data = load()
    key = habit_name.strip().lower()
    if key not in data["habits"]:
        return f"Habit '{habit_name}' not found."
    del data["habits"][key]
    data["logs"].pop(key, None)
    save(data)
    return f"Habit '{habit_name}' and all its logs have been removed."


@mcp.tool()
def undo_log(habit_name: str, log_date: str = "") -> str:
    """Remove a log entry for a habit (undo a mistaken check-in).

    Args:
        habit_name: Name of the habit.
        log_date: Date to remove in YYYY-MM-DD format. Defaults to today.
    """
    data = load()
    key = habit_name.strip().lower()
    target = log_date.strip() if log_date else today()
    logs = data["logs"].get(key, [])
    if target not in logs:
        return f"No log found for '{habit_name}' on {target}."
    logs.remove(target)
    data["logs"][key] = logs
    save(data)
    return f"Removed log for '{habit_name}' on {target}."


# ENTRY POINT

if __name__ == "__main__":
    mcp.run()
