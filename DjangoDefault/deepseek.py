import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sqlite3
import os
import platform

DB_NAME = "documents.db"
current_user = None  # Hozircha foydalanuvchi tizimga kirmagan

def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            full_name TEXT NOT NULL,
            role TEXT CHECK(role IN ('talaba', 'o‘qituvchi')) NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            path TEXT NOT NULL UNIQUE
        )
    """)
    conn.commit()
    conn.close()

def register_user():
    """ Foydalanuvchini ro‘yxatdan o‘tkazish """
    global reg_window
    username = entry_name.get()
    fullname = full_name.get()
    role = role_var.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showwarning("Xatolik", "Barcha maydonlarni to‘ldiring!")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, role, password,full_name) VALUES (?, ?, ?,?)", (username, role, password,fullname))
        conn.commit()
        messagebox.showinfo("Muvaffaqiyatli", "Ro‘yxatdan o‘tildi! Endi tizimga kiring.")
        reg_window.destroy()  # Ro‘yxatdan o‘tish oynasini yopish
        open_login_window()  # Avtomatik login oynasini ochish
    except sqlite3.IntegrityError:
        messagebox.showwarning("Xatolik", "Bu foydalanuvchi allaqachon mavjud!")
    finally:
        conn.close()

def login_user():
    """ Foydalanuvchini tizimga kiritish """
    global current_user
    username = entry_login_name.get()
    password = entry_login_password.get()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        current_user = user[2]
        messagebox.showinfo("Xush kelibsiz!", f"Salom, {current_user}!")
        login_window.destroy()  # Login oynasini yopish
        open_main_window()  # Asosiy oynani ochish
    else:
        messagebox.showerror("Xatolik", "username Name yoki parol noto‘g‘ri!")

def open_register_window():
    """ Ro‘yxatdan o‘tish oynasini ochish """
    global reg_window, entry_name,full_name, entry_password, role_var
    reg_window = tk.Tk()
    reg_window.title("Ro‘yxatdan o‘tish")
    reg_window.geometry("300x250")
    tk.Label(reg_window, text="F.I.O:").pack()
    full_name = tk.Entry(reg_window)
    full_name.pack() 

    tk.Label(reg_window, text="Username:").pack()
    entry_name = tk.Entry(reg_window)
    entry_name.pack()

    tk.Label(reg_window, text="Rolni tanlang:").pack()
    role_var = tk.StringVar(value='talaba')
    ttk.Combobox(reg_window, textvariable=role_var, values=["talaba", "o‘qituvchi"]).pack()

    tk.Label(reg_window, text="Password:").pack()
    entry_password = tk.Entry(reg_window, show="*")
    entry_password.pack()

    tk.Button(reg_window, text="Ro‘yxatdan o‘tish", command=register_user, bg='#4CAF50', fg='white').pack(pady=10)

    reg_window.mainloop()

def open_login_window():
    """ Tizimga kirish oynasini ochish """
    global login_window, entry_login_name, entry_login_password
    login_window = tk.Tk()
    login_window.title("Tizimga kirish")
    login_window.geometry("300x200")

    tk.Label(login_window, text="Username:").pack()
    entry_login_name = tk.Entry(login_window)
    entry_login_name.pack()

    tk.Label(login_window, text="Password:").pack()
    entry_login_password = tk.Entry(login_window, show="*")
    entry_login_password.pack()


    tk.Button(login_window, text="Kirish", command=login_user, bg='#008CBA', fg='white').pack(pady=10)
    tk.Button(login_window, text="Ro‘yxatdan o‘tish", command=lambda: [login_window.destroy(), open_register_window()]).pack()

    login_window.mainloop()

def open_main_window():
    """ Asosiy oynani ochish """
    global root, listbox, btn_select, btn_open, btn_delete

    root = tk.Tk()
    root.title("Kafedra hujjatlarini boshqarish")
    root.geometry("800x500")

    tk.Label(root, text=f"Hush kelibsiz, {current_user}!", font=("Arial", 12)).pack(pady=5)

    btn_select = tk.Button(root, text="Hujjat qo‘shish", command=select_file, bg='#008CBA', fg='white')
    btn_select.pack(pady=5)

    listbox = tk.Listbox(root, width=60, height=15)
    listbox.pack(pady=5)

    btn_open = tk.Button(root, text="Faylni ochish", command=open_file, bg='#4CAF50', fg='white')
    btn_open.pack(pady=5)

    btn_delete = tk.Button(root, text="Faylni o‘chirish", command=delete_file, bg='#f44336', fg='white')
    btn_delete.pack(pady=5)

    update_listbox()
    root.mainloop()

def select_file():
    """ Fayl tanlash """
    file_path = filedialog.askopenfilename()
    if file_path:
        file_name = os.path.basename(file_path)
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO documents (name, path) VALUES (?, ?)", (file_name, file_path))
            conn.commit()
        except sqlite3.IntegrityError:
            messagebox.showwarning("Xatolik", "Bu fayl allaqachon mavjud!")
        conn.close()
        update_listbox()

def open_file():
    """ Fayl ochish """
    selected = listbox.curselection()
    if selected:
        file_name = listbox.get(selected)
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT path FROM documents WHERE name = ?", (file_name,))
        result = cursor.fetchone()
        conn.close()

        if result and os.path.exists(result[0]):
            if platform.system() == "Windows":
                os.startfile(result[0])
            else:
                os.system(f"xdg-open '{result[0]}'")
        else:
            messagebox.showwarning("Xatolik", "Fayl topilmadi!")

def delete_file():
    """ Faylni o‘chirish """
    selected = listbox.curselection()
    if selected:
        file_name = listbox.get(selected)
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM documents WHERE name = ?", (file_name,))
        conn.commit()
        conn.close()
        update_listbox()

def update_listbox():
    """ Ro‘yxatni yangilash """
    listbox.delete(0, tk.END)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM documents")
    for file in cursor.fetchall():
        listbox.insert(tk.END, file[0])
    conn.close()

# **Bazani yaratish va login oynasini ochish**
create_database()
open_login_window()
