import sqlite3
from datetime import datetime


DB_NAME = "placement.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    return sqlite3.connect(DB_NAME)


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            course TEXT,
            created_at TEXT
        )
    """)

    # Test results table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            test_type TEXT,
            score INTEGER,
            total INTEGER,
            percentage REAL,
            attempted_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


# =========================================================
# REGISTER USER
# =========================================================

def register_user(name, email, password, course):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            INSERT INTO users
            (name, email, password, course, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            name,
            email,
            password,
            course,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


# =========================================================
# LOGIN USER
# =========================================================

def login_user(email, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, course
        FROM users
        WHERE email = ? AND password = ?
    """, (
        email,
        password
    ))

    user = cursor.fetchone()

    conn.close()

    return user


# =========================================================
# SAVE TEST RESULT
# =========================================================

def save_test_result(user_id, test_type, score, total):

    percentage = (score / total) * 100

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO test_results
        (user_id, test_type, score, total, percentage, attempted_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        test_type,
        score,
        total,
        percentage,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


# =========================================================
# GET AVERAGE SCORES
# =========================================================

def get_average_scores(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT test_type, AVG(percentage)
        FROM test_results
        WHERE user_id = ?
        GROUP BY test_type
    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    scores = {}

    for test_type, average in rows:

        scores[test_type] = round(average, 1)

    return scores


# =========================================================
# GET TEST COUNT
# =========================================================

def get_test_count(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM test_results
        WHERE user_id = ?
    """, (user_id,))

    count = cursor.fetchone()[0]

    conn.close()

    return count


# =========================================================
# GET RECENT RESULTS
# =========================================================

def get_recent_results(user_id, limit=6):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT test_type,
               score,
               total,
               percentage,
               attempted_at
        FROM test_results
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
    """, (
        user_id,
        limit
    ))

    results = cursor.fetchall()

    conn.close()

    return results


# =========================================================
# GET TOTAL QUESTIONS
# =========================================================

def get_total_questions(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(score), 0)
        FROM test_results
        WHERE user_id = ?
    """, (user_id,))

    total = cursor.fetchone()[0]

    conn.close()

    return total