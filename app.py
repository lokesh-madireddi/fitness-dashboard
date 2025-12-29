from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date

app = Flask(__name__)
DB_NAME = "fitness.db" 

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fitness (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            steps INTEGER,
            workout TEXT,
            calories INTEGER,
            weight REAL,
            notes TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        steps = request.form["steps"]
        workout = request.form["workout"]
        calories = request.form["calories"]
        weight = request.form["weight"]
        notes = request.form["notes"]

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO fitness (date, steps, workout, calories, weight, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (date.today(), steps, workout, calories, weight, notes))
        conn.commit()
        conn.close()

        return redirect("/")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fitness ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()

    return render_template("index.html", data=data)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
