import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import datetime
import sqlite3
import pygame
import time


# Create the tasks table in the database
def create_table():
    conn = sqlite3.connect("hackplanner.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task_name TEXT, task_date DATE)")
    conn.commit()
    conn.close()

# Add a task to the database
def add_task():
    task_name = task_name_entry.get()
    task_date = task_date_entry.get_date()
    if task_name.strip() != '':
        conn = sqlite3.connect("hackplanner.db")
        c = conn.cursor()
        c.execute("INSERT INTO tasks (task_name, task_date) VALUES (?, ?)", (task_name, task_date.strftime('%Y-%m-%d')))
        conn.commit()
        conn.close()
        task_list.insert(tk.END, f"{task_name} - {task_date.strftime('%Y-%m-%d')}")
        task_name_entry.delete(0, tk.END)
        task_date_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Task name cannot be empty!")

# Retrieve tasks from the database
def retrieve_tasks():
    conn = sqlite3.connect("hackplanner.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()
    conn.close()
    for task in tasks:
        task_list.insert(tk.END, f"{task[1]} - {task[2]}")

def set_reminder():
    selected_task = task_list.curselection()
    if len(selected_task) > 0:
        task = task_list.get(selected_task[0])
        task_name, task_date = task.split(" - ")
        date_obj = datetime.datetime.strptime(task_date, "%Y-%m-%d").date()
        today = datetime.date.today()
        if date_obj >= today:
            days_left = (date_obj - today).days
            messagebox.showinfo("Reminder Set", f"Reminder set for Task '{task_name}'\nDays Left: {days_left}")
        else:
            messagebox.showinfo("Reminder Set", f"Reminder set for Task '{task_name}' (Past Due Date)")
    else:
        messagebox.showwarning("Warning", "Please select a task from the list!")


def set_alarm():
    alarm_time = alarm_time_entry.get()
    if alarm_time.strip() != '':
        try:
            current_time = datetime.datetime.now().strftime("%H:%M")
            alarm_datetime = datetime.datetime.strptime(alarm_time, "%H:%M")
            current_datetime = datetime.datetime.strptime(current_time, "%H:%M")
            time_diff = (alarm_datetime - current_datetime).total_seconds()

            if time_diff > 0:
                messagebox.showwarning("Warning", "Please select a future time for the alarm.")
            else:
                pygame.mixer.init()
                alarm_sound_file = "alarm.wav"  # Replace with the actual path to your audio file
                pygame.mixer.music.load(alarm_sound_file)
                pygame.mixer.music.play()
                messagebox.showinfo("Alarm", "Time's up!")

        except ValueError:
            messagebox.showwarning("Warning", "Please enter the alarm time in HH:MM format.")

    else:
        messagebox.showwarning("Warning", "Please enter the alarm time.")

# Create the tasks table in the database
create_table()

root = tk.Tk()
root.title("HackPlanner")
root.geometry("1000x1500")
root.config(bg="#FBE9E7")

header_frame = tk.Frame(root, bg="#F48FB1")
header_frame.pack(fill=tk.X)

header_label = tk.Label(header_frame, text="HackPlanner", fg="#FFF", bg="#F48FB1", font=("Arial", 32))
header_label.pack(pady=20)

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack()

add_task_frame = tk.Frame(main_frame, bg="#FFF")
add_task_frame.pack(pady=10)

task_name_label = tk.Label(add_task_frame, text="Task name:", bg="#FFF", font=("Arial", 16))
task_name_label.grid(row=0, column=0, padx=5, pady=5)

task_name_entry = tk.Entry(add_task_frame, width=30, font=("Arial", 16))
task_name_entry.grid(row=0, column=1, padx=5, pady=5)

task_date_label = tk.Label(add_task_frame, text="Task date:", bg="#FFF", font=("Arial", 16))
task_date_label.grid(row=1, column=0, padx=5, pady=5)

task_date_entry = DateEntry(add_task_frame, width=12, background="#FFF", foreground="#000", font=("Arial", 14))
task_date_entry.grid(row=1, column=1, padx=5, pady=5)

add_button = tk.Button(main_frame, text="Add Task", command=add_task, bg="#F48FB1", fg="#FFF", font=("Arial", 16))
add_button.pack(pady=5)

tasks_frame = tk.Frame(main_frame, bg="#FFF")
tasks_frame.pack()

tasks_label = tk.Label(tasks_frame, text="Tasks", font=("Arial", 24), bg="#FFF")
tasks_label.pack(pady=5)

task_list = tk.Listbox(tasks_frame, width=50, font=("Arial", 14))
task_list.pack(pady=5)

retrieve_tasks()

reminder_button = tk.Button(main_frame, text="Set Reminder", command=set_reminder, bg="#F48FB1", fg="#FFF", font=("Arial", 16))
reminder_button.pack(pady=10)

alarm_frame = tk.Frame(main_frame, bg="#FFF")
alarm_frame.pack(pady=5)

alarm_time_label = tk.Label(alarm_frame, text="Alarm time (HH:MM):", bg="#FFF", font=("Arial", 16))
alarm_time_label.grid(row=0, column=0, padx=5, pady=5)

alarm_time_entry = tk.Entry(alarm_frame, width=10, font=("Arial", 16))
alarm_time_entry.grid(row=0, column=1, padx=5, pady=5)

# Add the AM/PM selection dropdown
am_pm_var = tk.StringVar()
am_pm_var.set('AM')  # Set default selection to AM

am_pm_label = tk.Label(alarm_frame, text="AM/PM:", bg="#FFF", font=("Arial", 16))
am_pm_label.grid(row=0, column=2, padx=5, pady=5)

am_pm_dropdown = tk.OptionMenu(alarm_frame, am_pm_var, 'AM', 'PM')
am_pm_dropdown.grid(row=0, column=3, padx=5, pady=5)

alarm_button = tk.Button(main_frame, text="Set Alarm", command=set_alarm, bg="#F48FB1", fg="#bFF", font=("Arial", 16))
alarm_button.pack(pady=5)

footer_label = tk.Label(root, text="© 2023 HackPlanner. All rights reserved.", fg="#FFF", bg="#F48FB1", pady=10)
footer_label.pack(fill=tk.X)

root.mainloop()


