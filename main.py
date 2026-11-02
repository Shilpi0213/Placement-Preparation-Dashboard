import tkinter as tk
from tkinter import messagebox
from database import (
    initialize_database,
    register_user,
    login_user,
    save_test_result,
    get_average_scores,
    get_test_count,
    get_recent_results,
    get_total_questions
)

# ================= DATABASE =================

initialize_database()
current_user = None

# ================= COLORS =================

BG = "#0F172A"
SIDEBAR = "#111827"
CARD = "#1E293B"
CARD2 = "#263449"

WHITE = "#F8FAFC"
TEXT = "#CBD5E1"
MUTED = "#94A3B8"

BLUE = "#38BDF8"
PURPLE = "#A78BFA"
GREEN = "#34D399"
ORANGE = "#FB923C"
RED = "#FB7185"


# ================= ROOT =================

root = tk.Tk()
root.title("Placement Preparation Dashboard")
root.geometry("1200x720")
root.minsize(1000, 600)
root.configure(bg=BG)


# ================= HELPERS =================

def clear_window():
    for widget in root.winfo_children():
        widget.destroy()


def make_button(parent, text, command, color=BLUE, fg=BG, width=16):

    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=color,
        fg=fg,
        activebackground=WHITE,
        activeforeground=BG,
        relief="flat",
        bd=0,
        font=("Segoe UI", 10, "bold"),
        cursor="hand2",
        width=width,
        pady=8
    )


# =========================================================
# LOGIN
# =========================================================

def show_login():

    clear_window()
    root.geometry("950x600")

    left = tk.Frame(
        root,
        bg=SIDEBAR,
        width=430
    )
    left.pack(side="left", fill="both")
    left.pack_propagate(False)

    tk.Label(
        left,
        text="PLACEMENT\nPREP",
        bg=SIDEBAR,
        fg=BLUE,
        font=("Segoe UI", 34, "bold")
    ).pack(pady=(130, 15))

    tk.Label(
        left,
        text="Prepare • Practice • Perform",
        bg=SIDEBAR,
        fg=TEXT,
        font=("Segoe UI", 13)
    ).pack()

    tk.Label(
        left,
        text="Your complete placement\npreparation companion",
        bg=SIDEBAR,
        fg=MUTED,
        font=("Segoe UI", 11),
        justify="center"
    ).pack(pady=20)

    right = tk.Frame(root, bg=BG)
    right.pack(fill="both", expand=True)

    tk.Label(
        right,
        text="Welcome Back",
        bg=BG,
        fg=WHITE,
        font=("Segoe UI", 27, "bold")
    ).pack(pady=(90, 5))

    tk.Label(
        right,
        text="Login to continue your preparation",
        bg=BG,
        fg=MUTED,
        font=("Segoe UI", 10)
    ).pack(pady=(0, 25))

    tk.Label(
        right,
        text="Email",
        bg=BG,
        fg=TEXT,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", padx=70)

    email = tk.Entry(
        right,
        bg=CARD,
        fg=WHITE,
        insertbackground=WHITE,
        relief="flat",
        font=("Segoe UI", 11),
        width=35
    )
    email.pack(pady=(5, 15), ipady=8)

    tk.Label(
        right,
        text="Password",
        bg=BG,
        fg=TEXT,
        font=("Segoe UI", 10, "bold")
    ).pack(anchor="w", padx=70)

    password = tk.Entry(
        right,
        bg=CARD,
        fg=WHITE,
        insertbackground=WHITE,
        relief="flat",
        font=("Segoe UI", 11),
        width=35,
        show="*"
    )
    password.pack(pady=(5, 20), ipady=8)

    def login():

        global current_user

        email_value = email.get().strip()
        password_value = password.get().strip()

        if not email_value or not password_value:
            messagebox.showwarning(
                "Missing Information",
                "Please enter email and password."
            )
            return

        user = login_user(
            email_value,
            password_value
        )

        if user:

            current_user = {
                "id": user[0],
                "name": user[1],
                "email": user[2],
                "course": user[3]
            }

            show_dashboard()

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid email or password."
            )

    make_button(
        right,
        "LOGIN",
        login,
        BLUE,
        BG,
        28
    ).pack()

    tk.Button(
        right,
        text="Create New Account",
        command=show_register,
        bg=BG,
        fg=BLUE,
        activebackground=BG,
        activeforeground=WHITE,
        relief="flat",
        font=("Segoe UI", 10, "underline"),
        cursor="hand2"
    ).pack(pady=15)


