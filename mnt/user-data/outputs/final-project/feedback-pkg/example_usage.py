"""
example_usage.py
~~~~~~~~~~~~~~~~
Four ways to use the Student Feedback System package.
"""

# ── Example 1: Simplest usage ──────────────────────────────────────
from feedback_system import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


# ── Example 2: Custom configuration ────────────────────────────────
from feedback_system import create_app
from feedback_system.config import Config

class MyConfig(Config):
    DB_PATH     = '/var/data/university_feedback.db'
    SECRET_KEY  = 'my-super-secret-production-key'
    PER_PAGE    = 10
    APP_NAME    = 'University Course Feedback'
    APP_TAGLINE = 'Helping Faculty Improve Every Semester'
    PORT        = 8080

app = create_app(config=MyConfig)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


# ── Example 3: Plug into an existing Flask app ─────────────────────
from flask import Flask
from feedback_system.routes import feedback_bp
from feedback_system.database import init_db

existing_app = Flask(__name__)
existing_app.secret_key = 'your-existing-secret'
existing_app.config['DB_PATH']     = './feedback.db'
existing_app.config['PER_PAGE']    = 6
existing_app.config['APP_NAME']    = 'My Portal'
existing_app.config['APP_TAGLINE'] = 'Student Portal'

# Mount feedback under /feedback prefix
existing_app.register_blueprint(feedback_bp, url_prefix='/feedback')

with existing_app.app_context():
    init_db(existing_app.config['DB_PATH'])

# Dashboard → http://localhost:5000/feedback/
# Submit    → http://localhost:5000/feedback/submit


# ── Example 4: Use the database layer directly (no Flask) ──────────
from feedback_system.database import (
    init_db, add_feedback, get_all_feedback,
    search_feedback, get_stats, export_csv
)

DB = './my_feedback.db'

init_db(DB)
add_feedback(DB, 'Alice', 'DevOps Lab', '5', 'Best lab ever!')
add_feedback(DB, 'Bob',   'Python 101', '4', 'Very informative.')

rows   = get_all_feedback(DB)
stats  = get_stats(DB)
search = search_feedback(DB, 'DevOps')
csv    = export_csv(DB)

print(f"Total   : {stats['total']}")
print(f"Avg     : {stats['avg_rating']}")
print(f"Results : {len(search)}")

# Save CSV backup
with open('feedback_backup.csv', 'w', encoding='utf-8') as f:
    f.write(csv)
