import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import organizer

# Ask username before running
username = None

def login_gui():
    global username
    username = simpledialog.askstring("Login", "Enter username:")
    if not username:
        messagebox.showerror("Error", "Username is required!")
        return False
    return True

def select_folder():
    if not username:
        messagebox.showerror("Error", "You must log in first!")
        return
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        skip_input = simpledialog.askstring("Skip Extensions", "Enter extensions to skip (comma-separated, e.g., .txt,.jpg):")
        skip_exts = [s.strip().lower() for s in skip_input.split(",")] if skip_input else []
        organizer.backup_folder(username, folder_selected)
        organizer.organize_folder(username, folder_selected, skip_exts)
        messagebox.showinfo("Success", "Files organized successfully!")

root = tk.Tk()
root.title("File Organizer")
root.geometry("400x200")

login_button = tk.Button(root, text="Login", command=login_gui, font=("Arial", 12), bg="lightgreen")
login_button.pack(pady=10)

label = tk.Label(root, text="Select a folder to organize:", font=("Arial", 12))
label.pack(pady=20)

choose_button = tk.Button(root, text="Choose Folder", command=select_folder, font=("Arial", 12), bg="lightblue")
choose_button.pack(pady=10)

root.mainloop()