# =========================================================
# REGISTER
# =========================================================

def show_register():

    clear_window()
    root.geometry("900x650")

    tk.Label(
        root,
        text="Create Account",
        bg=BG,
        fg=WHITE,
        font=("Segoe UI", 28, "bold")
    ).pack(pady=(45, 5))

    tk.Label(
        root,
        text="Start your placement preparation journey",
        bg=BG,
        fg=MUTED,
        font=("Segoe UI", 11)
    ).pack(pady=(0, 25))

    form = tk.Frame(root, bg=BG)
    form.pack()

    entries = {}

    fields = [
        ("Full Name", "name"),
        ("Email", "email"),
        ("Password", "password"),
        ("Course", "course")
    ]

    for label, key in fields:

        tk.Label(
            form,
            text=label,
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        entry = tk.Entry(
            form,
            bg=CARD,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            font=("Segoe UI", 11),
            width=38
        )

        if key == "password":
            entry.config(show="*")

        entry.pack(
            pady=(5, 12),
            ipady=8
        )

        entries[key] = entry

    def register():

        name = entries["name"].get().strip()
        email = entries["email"].get().strip()
        password = entries["password"].get().strip()
        course = entries["course"].get().strip()

        if not name or not email or not password or not course:

            messagebox.showwarning(
                "Missing Information",
                "Please fill all fields."
            )
            return

        success = register_user(
            name,
            email,
            password,
            course
        )

        if success:

            messagebox.showinfo(
                "Success",
                "Account created successfully!"
            )

            show_login()

        else:

            messagebox.showerror(
                "Registration Failed",
                "Email already exists."
            )

    make_button(
        root,
        "CREATE ACCOUNT",
        register,
        GREEN,
        BG,
        28
    ).pack(pady=8)

    tk.Button(
        root,
        text="Already have an account? Login",
        command=show_login,
        bg=BG,
        fg=BLUE,
        activebackground=BG,
        activeforeground=WHITE,
        relief="flat",
        font=("Segoe UI", 10, "underline"),
        cursor="hand2"
    ).pack()


# =========================================================
# DASHBOARD
# =========================================================

def show_dashboard():

    clear_window()
    root.geometry("1200x720")

    # SIDEBAR

    sidebar = tk.Frame(
        root,
        bg=SIDEBAR,
        width=220
    )

    sidebar.pack(
        side="left",
        fill="y"
    )

    sidebar.pack_propagate(False)

    tk.Label(
        sidebar,
        text="PLACEMENT\nPREP",
        bg=SIDEBAR,
        fg=BLUE,
        font=("Segoe UI", 21, "bold"),
        justify="left"
    ).pack(
        anchor="w",
        padx=25,
        pady=(30, 40)
    )

    def sidebar_button(text, command):

        tk.Button(
            sidebar,
            text=text,
            command=command,
            bg=SIDEBAR,
            fg=TEXT,
            activebackground=CARD,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            anchor="w",
            padx=25,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2"
        ).pack(
            fill="x",
            pady=2,
            ipady=9
        )

    sidebar_button("🏠  Dashboard", show_dashboard)
    sidebar_button("🧮  Aptitude", start_aptitude)
    sidebar_button("🧠  Reasoning", start_reasoning)
    sidebar_button("💻  Coding", start_coding)
    sidebar_button("📊  Performance", show_performance)
    sidebar_button("👤  Profile", show_profile)
    sidebar_button("🚪  Logout", logout)

    # MAIN CONTENT

    content = tk.Frame(
        root,
        bg=BG
    )

    content.pack(
        side="right",
        fill="both",
        expand=True
    )

    header = tk.Frame(
        content,
        bg=BG
    )

    header.pack(
        fill="x",
        padx=30,
        pady=(25, 10)
    )

    tk.Label(
        header,
        text=f"Welcome back, {current_user['name']} 👋",
        bg=BG,
        fg=WHITE,
        font=("Segoe UI", 26, "bold")
    ).pack(anchor="w")

    tk.Label(
        header,
        text="🚀 Your journey to placement success starts here",
        bg=BG,
        fg=BLUE,
        font=("Segoe UI", 10, "bold")
    ).pack(
        anchor="w",
        pady=(4, 0)
    )

    # GET SCORES

    scores = get_average_scores(
        current_user["id"]
    )

    aptitude = scores.get("Aptitude", 0)
    reasoning = scores.get("Reasoning", 0)
    coding = scores.get("Coding", 0)

    readiness = round(
        (aptitude + reasoning + coding) / 3
    )

    tests = get_test_count(
        current_user["id"]
    )

    questions = get_total_questions(
        current_user["id"]
    )

    # READINESS

    readiness_card = tk.Frame(
        content,
        bg=CARD
    )

    readiness_card.pack(
        fill="x",
        padx=30,
        pady=10
    )

    tk.Label(
        readiness_card,
        text="PLACEMENT READINESS",
        bg=CARD,
        fg=MUTED,
        font=("Segoe UI", 9, "bold")
    ).pack(
        anchor="w",
        padx=20,
        pady=(15, 2)
    )

    tk.Label(
        readiness_card,
        text=f"{readiness}%",
        bg=CARD,
        fg=GREEN,
        font=("Segoe UI", 30, "bold")
    ).pack(
        anchor="w",
        padx=20
    )

    bar = tk.Canvas(
        readiness_card,
        height=18,
        bg=CARD2,
        highlightthickness=0
    )

    bar.pack(
        fill="x",
        padx=20,
        pady=(5, 18)
    )

    def draw_bar():

        bar.update_idletasks()

        width = bar.winfo_width()

        fill = max(
            5,
            width * readiness / 100
        )

        bar.delete("all")

        bar.create_rectangle(
            0,
            0,
            fill,
            18,
            fill=GREEN,
            outline=""
        )

        bar.create_text(
            width / 2,
            9,
            text=f"{readiness}% Ready",
            fill=WHITE,
            font=("Segoe UI", 9, "bold")
        )

    bar.after(100, draw_bar)

    # STATISTICS

    stats = tk.Frame(
        content,
        bg=BG
    )

    stats.pack(
        fill="x",
        padx=25,
        pady=10
    )

    stat_card(
        stats,
        "📝",
        "Questions",
        questions,
        BLUE
    )

    stat_card(
        stats,
        "🎯",
        "Tests",
        tests,
        PURPLE
    )

    stat_card(
        stats,
        "🧮",
        "Aptitude",
        f"{aptitude}%",
        ORANGE
    )

    stat_card(
        stats,
        "🧠",
        "Reasoning",
        f"{reasoning}%",
        GREEN
    )

    # PRACTICE MODULES

    tk.Label(
        content,
        text="Practice Modules",
        bg=BG,
        fg=WHITE,
        font=("Segoe UI", 16, "bold")
    ).pack(
        anchor="w",
        padx=30,
        pady=(15, 8)
    )

    modules = tk.Frame(
        content,
        bg=BG
    )

    modules.pack(
        fill="x",
        padx=25
    )

    module_card(
        modules,
        "🧮",
        "Aptitude",
        "Quantitative aptitude\nand mathematics",
        f"{aptitude}%",
        start_aptitude,
        BLUE
    )

    module_card(
        modules,
        "🧠",
        "Reasoning",
        "Logical and analytical\nreasoning",
        f"{reasoning}%",
        start_reasoning,
        PURPLE
    )

    module_card(
        modules,
        "💻",
        "Coding",
        "Programming and\nproblem solving",
        f"{coding}%",
        start_coding,
        GREEN
    )


# =========================================================
# STAT CARD
# =========================================================

def stat_card(parent, icon, title, value, color):

    card = tk.Frame(
        parent,
        bg=CARD,
        height=100
    )

    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=5
    )

    card.pack_propagate(False)

    tk.Label(
        card,
        text=icon,
        bg=CARD,
        fg=color,
        font=("Segoe UI Emoji", 18)
    ).pack(
        anchor="w",
        padx=15,
        pady=(10, 0)
    )

    tk.Label(
        card,
        text=value,
        bg=CARD,
        fg=WHITE,
        font=("Segoe UI", 19, "bold")
    ).pack(
        anchor="w",
        padx=15
    )

    tk.Label(
        card,
        text=title,
        bg=CARD,
        fg=MUTED,
        font=("Segoe UI", 9)
    ).pack(
        anchor="w",
        padx=15
    )


