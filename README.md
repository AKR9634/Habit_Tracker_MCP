# 🧠 Habit Tracker MCP Server

A lightweight MCP server built with FastMCP for tracking daily habits, streaks, and consistency — all stored locally in a simple JSON file.

Perfect for use with Claude Desktop or any MCP-compatible client.

---

## ✨ Features

- ✅ Create and manage habits
- 📅 Log habit completions by date
- 🔥 Automatic streak tracking
- 📊 Weekly completion summaries
- ↩️ Undo mistaken logs
- 🗑️ Remove habits cleanly
- 💾 Local-first JSON storage (no database required)

---

## 🚀 Installation

```bash
pip install fastmcp
```

Run the server:

```bash
python habit_tracker.py
```

---

## 🔌 Connect to Claude Desktop

Add this configuration to your `claude_desktop_config.json`:

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

Restart Claude Desktop after saving the config.

---

## 🛠 Available Tools

| Tool | Description |
|------|-------------|
| `add_habit` | Create a new habit |
| `log_done` | Mark a habit as completed for a date |
| `get_streaks` | View current streaks |
| `list_habits` | List all tracked habits |
| `weekly_summary` | Show a 7-day completion grid |
| `remove_habit` | Delete a habit and its logs |
| `undo_log` | Remove an accidental completion log |

---

## 💬 Example Prompts

```text
"Add a habit called Meditate"

"Log exercise as done for today"

"What are my current streaks?"

"Show my weekly summary"

"I accidentally logged reading twice, undo today's log"
```

---

## 📁 Data Storage

All data is stored locally in:

```text
habits.json
```

No external database or cloud service is required.

Example structure:

```json
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
    "exercise": [
      "2026-05-10",
      "2026-05-11",
      "2026-05-13",
      "2026-05-14",
      "2026-05-15",
      "2026-05-16"
    ],
    "read": [
      "2026-05-12",
      "2026-05-15",
      "2026-05-16"
    ],
    "meditate": [
      "2026-05-14",
      "2026-05-15"
    ]
  }
}
```

---

## 📌 Notes

- Dates use the `YYYY-MM-DD` format
- Habit names are stored internally in lowercase
- Data is human-readable and easy to back up
- Works fully offline

---

## 📜 License

MIT License