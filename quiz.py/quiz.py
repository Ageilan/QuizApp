import tkinter as tk
import random
from tkinter import messagebox

# -------------------------
# Quiz Data (15 questions)
# -------------------------
quiz_data = [
    {"question": "What is the capital of France?", "options": ["Paris", "London", "Rome", "Berlin"], "answer": "Paris"},
    {"question": "Which language is known as the language of AI?", "options": ["C++", "Java", "Python", "Ruby"], "answer": "Python"},
    {"question": "Who is the founder of Microsoft?", "options": ["Steve Jobs", "Bill Gates", "Mark Zuckerberg", "Elon Musk"], "answer": "Bill Gates"},
    {"question": "Which keyword is used to define a function in Python?", "options": ["func", "def", "function", "define"], "answer": "def"},
    {"question": "Which of the following is a Python tuple?", "options": ["[1,2,3]", "{1,2,3}", "(1,2,3)", "{ }"], "answer": "(1,2,3)"},
    {"question": "Python lists are enclosed in which brackets?", "options": ["()", "[]", "{}", "<>"], "answer": "[]"},
    {"question": "Which of these is used for single-line comments in Python?", "options": ["#", "//", "/*", "--"], "answer": "#"},
    {"question": "What is the output of 3 + 2 * 2 in Python?", "options": ["10", "7", "8", "9"], "answer": "7"},
    {"question": "What does len('Python') return?", "options": ["5", "6", "7", "Error"], "answer": "6"},
    {"question": "Which of the following is not a Python data type?", "options": ["list", "tuple", "map", "int"], "answer": "map"},
    {"question": "Which operator is used for exponentiation in Python?", "options": ["^", "**", "exp", "pow"], "answer": "**"},
    {"question": "What is the correct way to open a file for reading in Python?", "options": ["open('file.txt','r')", "open('file.txt','w')", "open('file.txt','a')", "open('file.txt','rw')"], "answer": "open('file.txt','r')"},
    {"question": "Python supports which type of programming?", "options": ["Object-Oriented", "Functional", "Procedural", "All of the above"], "answer": "All of the above"},
    {"question": "Which function converts a string to an integer in Python?", "options": ["str()", "int()", "float()", "char()"], "answer": "int()"},
    {"question": "Which of the following is used to create an empty set in Python?", "options": ["{}", "[]", "set()", "()"], "answer": "set()"}
]

time_limit = 10  # seconds per question

# -------------------------
# Global Variables
# -------------------------
score = 0
current_q = 0
timer_id = None
time_left = time_limit

# -------------------------
# Start Screen
# -------------------------
def start_screen():
    global root
    root = tk.Tk()
    root.title("Quiz Registration")
    root.geometry("400x300")

    tk.Label(root, text="Register Number").pack(pady=5)
    reg_entry = tk.Entry(root)
    reg_entry.pack()

    tk.Label(root, text="Name").pack(pady=5)
    name_entry = tk.Entry(root)
    name_entry.pack()

    tk.Label(root, text="Date of Birth (DD/MM/YYYY)").pack(pady=5)
    dob_entry = tk.Entry(root)
    dob_entry.pack()

    tk.Button(root, text="Start Quiz", font=("Arial", 14),
              command=lambda: validate_and_start(reg_entry.get(), name_entry.get(), dob_entry.get())
             ).pack(pady=20)

    root.mainloop()

# -------------------------
# Validate Registration
# -------------------------
def validate_and_start(reg, name, dob):
    if not reg.strip() or not name.strip() or not dob.strip():
        messagebox.showerror("Error", "All fields are mandatory!")
        return
    start_quiz(reg, name, dob)

# -------------------------
# Start Quiz
# -------------------------
def start_quiz(reg, name, dob):
    global quiz, score, current_q, quiz_root
    root.destroy()
    quiz_root = tk.Tk()
    quiz_root.title(f"Quiz App - {name}")
    quiz_root.geometry("500x400")

    # Select 15 random questions
    quiz = random.sample(quiz_data, 15)

    score = 0
    current_q = 0

    # Widgets
    global timer_label, question_label, buttons_frame
    timer_label = tk.Label(quiz_root, text=f"Time left: {time_limit}", font=("Arial", 14))
    timer_label.pack(pady=10)

    question_label = tk.Label(quiz_root, text="", font=("Arial", 16), wraplength=450)
    question_label.pack(pady=20)

    buttons_frame = tk.Frame(quiz_root)
    buttons_frame.pack()

    next_question()

    quiz_root.mainloop()

# -------------------------
# Next Question
# -------------------------
def next_question():
    global current_q, score, time_left, timer_id
    if current_q >= len(quiz):
        show_result()
        return

    q = quiz[current_q]
    question_label.config(text=q["question"])

    # Shuffle options
    options = q["options"][:]
    random.shuffle(options)

    # Clear previous buttons
    for widget in buttons_frame.winfo_children():
        widget.destroy()

    for option in options:
        b = tk.Button(buttons_frame, text=option, width=25, font=("Arial", 12),
                      command=lambda opt=option: check_answer(opt))
        b.pack(pady=5)

    # Reset timer
    time_left = time_limit
    update_timer()

# -------------------------
# Timer Update
# -------------------------
def update_timer():
    global time_left, timer_id, current_q
    timer_label.config(text=f"Time left: {time_left}s")
    if time_left > 0:
        time_left -= 1
        timer_id = quiz_root.after(1000, update_timer)
    else:
        current_q += 1
        next_question()

# -------------------------
# Check Answer
# -------------------------
def check_answer(selected):
    global score, current_q, timer_id
    quiz_root.after_cancel(timer_id)
    if selected == quiz[current_q]["answer"]:
        score += 1
    current_q += 1
    next_question()

# -------------------------
# Show Result
# -------------------------
def show_result():
    for widget in quiz_root.winfo_children():
        widget.destroy()
    tk.Label(quiz_root, text=f"Quiz Finished!\nYour Score: {score}/{len(quiz)}", font=("Arial", 16)).pack(pady=40)
    tk.Button(quiz_root, text="Restart Quiz", font=("Arial", 12),
              command=lambda: [quiz_root.destroy(), start_screen()]).pack(pady=10)
    tk.Button(quiz_root, text="End Test", font=("Arial", 12),
              command=quiz_root.destroy).pack(pady=10)

# -------------------------
# Start App
# -------------------------
if __name__ == "__main__":
    start_screen()