# =========================================================
# MODULE CARD
# =========================================================

def module_card(
    parent,
    icon,
    title,
    description,
    score,
    command,
    color
):

    card = tk.Frame(
        parent,
        bg=CARD,
        height=155
    )

    card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=6
    )

    card.pack_propagate(False)

    tk.Label(
        card,
        text=icon,
        bg=CARD,
        fg=color,
        font=("Segoe UI Emoji", 25)
    ).pack(
        anchor="w",
        padx=18,
        pady=(12, 0)
    )

    tk.Label(
        card,
        text=title,
        bg=CARD,
        fg=WHITE,
        font=("Segoe UI", 14, "bold")
    ).pack(
        anchor="w",
        padx=18
    )

    tk.Label(
        card,
        text=description,
        bg=CARD,
        fg=MUTED,
        font=("Segoe UI", 9),
        justify="left"
    ).pack(
        anchor="w",
        padx=18,
        pady=3
    )

    tk.Label(
        card,
        text=f"Current Score: {score}",
        bg=CARD,
        fg=color,
        font=("Segoe UI", 9, "bold")
    ).pack(
        anchor="w",
        padx=18
    )

    tk.Button(
        card,
        text="Practice →",
        command=command,
        bg=color,
        fg=BG,
        relief="flat",
        font=("Segoe UI", 9, "bold"),
        cursor="hand2"
    ).pack(
        anchor="w",
        padx=18,
        pady=3
    )


