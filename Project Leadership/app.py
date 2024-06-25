from flask import Flask, render_template, request, redirect, url_for, g, session, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Function to get SQLite connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('user_data.db')
    return db

# Function to close SQLite connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Initialize database when app starts
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,  -- Ensure name is unique
                passcode TEXT NOT NULL,
                last_login TEXT,
                streak INTEGER DEFAULT 0
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS journal_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                template_id TEXT,
                text TEXT,
                created_at TEXT,
                user_name TEXT
            )
        ''')
        db.commit()

# Initialize database when app starts
init_db()

# Route to render ex.html form
@app.route('/')
def index():
    return render_template('ex.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    passcode = request.form.get('passcode')

    db = get_db()
    cursor = db.cursor()

    # Check if the user's name and passcode exist in the database
    cursor.execute('SELECT * FROM users WHERE name = ? AND passcode = ?', (name, passcode))
    user = cursor.fetchone()

    if user:
        # Store the user's name in the session
        session['user_name'] = name
        
        # Get current time and last login time
        current_time = datetime.now()
        last_login_time = datetime.strptime(user[3], '%Y-%m-%d %H:%M:%S') if user[3] else None
        
        # Calculate the streak based on calendar day
        if last_login_time:
            current_date = current_time.date()
            last_login_date = last_login_time.date()
            days_difference = (current_date - last_login_date).days
            
            if days_difference == 1:
                streak = user[4] + 1
            elif days_difference > 1:
                streak = 1
            else:
                streak = user[4]
        else:
            streak = 1
        
        # Update last_login and streak
        cursor.execute('UPDATE users SET last_login = ?, streak = ? WHERE name = ?', (current_time.strftime('%Y-%m-%d %H:%M:%S'), streak, name))
        db.commit()
        
        return redirect(url_for('main_page'))
    else:
        flash('Invalid credentials. Please try again.')
        return redirect(url_for('index'))

# Route to render the main page
@app.route('/main')
def main_page():
    if 'user_name' in session:
        user_name = session['user_name']
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT streak FROM users WHERE name = ?', (user_name,))
        user_streak = cursor.fetchone()[0]
        return render_template('main.html', user_name=user_name, user_streak=user_streak)
    else:
        return redirect(url_for('index'))

# Route to render c1.html
@app.route('/c1')
def c1_page():
    return render_template('c1.html')

# Route to render course.html
@app.route('/course')
def course_page():
    return render_template('course.html')

# Route to render profile.html
@app.route('/profile')
def profile_page():
    if 'user_name' in session:
        user_name = session['user_name']
        db = get_db()
        cursor = db.cursor()
        # Fetch user data for profile display (adjust query as needed)
        cursor.execute('SELECT * FROM users WHERE name = ?', (user_name,))
        user_data = cursor.fetchone()

        # Fetch journal entries for the user
        cursor.execute('SELECT * FROM journal_entries WHERE user_name = ? AND (template_id = ? OR template_id = ?)',
                       (user_name, '1t2', '1t3'))
        entries = cursor.fetchall()

        return render_template('profile.html', user_name=user_name, user_data=user_data, entries=entries)
    else:
        return redirect(url_for('index'))

# Route to render 3t1.html (Journal entry page)
@app.route('/3t1')
def journal_page_3t1():
    return render_template('3t1.html')

# Route to render 3t2.html (Journal entry page)
@app.route('/3t2')
def journal_page_3t2():
    return render_template('3t2.html')
@app.route('/started')
def journal_page_started():
    return render_template('getting.html')
@app.route('/comm')
def journal_page_comm():
    return render_template('communication.html')
@app.route('/example')
def journal_page_example():
    return render_template('example page.html')
# Route to render 2t1.html (Journal entry page)
@app.route('/2t1')
def journal_page_2t1():
    return render_template('2t1.html')

# Route to render 2t2.html (Journal entry page)
@app.route('/2t2')
def journal_page_2t2():
    return render_template('2t2.html')

# Route to render 2t3.html (Journal entry page)
@app.route('/2t3')
def journal_page_2t3():
    return render_template('2t3.html')

# Route to render 1t3.html (Journal entry page)
@app.route('/1t3')
def journal_page_1t3():
    return render_template('1t3.html')

# Route to render 1t4.html (Journal entry page)
@app.route('/1t4')
def journal_page_1t4():
    return render_template('1t4.html')

# Route to render newpage.html
@app.route('/newpage')
def newpage():
    if 'user_name' in session:
        user_name = session['user_name']
        db = get_db()
        cursor = db.cursor()
        
        # Fetch entries with template_id '1t2' or '1t3' for the user
        cursor.execute('SELECT * FROM journal_entries WHERE user_name = ? AND (template_id = ? OR template_id = ?)',
                       (user_name, '1t2', '1t3'))
        entries = cursor.fetchall()
        
        return render_template('newpage.html', entries=entries)
    else:
        return redirect(url_for('index'))

# Route to render 1t2.html (Journal entry page)
@app.route('/1t2')
def journal_page_1t2():
    return render_template('1t2.html')

@app.route('/why')
def journal_page_why():
    return render_template('why.html')

@app.route('/principle')
def journal_page_principle():
    return render_template('execution.html')

@app.route('/team')
def journal_page_team():
    return render_template('team.html')

# Route to render 1t1.html (Journal entry page)
@app.route('/1t1')
def journal_page_1t1():
    return render_template('1t1.html')

# Route to handle journal form submission
@app.route('/submit_journal', methods=['POST'])
def submit_journal():
    template_id = request.form.get('templateId')
    journal_text = request.form.get('journalText')
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_name = session.get('user_name')  # Fetch user's name from session

    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO journal_entries (template_id, text, created_at, user_name)
        VALUES (?, ?, ?, ?)
    ''', (template_id, journal_text, created_at, user_name))
    db.commit()

    return '', 204  # Return no content response

