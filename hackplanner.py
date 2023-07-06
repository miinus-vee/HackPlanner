import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import datetime

def add_task():
    task_name = task_name_entry.get()
    task_date = task_date_entry.get_date()
    if task_name.strip() != '':
        task_list.insert(tk.END, f"{task_name} - {task_date.strftime('%Y-%m-%d')}")
        task_name_entry.delete(0, tk.END)
        task_date_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Task name cannot be empty!")

def set_reminder():
    selected_task = task_list.curselection()
    if len(selected_task) > 0:
        task = task_list.get(selected_task[0])
        task_name, task_date = task.split(" - ")
        date_obj = datetime.datetime.strptime(task_date, "%Y-%m-%d")
        today = datetime.date.today()
        if date_obj >= today:
            days_left = (date_obj - today).days
            messagebox.showinfo("Reminder Set", f"Reminder set for Task '{task_name}'\nDays Left: {days_left}")
        else:
            messagebox.showinfo("Reminder Set", f"Reminder set for Task '{task_name}' (Past Due Date)")
    else:
        messagebox.showwarning("Warning", "Please select a task from the list!")

root = tk.Tk()
root.title("HackPlanner")
root.geometry("900x700")
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
add_button.pack(pady=10)

tasks_frame = tk.Frame(main_frame, bg="#FFF")
tasks_frame.pack()

tasks_label = tk.Label(tasks_frame, text="Tasks", font=("Arial", 24), bg="#FFF")
tasks_label.pack(pady=10)

task_list = tk.Listbox(tasks_frame, width=50, font=("Arial", 14))
task_list.pack(pady=5)

reminder_button = tk.Button(main_frame, text="Set Reminder", command=set_reminder, bg="#F48FB1", fg="#FFF", font=("Arial", 16))
reminder_button.pack(pady=10)

footer_label = tk.Label(root, text="© 2023 HackPlanner. All rights reserved.", fg="#FFF", bg="#F48FB1", pady=10)
footer_label.pack(fill=tk.X)

root.mainloop()