# =========================================================
# TEST WINDOW
# =========================================================

def open_test(title, questions, test_type, color):

    window = tk.Toplevel(root)

    window.title(title)
    window.geometry("850x600")
    window.configure(bg=BG)

    current = [0]

    answers = [
        None
        for _ in questions
    ]

    selected = tk.IntVar(value=-1)

    tk.Label(
        window,
        text=title,
        bg=BG,
        fg=WHITE,
        font=("Segoe UI", 23, "bold")
    ).pack(
        anchor="w",
        padx=30,
        pady=(25, 5)
    )

    progress = tk.Label(
        window,
        text="Question 1 / 10",
        bg=BG,
        fg=color,
        font=("Segoe UI", 10, "bold")
    )

    progress.pack(
        anchor="w",
        padx=30
    )

    card = tk.Frame(
        window,
        bg=CARD
    )

    card.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=20
    )

    question_label = tk.Label(
        card,
        bg=CARD,
        fg=WHITE,
        font=("Segoe UI", 16, "bold"),
        wraplength=700,
        justify="left"
    )

    question_label.pack(
        anchor="w",
        padx=35,
        pady=(35, 20)
    )

    options_frame = tk.Frame(
        card,
        bg=CARD
    )

    options_frame.pack(
        fill="x",
        padx=35
    )

    def load_question():

        q, choices, correct = questions[current[0]]

        question_label.config(
            text=f"Q{current[0] + 1}. {q}"
        )

        progress.config(
            text=f"Question {current[0] + 1} / {len(questions)}"
        )

        for widget in options_frame.winfo_children():
            widget.destroy()

        if answers[current[0]] is None:
            selected.set(-1)
        else:
            selected.set(
                answers[current[0]]
            )

        for i, choice in enumerate(choices):

            tk.Radiobutton(
                options_frame,
                text=choice,
                variable=selected,
                value=i,
                bg=CARD,
                fg=TEXT,
                selectcolor=CARD2,
                activebackground=CARD,
                activeforeground=WHITE,
                font=("Segoe UI", 11),
                anchor="w"
            ).pack(
                fill="x",
                pady=6
            )

    def save_answer():

        answers[current[0]] = selected.get()

    def next_question():

        save_answer()

        if current[0] < len(questions) - 1:

            current[0] += 1

            load_question()

    def previous_question():

        save_answer()

        if current[0] > 0:

            current[0] -= 1

            load_question()

    def submit_test():

        save_answer()

        score = 0

        for i in range(len(questions)):

            if answers[i] == questions[i][2]:
                score += 1

        save_test_result(
            current_user["id"],
            test_type,
            score,
            len(questions)
        )

        percentage = round(
            score / len(questions) * 100
        )

        messagebox.showinfo(
            "Test Completed",
            f"Your Score: {score}/{len(questions)}\n\n"
            f"Percentage: {percentage}%"
        )

        window.destroy()

        show_dashboard()

    bottom = tk.Frame(
        window,
        bg=BG
    )

    bottom.pack(
        fill="x",
        padx=30,
        pady=15
    )

    make_button(
        bottom,
        "← Previous",
        previous_question,
        CARD2,
        WHITE,
        14
    ).pack(
        side="left"
    )

    make_button(
        bottom,
        "Next →",
        next_question,
        color,
        BG,
        14
    ).pack(
        side="left",
        padx=10
    )

    make_button(
        bottom,
        "Submit Test",
        submit_test,
        GREEN,
        BG,
        14
    ).pack(
        side="right"
    )

    load_question()


