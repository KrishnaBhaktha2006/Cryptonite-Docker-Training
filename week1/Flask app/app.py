import sqlite3
from flask import Flask, render_template, url_for, request, redirect, g, abort
from datetime import datetime
import os

# --- Database Configuration ---
DATABASE = 'test.db'
app = Flask(__name__)

APP_ENV = os.environ.get('APP_ENV', 'development')

def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    if 'db' not in g:
        # Use sqlite3.Row to access columns by name (like task['content'])
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(e=None):
    """Closes the database again at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Initializes the database from the schema.sql file."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

# Create a flask command to initialize the DB. Run 'flask init-db' in your terminal.
@app.cli.command('init-db')
def init_db_command():
    """Clears the existing data and creates new tables."""
    init_db()
    print('Initialized the database.')

# --- Helper Function ---
def get_task(id):
    """Helper function to get a single task by ID or abort with 404."""
    db = get_db()
    task = db.execute('SELECT * FROM todo WHERE id = ?', (id,)).fetchone()
    if task is None:
        abort(404) # Not Found
    return task

# --- Routes ---
@app.route('/', methods=['POST', 'GET'])
def index():
    db = get_db()
    if request.method == 'POST':
        task_content = request.form['content']
        if not task_content:
            return 'There was an issue adding your task: Content cannot be empty', 400

        db.execute('INSERT INTO todo (content) VALUES (?)', (task_content,))
        db.commit()
        return redirect('/')

    else:
        # Fetch all tasks from the database
        tasks_cursor = db.execute('SELECT * FROM todo ORDER BY date_created')
        tasks = tasks_cursor.fetchall()
        return render_template('index.html', tasks=tasks, app_env=APP_ENV)


@app.route('/delete/<int:id>')
def delete(id):
    # Ensure task exists before deleting
    get_task(id)
    
    db = get_db()
    db.execute('DELETE FROM todo WHERE id = ?', (id,))
    db.commit()
    return redirect('/')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # Get the existing task or 404
    task = get_task(id)
    
    if request.method == 'POST':
        new_content = request.form['content']
        if not new_content:
            return 'There was an issue updating your task: Content cannot be empty', 400

        db = get_db()
        db.execute('UPDATE todo SET content = ? WHERE id = ?', (new_content, id))
        db.commit()
        return redirect('/')

    else:
        # For the GET request, just show the update page
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)