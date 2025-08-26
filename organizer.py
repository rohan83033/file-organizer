import os
import shutil
import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading

# Backend functions from your original code
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx", ".csv"],
    "Videos": [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"]
}

SIZE_LIMITS = {
    "Small": 1 * 1024 * 1024,
    "Medium": 10 * 1024 * 1024,
    "Large": float("inf")
}

DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
UNDO_FILE = os.path.join(DATA_DIR, "undo_log.json")

def ensure_data_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "logs"), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIR, "backups"), exist_ok=True)

def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def get_category(extension):
    for category, exts in FILE_TYPES.items():
        if extension.lower() in exts:
            return category
    return "Others"

def get_size_group(size):
    if size <= SIZE_LIMITS["Small"]:
        return "Small"
    elif size <= SIZE_LIMITS["Medium"]:
        return "Medium"
    return "Large"

def create_log(username, message):
    log_file = os.path.join(DATA_DIR, "logs", f"{username}_log.txt")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {message}\n")

def backup_folder(username, folder_path):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = os.path.join(DATA_DIR, "backups", username, timestamp)
    os.makedirs(backup_dir, exist_ok=True)
    for item in os.listdir(folder_path):
        src_path = os.path.join(folder_path, item)
        if os.path.isfile(src_path):
            shutil.copy2(src_path, backup_dir)
    return backup_dir

class FileOrganizerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("File Organizer")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.current_user = None
        ensure_data_dirs()
        
        # Initialize with login screen
        self.show_login_screen()
        
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_screen(self):
        self.clear_window()
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="📁 File Organizer", 
                              font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#2c3e50")
        title_label.pack(pady=(50, 30))
        
        # Login form frame
        form_frame = tk.Frame(main_frame, bg="#ffffff", relief="raised", bd=2)
        form_frame.pack(pady=20, padx=100, fill="x")
        
        tk.Label(form_frame, text="Login / Register", font=("Arial", 16, "bold"), 
                bg="#ffffff", fg="#34495e").pack(pady=20)
        
        # Username field
        tk.Label(form_frame, text="Username:", font=("Arial", 10), 
                bg="#ffffff").pack(pady=(10, 5))
        self.username_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
        self.username_entry.pack(pady=(0, 10))
        
        # Password field
        tk.Label(form_frame, text="Password:", font=("Arial", 10), 
                bg="#ffffff").pack(pady=(10, 5))
        self.password_entry = tk.Entry(form_frame, font=("Arial", 12), width=30, show="*")
        self.password_entry.pack(pady=(0, 20))
        
        # Buttons frame
        buttons_frame = tk.Frame(form_frame, bg="#ffffff")
        buttons_frame.pack(pady=(0, 20))
        
        login_btn = tk.Button(buttons_frame, text="Login", command=self.login,
                             bg="#3498db", fg="white", font=("Arial", 12, "bold"),
                             padx=20, pady=8, cursor="hand2")
        login_btn.pack(side="left", padx=(0, 10))
        
        register_btn = tk.Button(buttons_frame, text="Register", command=self.register,
                               bg="#2ecc71", fg="white", font=("Arial", 12, "bold"),
                               padx=20, pady=8, cursor="hand2")
        register_btn.pack(side="left")
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda e: self.login())
        
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password!")
            return
        
        users = load_users()
        if username in users and users[username]["password"] == password:
            self.current_user = username
            messagebox.showinfo("Success", f"Welcome, {username}!")
            self.show_main_menu()
        else:
            messagebox.showerror("Error", "Invalid credentials!")
    
    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password!")
            return
        
        users = load_users()
        if username in users:
            messagebox.showerror("Error", "Username already exists!")
            return
        
        users[username] = {"password": password}
        save_users(users)
        messagebox.showinfo("Success", "Registration successful! You can now login.")
        
    def show_main_menu(self):
        self.clear_window()
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg="#34495e")
        header_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(header_frame, text=f"Welcome, {self.current_user}!", 
                font=("Arial", 18, "bold"), bg="#34495e", fg="white").pack(pady=15)
        
        # Menu buttons frame
        buttons_frame = tk.Frame(main_frame, bg="#f0f0f0")
        buttons_frame.pack(expand=True)
        
        # Create menu buttons
        buttons = [
            ("📂 Organize Folder", self.show_organize_screen, "#3498db"),
            ("⏪ Undo Last Operation", self.undo_operation, "#e67e22"),
            ("📜 View Log", self.show_log_screen, "#9b59b6"),
            ("👋 Logout", self.logout, "#e74c3c")
        ]
        
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(buttons_frame, text=text, command=command,
                          bg=color, fg="white", font=("Arial", 14, "bold"),
                          width=25, pady=15, cursor="hand2")
            btn.pack(pady=15)
    
    def show_organize_screen(self):
        self.clear_window()
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg="#3498db")
        header_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(header_frame, text="📂 Organize Folder", 
                font=("Arial", 18, "bold"), bg="#3498db", fg="white").pack(pady=15)
        
        # Form frame
        form_frame = tk.Frame(main_frame, bg="#ffffff", relief="raised", bd=2)
        form_frame.pack(fill="both", expand=True, padx=50, pady=20)
        
        # Folder selection
        tk.Label(form_frame, text="Select Folder to Organize:", font=("Arial", 12, "bold"), 
                bg="#ffffff").pack(pady=(20, 10))
        
        folder_frame = tk.Frame(form_frame, bg="#ffffff")
        folder_frame.pack(fill="x", padx=20, pady=10)
        
        self.folder_path_var = tk.StringVar()
        self.folder_entry = tk.Entry(folder_frame, textvariable=self.folder_path_var, 
                                   font=("Arial", 11), state="readonly")
        self.folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(folder_frame, text="Browse", command=self.browse_folder,
                             bg="#2ecc71", fg="white", font=("Arial", 10), cursor="hand2")
        browse_btn.pack(side="right")
        
        # Skip extensions
        tk.Label(form_frame, text="File Extensions to Skip (optional):", 
                font=("Arial", 12, "bold"), bg="#ffffff").pack(pady=(20, 10))
        
        tk.Label(form_frame, text="Enter comma-separated extensions (e.g., .txt,.jpg)", 
                font=("Arial", 10), bg="#ffffff", fg="#7f8c8d").pack(pady=(0, 5))
        
        self.skip_entry = tk.Entry(form_frame, font=("Arial", 11), width=40)
        self.skip_entry.pack(pady=10)
        
        # Progress bar
        self.progress_var = tk.StringVar(value="Ready to organize...")
        tk.Label(form_frame, textvariable=self.progress_var, font=("Arial", 10), 
                bg="#ffffff", fg="#7f8c8d").pack(pady=(20, 10))
        
        self.progress_bar = ttk.Progressbar(form_frame, mode='indeterminate')
        self.progress_bar.pack(fill="x", padx=20, pady=10)
        
        # Buttons
        buttons_frame = tk.Frame(form_frame, bg="#ffffff")
        buttons_frame.pack(pady=20)
        
        organize_btn = tk.Button(buttons_frame, text="🚀 Start Organization", 
                               command=self.start_organization,
                               bg="#e67e22", fg="white", font=("Arial", 12, "bold"),
                               padx=20, pady=10, cursor="hand2")
        organize_btn.pack(side="left", padx=10)
        
        back_btn = tk.Button(buttons_frame, text="← Back", command=self.show_main_menu,
                           bg="#7f8c8d", fg="white", font=("Arial", 12, "bold"),
                           padx=20, pady=10, cursor="hand2")
        back_btn.pack(side="left", padx=10)
    
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path_var.set(folder)
    
    def start_organization(self):
        folder_path = self.folder_path_var.get()
        if not folder_path:
            messagebox.showerror("Error", "Please select a folder!")
            return
        
        if not os.path.exists(folder_path):
            messagebox.showerror("Error", "Folder path does not exist!")
            return
        
        # Start organization in a separate thread
        self.progress_bar.start()
        self.progress_var.set("Creating backup...")
        
        thread = threading.Thread(target=self.organize_files_thread, args=(folder_path,))
        thread.daemon = True
        thread.start()
    
    def organize_files_thread(self, folder_path):
        try:
            skip_text = self.skip_entry.get().strip()
            skip_exts = [s.strip().lower() for s in skip_text.split(",")] if skip_text else []
            
            # Create backup
            self.root.after(0, lambda: self.progress_var.set("Creating backup..."))
            backup_path = backup_folder(self.current_user, folder_path)
            
            # Organize files
            self.root.after(0, lambda: self.progress_var.set("Organizing files..."))
            
            moved_files = []
            summary = {}
            
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isfile(item_path):
                    ext = os.path.splitext(item)[1]
                    if ext.lower() in skip_exts:
                        continue

                    category = get_category(ext)
                    size = os.path.getsize(item_path)
                    size_group = get_size_group(size)

                    creation_time = datetime.fromtimestamp(os.path.getctime(item_path))
                    year_folder = str(creation_time.year)
                    month_folder = f"{creation_time.month:02}"

                    category_folder = os.path.join(folder_path, category, year_folder, month_folder, size_group)
                    os.makedirs(category_folder, exist_ok=True)

                    # Handle duplicate names
                    base, extension = os.path.splitext(item)
                    new_path = os.path.join(category_folder, item)
                    counter = 1
                    while os.path.exists(new_path):
                        new_path = os.path.join(category_folder, f"{base}_{counter}{extension}")
                        counter += 1

                    shutil.move(item_path, new_path)
                    moved_files.append((new_path, folder_path))

                    summary[category] = summary.get(category, 0) + 1
                    create_log(self.current_user, f"Moved: {item} → {category}/{year_folder}/{month_folder}/{size_group}")

            # Save undo information
            if moved_files:
                with open(UNDO_FILE, "w") as f:
                    json.dump({"user": self.current_user, "files": moved_files}, f)

            # Show results
            self.root.after(0, lambda: self.show_organization_results(summary, backup_path))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Organization failed: {str(e)}"))
        finally:
            self.root.after(0, lambda: self.progress_bar.stop())
    
    def show_organization_results(self, summary, backup_path):
        self.progress_bar.stop()
        self.progress_var.set("Organization complete!")
        
        if summary:
            result_text = "Organization Summary:\n\n"
            for category, count in summary.items():
                result_text += f"• {category}: {count} file(s)\n"
            result_text += f"\nBackup created at:\n{backup_path}"
            messagebox.showinfo("Success", result_text)
        else:
            messagebox.showinfo("Info", "No files were organized.")
    
    def undo_operation(self):
        if not os.path.exists(UNDO_FILE):
            messagebox.showerror("Error", "No undo history found!")
            return

        with open(UNDO_FILE, "r") as f:
            data = json.load(f)

        if data["user"] != self.current_user:
            messagebox.showerror("Error", "You can only undo your own last operation!")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to undo the last organization?"):
            try:
                restored_count = 0
                for new_path, original_folder in data["files"]:
                    if os.path.exists(new_path):
                        filename = os.path.basename(new_path)
                        original_path = os.path.join(original_folder, filename)
                        
                        # Handle duplicates in original folder
                        counter = 1
                        while os.path.exists(original_path):
                            base, ext = os.path.splitext(filename)
                            original_path = os.path.join(original_folder, f"{base}_{counter}{ext}")
                            counter += 1
                        
                        shutil.move(new_path, original_path)
                        create_log(self.current_user, f"Restored: {filename}")
                        restored_count += 1

                os.remove(UNDO_FILE)
                messagebox.showinfo("Success", f"Undo complete! Restored {restored_count} files.")
                
            except Exception as e:
                messagebox.showerror("Error", f"Undo failed: {str(e)}")
    
    def show_log_screen(self):
        self.clear_window()
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_frame, bg="#9b59b6")
        header_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(header_frame, text="📜 Activity Log", 
                font=("Arial", 18, "bold"), bg="#9b59b6", fg="white").pack(pady=15)
        
        # Log display frame
        log_frame = tk.Frame(main_frame, bg="#ffffff", relief="raised", bd=2)
        log_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Scrolled text widget
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, 
                                                 font=("Courier", 10), 
                                                 bg="#f8f9fa", fg="#2c3e50")
        self.log_text.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Load and display log
        self.load_log()
        
        # Back button
        back_btn = tk.Button(main_frame, text="← Back", command=self.show_main_menu,
                           bg="#7f8c8d", fg="white", font=("Arial", 12, "bold"),
                           padx=20, pady=10, cursor="hand2")
        back_btn.pack()
    
    def load_log(self):
        log_file = os.path.join(DATA_DIR, "logs", f"{self.current_user}_log.txt")
        if not os.path.exists(log_file):
            self.log_text.insert("1.0", "No activity log found. Start organizing files to see activity here!")
            self.log_text.config(state="disabled")
            return
        
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                log_content = f.read()
                if log_content.strip():
                    self.log_text.insert("1.0", log_content)
                else:
                    self.log_text.insert("1.0", "Activity log is empty. Start organizing files to see activity here!")
        except Exception as e:
            self.log_text.insert("1.0", f"Error reading log file: {str(e)}")
        
        self.log_text.config(state="disabled")
    
    def logout(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to logout?"):
            self.current_user = None
            self.show_login_screen()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FileOrganizerGUI()
    app.run()