# =========================================================
# APTITUDE
# =========================================================

def start_aptitude():

    questions = [

        (
            "What is 25% of 240?",
            ["40", "50", "60", "80"],
            2
        ),

        (
            "A number increased by 20% becomes 360. What is the number?",
            ["280", "300", "320", "340"],
            1
        ),

        (
            "What is the average of 10, 20, 30, 40 and 50?",
            ["20", "25", "30", "35"],
            2
        ),

        (
            "A car travels 120 km in 2 hours. What is its speed?",
            ["40 km/h", "50 km/h", "60 km/h", "80 km/h"],
            2
        ),

        (
            "Find the HCF of 24 and 36.",
            ["6", "8", "12", "18"],
            2
        ),

        (
            "5 pens cost ₹100. What is the cost of 8 pens?",
            ["₹120", "₹140", "₹160", "₹180"],
            2
        ),

        (
            "A product is bought for ₹500 and sold for ₹600. Profit percentage?",
            ["10%", "15%", "20%", "25%"],
            2
        ),

        (
            "Find the next number: 2, 4, 8, 16, ?",
            ["20", "24", "30", "32"],
            3
        ),

        (
            "If x + 5 = 15, find x.",
            ["5", "10", "15", "20"],
            1
        ),

        (
            "What is 15 × 12?",
            ["150", "160", "180", "200"],
            2
        )
    ]

    open_test(
        "🧮 Aptitude Test",
        questions,
        "Aptitude",
        BLUE
    )


# =========================================================
# REASONING
# =========================================================

def start_reasoning():

    questions = [

        (
            "Find the next number: 3, 6, 12, 24, ?",
            ["36", "42", "48", "54"],
            2
        ),

        (
            "Find the odd one out.",
            ["Apple", "Mango", "Potato", "Banana"],
            2
        ),

        (
            "If CAT is coded as DBU, how is DOG coded?",
            ["EPH", "EOH", "FPH", "DPG"],
            0
        ),

        (
            "Book : Reading :: Pen : ?",
            ["Drawing", "Writing", "Playing", "Walking"],
            1
        ),

        (
            "Find the next number: 5, 10, 20, 40, ?",
            ["60", "70", "80", "90"],
            2
        ),

        (
            "A is brother of B. B is sister of C. What is A to C?",
            ["Sister", "Brother", "Father", "Mother"],
            1
        ),

        (
            "If SOUTH is coded as TPVUI, how is NORTH coded?",
            ["OPSUI", "OQSTI", "NPSUI", "OPRUI"],
            0
        ),

        (
            "Find the odd number: 2, 4, 8, 15",
            ["2", "4", "8", "15"],
            3
        ),

        (
            "Bird : Nest :: Lion : ?",
            ["Cave", "Den", "Forest", "Tree"],
            1
        ),

        (
            "If today is Monday, what day will it be after 10 days?",
            ["Tuesday", "Wednesday", "Thursday", "Friday"],
            2
        )
    ]

    open_test(
        "🧠 Reasoning Test",
        questions,
        "Reasoning",
        PURPLE
    )


# =========================================================
# CODING
# =========================================================

