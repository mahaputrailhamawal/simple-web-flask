from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def get_db_connection():
    return mysql.connector.connect(
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )

def create_user_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(25) NOT NULL UNIQUE,
            password VARCHAR(12) NOT NULL
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

def create_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')"
        cursor.execute(query)
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def get_user(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = f"SELECT * FROM users WHERE username = '{username}'"
        cursor.execute(query)
        user = cursor.fetchone()
        return user
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()
@app.route('/')
def index():
    if 'username' in session:
        return f"Hello, {session['username']}!"
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        create_user(username, password)
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        
        if user and user[2] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    create_user_table()
    app.run(host="0.0.0.0", debug=True)