import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from dsl.InterpreterJSON import Interpretator

def open_json_file():
    global json_file_path
    json_file_path = filedialog.askopenfilename(title="Select a JSON file", filetypes=[("JSON files", "*.json")])
    if json_file_path:
        if json_file_path.endswith('.json'):
            json_status_label.config(text="File selected", fg="green")
            check_files_selected()
        else:
            messagebox.showerror("Error", "The selected file is not a JSON file.")
            json_status_label.config(text="No file", fg="red")
    else:
        json_status_label.config(text="No file", fg="red")

def open_log_file():
    global log_file_path
    log_file_path = filedialog.askopenfilename(title="Select a log file", filetypes=[("Log files", "*.log"), ("Text files", "*.txt"), ("DB files", "*.xidb")])
    if log_file_path:
        log_status_label.config(text="File selected", fg="green")
        check_files_selected()
    else:
        log_status_label.config(text="No file", fg="red")

def find_antipatterns():
    interpretator = Interpretator(file=json_file_path)
    interpretator.run()
    messagebox.showinfo("Success", "Analysis complete. Check the report.")

def check_files_selected():
    if json_file_path and log_file_path:
        find_antipatterns_button.config(state="normal", bg="green")
    else:
        find_antipatterns_button.config(state="disabled", bg="grey")

# Инициализация переменных для путей файлов
json_file_path = ""
log_file_path = ""

root = tk.Tk()
root.title("File Selector")
root.geometry("600x400")

open_json_button = tk.Button(root, text="Open JSON file", command=open_json_file)
open_json_button.pack(pady=20)
json_status_label = tk.Label(root, text="No file", fg="red")
json_status_label.pack()

open_log_button = tk.Button(root, text="Open log file", command=open_log_file)
open_log_button.pack(pady=20)
log_status_label = tk.Label(root, text="No file", fg="red")
log_status_label.pack()

find_antipatterns_button = tk.Button(root, text="Find Antipatterns", command=find_antipatterns, state="disabled", bg="grey")
find_antipatterns_button.pack(pady=20)

file_label = tk.Label(root, text="Please select a JSON file and a log file.")
file_label.pack(pady=20)

root.mainloop()