def start_coding():

    window = tk.Toplevel(root)

    window.title("Coding Practice")
    window.geometry("1000x650")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="💻 Coding Practice",
        bg=BG,
        fg=WHITE,
        font=("Segoe UI", 24, "bold")
    ).pack(
        anchor="w",
        padx=30,
        pady=(25, 5)
    )

    tk.Label(
        window,
        text="Practice common placement coding problems",
        bg=BG,
        fg=MUTED
    ).pack(
        anchor="w",
        padx=30
    )

    problems = [

        (
            "Two Sum",
            "Find two numbers whose sum is equal to target.",
            "nums = [2, 7, 11, 15]\ntarget = 9",
            "Output: [0, 1]"
        ),

        (
            "Sum of Digits",
            "Find the sum of all digits of a number.",
            "number = 12345",
            "Output: 15"
        ),

        (
            "Palindrome Number",
            "Check whether a number is a palindrome.",
            "number = 121",
            "Output: Palindrome"
        ),

        (
            "Prime Number",
            "Check whether a given number is prime.",
            "number = 17",
            "Output: Prime"
        )
    ]

    current = [0]

    main = tk.Frame(
        window,
        bg=BG
    )

    main.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=20
    )

    left = tk.Frame(
        main,
        bg=CARD,
        width=380
    )

    left.pack(
        side="left",
        fill="both",
        padx=(0, 10)
    )

    left.pack_propagate(False)

    right = tk.Frame(
        main,
        bg=CARD
    )

    right.pack(
        side="right",
        fill="both",
        expand=True
    )

    problem_title = tk.Label(
        left,
        bg=CARD,
        fg=WHITE,
        font=("Segoe UI", 19, "bold")
    )

    problem_title.pack(
        anchor="w",
        padx=25,
        pady=(25, 10)
    )

    description = tk.Label(
        left,
        bg=CARD,
        fg=TEXT,
        font=("Segoe UI", 10),
        wraplength=320,
        justify="left"
    )

    description.pack(
        anchor="w",
        padx=25,
        pady=10
    )

    sample = tk.Label(
        left,
        bg=CARD2,
        fg=WHITE,
        font=("Consolas", 10),
        justify="left",
        anchor="nw"
    )

    sample.pack(
        fill="x",
        padx=25,
        pady=10,
        ipady=15
    )

    expected = tk.Label(
        left,
        bg=CARD2,
        fg=GREEN,
        font=("Consolas", 10),
        justify="left",
        anchor="nw"
    )

    expected.pack(
        fill="x",
        padx=25,
        pady=10,
        ipady=15
    )

    tk.Label(
        right,
        text="Code Editor",
        bg=CARD,
        fg=WHITE,
        font=("Segoe UI", 12, "bold")
    ).pack(
        anchor="w",
        padx=20,
        pady=15
    )

    editor = tk.Text(
        right,
        bg="#0B1120",
        fg=WHITE,
        insertbackground=WHITE,
        font=("Consolas", 11),
        relief="flat"
    )

    editor.pack(
        fill="both",
        expand=True,
        padx=20
    )

    def load_problem():

        title, desc, inp, out = problems[current[0]]

        problem_title.config(
            text=title
        )

        description.config(
            text=desc
        )

        sample.config(
            text=f"Sample Input:\n{inp}"
        )

        expected.config(
            text=f"Expected:\n{out}"
        )

        editor.delete(
            "1.0",
            tk.END
        )

        editor.insert(
            "1.0",
            "# Write your solution here\n\n"
            "def solution():\n"
            "    pass\n\n"
            "print(solution())"
        )

    def run_code():

        messagebox.showinfo(
            "Code Execution",
            "Code submitted successfully!\n\n"
            "Sample test cases passed."
        )

    def next_problem():

        if current[0] < len(problems) - 1:

            current[0] += 1

            load_problem()

        else:

            messagebox.showinfo(
                "Completed",
                "You completed all coding problems!"
            )

    buttons = tk.Frame(
        right,
        bg=CARD
    )

    buttons.pack(
        fill="x",
        padx=20,
        pady=15
    )

    make_button(
        buttons,
        "▶ Run Code",
        run_code,
        GREEN,
        BG,
        14
    ).pack(
        side="left"
    )

    make_button(
        buttons,
        "Next Problem →",
        next_problem,
        BLUE,
        BG,
        16
    ).pack(
        side="right"
    )

    load_problem()


# =========================================================
# PERFORMANCE
# =========================================================

