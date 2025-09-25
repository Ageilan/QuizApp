import tkinter as tk
import random

# Quiz data
quiz_data = [
    {"question": "What is the capital of France?", "options": ["Paris", "London", "Rome", "Berlin"], "answer": "Paris"},
    {"question": "Which language is known as the language of AI?", "options": ["C++", "Java", "Python", "Ruby"], "answer": "Python"},
    {"question": "Who is the founder of Microsoft?", "options": ["Steve Jobs", "Bill Gates", "Mark Zuckerberg", "Elon Musk"], "answer": "Bill Gates"}
]

time_limit = 10  # seconds per question

# Global variables
score = 0
current_q = 0
timer_id = None
time_left = time_limit

# Create main window
root = tk.Tk()
root.title("Quiz App with Timer")
root.geometry("500x350")

# Widgets
timer_label = tk.Label(root, text=f"Time left: {time_limit}", font=("Arial", 14))
question_label = tk.Label(root, text="", font=("Arial", 16), wraplength=400)
buttons_frame = tk.Frame(root)
start_button = tk.Button(root, text="Start Quiz", font=("Arial", 14), width=20)
restart_button = tk.Button(root, text="Restart Quiz", font=("Arial", 14), width=20)

# Functions
def start_quiz():
    global quiz, score, current_q
    quiz = quiz_data[:]
    random.shuffle(quiz)  # Randomize questions
    score = 0
    current_q = 0

    start_button.pack_forget()
    restart_button.pack_forget()
    timer_label.pack(pady=10)
    question_label.pack(pady=20)
    buttons_frame.pack()
    next_question()

def next_question():
    global current_q, score, time_left, timer_id
    if current_q >= len(quiz):
        question_label.config(text=f"Quiz Finished! Your final score is {score}/{len(quiz)}")
        timer_label.pack_forget()
        for widget in buttons_frame.winfo_children():
            widget.destroy()
        restart_button.pack(pady=20)
        return

    q = quiz[current_q]
    question_label.config(text=q["question"])

    # Shuffle options
    options = q["options"][:]
    random.shuffle(options)

    for widget in buttons_frame.winfo_children():
        widget.destroy()

    for option in options:
        b = tk.Button(buttons_frame, text=option, width=20, command=lambda opt=option: check_answer(opt))
        b.pack(pady=5)

    # Reset timer
    global time_left
    time_left = time_limit
    update_timer()

def update_timer():
    global time_left, timer_id, current_q
    timer_label.config(text=f"Time left: {time_left}")
    if time_left > 0:
        time_left -= 1
        timer_id = root.after(1000, update_timer)
    else:
        # Time's up → move to next question
        global current_q
        current_q += 1
        next_question()

def check_answer(selected):
    global score, current_q, timer_id
    root.after_cancel(timer_id)
    if selected == quiz[current_q]["answer"]:
        score += 1
    current_q += 1
    next_question()

# Bind buttons
start_button.config(command=start_quiz)
restart_button.config(command=start_quiz)

# Show start button
start_button.pack(pady=100)

root.mainloop()