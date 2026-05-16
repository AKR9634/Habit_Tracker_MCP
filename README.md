# Habit Tracker MCP Server

A simple MCP server built with FastMCP that tracks daily habits and streaks using a local JSON file.

## Setup

```bash
pip install fastmcp
python habit_tracker.py
```

## Connect to Claude Desktop

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "habit-tracker": {
      "command": "python",
      "args": ["/full/path/to/habit_tracker.py"]
    }
  }
}
```

## Tools

| Tool | What it does |
|---|---|
| `add_habit` | Create a new habit to track |
| `log_done` | Mark a habit complete for today (or any date) |
| `get_streaks` | See current streak for every habit |
| `list_habits` | List all habits with creation date and total count |
| `weekly_summary` | 7-day grid showing completion per habit |
| `remove_habit` | Delete a habit and all its history |
| `undo_log` | Remove a mistaken check-in |

## Example usage with Claude

> "Add a habit called Meditate"  
> "Log exercise as done for today"  
> "What are my current streaks?"  
> "Show me my weekly summary"  
> "I accidentally logged reading twice, undo today's log"

## Data storage

All data is saved in `habits.json` in the same folder as the script. Back it up anytime — it's plain JSON.


The Data in the habits.json is of the form:

{
  "habits": {
    "exercise": {
      "name": "Exercise",
      "description": "30 mins workout",
      "created": "2026-05-10"
    },
    "read": {
      "name": "Read",
      "description": "",
      "created": "2026-05-12"
    },
    "meditate": {
      "name": "Meditate",
      "description": "10 mins morning session",
      "created": "2026-05-14"
    }
  },
  "logs": {
    "exercise": ["2026-05-10", "2026-05-11", "2026-05-13", "2026-05-14", "2026-05-15", "2026-05-16"],
    "read":     ["2026-05-12", "2026-05-15", "2026-05-16"],
    "meditate": ["2026-05-14", "2026-05-15"]
  }
}