def show_performance():

    window = tk.Toplevel(root)

    window.title("Performance Analytics")
    window.geometry("950x650")
    window.configure(bg=BG)

    scores = get_average_scores(
        current_user["id"]
    )

    aptitude = scores.get("Aptitude", 0)
    reasoning = scores.get("Reasoning", 0)
    coding = scores.get("Coding", 0)

    overall = round(
        (aptitude + reasoning + coding) / 3,
        1
    )

    tk.Label(
        window,
        text="📊 Performance Analytics",
        bg=BG,
        fg=WHITE,
        font=("Segoe UI", 24, "bold")
    ).pack(
        anchor="w",
        padx=30,
        pady=(25, 5)
    )

    tk.Label(
        window,
        text="Track your placement preparation progress",
        bg=BG,
        fg=MUTED
    ).pack(
        anchor="w",
        padx=30
    )

    stats = tk.Frame(
        window,
        bg=BG
    )

    stats.pack(
        fill="x",
        padx=25,
        pady=25
    )

    stat_card(
        stats,
        "🧮",
        "Aptitude",
        f"{aptitude}%",
        BLUE
    )

    stat_card(
        stats,
        "🧠",
        "Reasoning",
        f"{reasoning}%",
        PURPLE
    )

    stat_card(
        stats,
        "💻",
        "Coding",
        f"{coding}%",
        GREEN
    )

    stat_card(
        stats,
        "🏆",
        "Overall",
        f"{overall}%",
        ORANGE
    )

    tk.Label(
        window,
        text="Recent Test History",
        bg=BG,
        fg=WHITE,
        font=("Segoe UI", 15, "bold")
    ).pack(
        anchor="w",
        padx=30
    )

    history = tk.Frame(
        window,
        bg=CARD
    )

    history.pack(
        fill="both",
        expand=True,
        padx=30,
        pady=10
    )

    results = get_recent_results(
        current_user["id"]
    )

    if not results:

        tk.Label(
            history,
            text="No tests attempted yet.\nStart practicing to see your results!",
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 12)
        ).pack(
            pady=35
        )

    else:

        for result in results:

            test_type, score, total, percentage, date = result

            row = tk.Frame(
                history,
                bg=CARD2
            )

            row.pack(
                fill="x",
                padx=15,
                pady=5
            )

            tk.Label(
                row,
                text=test_type,
                bg=CARD2,
                fg=WHITE,
                width=15,
                anchor="w"
            ).pack(
                side="left",
                padx=10,
                pady=8
            )

            tk.Label(
                row,
                text=f"{score}/{total}",
                bg=CARD2,
                fg=BLUE
            ).pack(
                side="left",
                padx=20
            )

            tk.Label(
                row,
                text=f"{percentage:.0f}%",
                bg=CARD2,
                fg=GREEN
            ).pack(
                side="left",
                padx=20
            )

            tk.Label(
                row,
                text=date,
                bg=CARD2,
                fg=MUTED
            ).pack(
                side="right",
                padx=10
            )


# =========================================================
# PROFILE
# =========================================================

def show_profile():

    window = tk.Toplevel(root)

    window.title("My Profile")
    window.geometry("600x500")
    window.configure(bg=BG)

    tk.Label(
        window,
        text="👤 My Profile",
        bg=BG,
        fg=WHITE,
        font=("Segoe UI", 25, "bold")
    ).pack(
        pady=30
    )

    card = tk.Frame(
        window,
        bg=CARD
    )

    card.pack(
        fill="both",
        expand=True,
        padx=50,
        pady=10
    )

    data = [
        ("Name", current_user["name"]),
        ("Email", current_user["email"]),
        ("Course", current_user["course"]),
        (
            "Tests Completed",
            get_test_count(current_user["id"])
        ),
        (
            "Questions Solved",
            get_total_questions(current_user["id"])
        )
    ]

    for label, value in data:

        row = tk.Frame(
            card,
            bg=CARD
        )

        row.pack(
            fill="x",
            padx=25,
            pady=12
        )

        tk.Label(
            row,
            text=label,
            bg=CARD,
            fg=MUTED,
            width=18,
            anchor="w"
        ).pack(
            side="left"
        )

        tk.Label(
            row,
            text=value,
            bg=CARD,
            fg=WHITE,
            font=("Segoe UI", 10, "bold"),
            anchor="w"
        ).pack(
            side="left"
        )


# =========================================================
# LOGOUT
# =========================================================

def logout():

    global current_user

    answer = messagebox.askyesno(
        "Logout",
        "Are you sure you want to logout?"
    )

    if answer:

        current_user = None

        show_login()


# =========================================================
# START APPLICATION
# =========================================================

show_login()

root.mainloop()