# Route to handle signup form submission
@app.route('/signup_submit', methods=['POST'])
def signup_submit():
    name = request.form.get('name')
    passcode = request.form.get('passcode')

    db = get_db()
    cursor = db.cursor()

    try:
        # Attempt to insert the new user into the database
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            INSERT INTO users (name, passcode, last_login, streak)
            VALUES (?, ?, ?, ?)
        ''', (name, passcode, current_time, 0))
        db.commit()

        flash('Account created successfully! Please log in.')
        return redirect(url_for('index'))
    except sqlite3.IntegrityError:
        flash('This username is already taken. Please choose a different username.')
        return redirect(url_for('index'))

@app.route('/edit')
def journal_entries():
    if 'user_name' in session:
        user_name = session['user_name']
        db = get_db()
        cursor = db.cursor()
        cursor.execute('SELECT * FROM journal_entries WHERE user_name = ?', (user_name,))
        entries = cursor.fetchall()

        return render_template('edit.html', entries=entries)
    else:
        return redirect(url_for('index'))

@app.route('/bookmark_entry/<int:entry_id>')
def bookmark_entry(entry_id):
    if 'user_name' in session:
        # Logic to bookmark the entry (e.g., update the database)
        flash('Entry bookmarked.')
        return redirect(url_for('journal_entries'))
    else:
        return redirect(url_for('index'))

@app.route('/delete_entry/<int:entry_id>')
def delete_entry(entry_id):
    if 'user_name' in session:
        db = get_db()
        cursor = db.cursor()
        cursor.execute('DELETE FROM journal_entries WHERE id = ?', (entry_id,))
        db.commit()
        flash('Entry deleted.')
        return redirect(url_for('journal_entries'))
    else:
        return redirect(url_for('index'))

@app.route('/edit_entry/<int:entry_id>', methods=['POST'])
def edit_entry(entry_id):
    if 'user_name' in session:
        db = get_db()
        cursor = db.cursor()
        
        new_text = request.form.get('journalText')
        cursor.execute('UPDATE journal_entries SET text = ? WHERE id = ?', (new_text, entry_id))
        db.commit()
        flash('Entry updated.')
        return redirect(url_for('journal_entries'))
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
