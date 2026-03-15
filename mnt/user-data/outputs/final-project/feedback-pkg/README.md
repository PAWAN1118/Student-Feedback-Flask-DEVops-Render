# Student Feedback System

A plug-and-play student feedback web application built with Flask.
Install it, run one command, and you have a fully working feedback portal.

## Installation

```bash
pip install student-feedback-system
```

## Quickstart

```bash
feedback-system run
# Open http://localhost:5000
```

## CLI Commands

```bash
feedback-system run                    # Start app (default port 5000)
feedback-system run --port 8080        # Custom port
feedback-system run --debug            # Debug mode
feedback-system run --config development

feedback-system init-db                # Create database tables
feedback-system export-csv             # Export all feedback to feedback.csv
feedback-system reset-db               # ⚠ Delete all data and recreate DB
feedback-system info                   # Show current configuration
feedback-system --version              # Show version
```

## Configuration via Environment Variables

```bash
export DB_PATH=/var/data/feedback.db
export SECRET_KEY=your-production-secret
export PORT=8080
export PER_PAGE=10
export APP_NAME="My University Feedback"

feedback-system run
```

## Configuration via Code

```python
from feedback_system import create_app
from feedback_system.config import Config

class MyConfig(Config):
    DB_PATH    = '/var/data/feedback.db'
    SECRET_KEY = 'super-secret-key'
    PER_PAGE   = 10
    APP_NAME   = 'My University Feedback'
    APP_TAGLINE= 'Helping Faculty Improve Every Semester'

app = create_app(config=MyConfig)
app.run(host='0.0.0.0', port=8080)
```

## Embed in an Existing Flask App

```python
from flask import Flask
from feedback_system.routes import feedback_bp
from feedback_system.database import init_db

app = Flask(__name__)
app.config['DB_PATH'] = './feedback.db'
app.config['PER_PAGE'] = 6
app.secret_key = 'your-secret'

# Mount at /feedback prefix
app.register_blueprint(feedback_bp, url_prefix='/feedback')

with app.app_context():
    init_db(app.config['DB_PATH'])

# Dashboard → http://localhost:5000/feedback/
# Submit   → http://localhost:5000/feedback/submit
```

## Use the Database Layer Directly

```python
from feedback_system.database import init_db, add_feedback, get_stats, export_csv

DB = './feedback.db'
init_db(DB)
add_feedback(DB, 'Alice', 'DevOps Lab', '5', 'Best lab ever!')
print(get_stats(DB))

csv_data = export_csv(DB)
with open('backup.csv', 'w') as f:
    f.write(csv_data)
```

## Features

- Submit, view, edit, delete feedback
- Star ratings (1–5)
- Search and filter
- Pagination (configurable per page)
- Rating distribution chart
- CSV export via CLI and HTTP
- Professional corporate UI (navy/gold theme)
- Health check endpoint at `/health`

## Tech Stack

Flask · SQLite · Gunicorn · Chart.js · Click

## License

MIT
