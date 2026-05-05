import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os


# Константы

HISTORY_FILE = "password_history.json"
MIN_PASSWORD_LENGTH = 4
MAX_PASSWORD_LENGTH = 64


# Загрузка истории

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Сохранение истории

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)


# Генерация пароля

def generate_password():
    length = password_length.get()
    include_digits = var_digits.get()
    include_letters = var_letters.get()
    include_symbols = var_symbols.get()
    
    if length < MIN_PASSWORD_LENGTH or length > MAX_PASSWORD_LENGTH:
        messagebox.showerror("Ошибка", f"Длина пароля должна быть между {MIN_PASSWORD_LENGTH} и {MAX_PASSWORD_LENGTH}.")
        return

    chars = ""
    if include_digits:
        chars += string.digits
    if include_letters:
        chars += string.ascii_letters
    if include_symbols:
        chars += string.punctuation

    if not chars:
        messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов!")
        return

    password = "".join(random.choice(chars) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)

    # Сохранение в историю
    history.append(password)
    save_history(history)
    update_history_table()


# Обновление таблицы истории

def update_history_table():
    for row in history_table.get_children():
        history_table.delete(row)
    for i, pwd in enumerate(history[::-1], start=1):
        history_table.insert("", tk.END, values=(i, pwd))


# Основное окно

root = tk.Tk()
root.title("Random Password Generator")
root.geometry("500x500")
root.resizable(False, False)


# Виджеты

frame_settings = tk.Frame(root)
frame_settings.pack(pady=10)

# Ползунок длины
tk.Label(frame_settings, text="Длина пароля:").grid(row=0, column=0, sticky="w")
password_length = tk.IntVar(value=12)
slider_length = tk.Scale(frame_settings, from_=MIN_PASSWORD_LENGTH, to=MAX_PASSWORD_LENGTH, orient=tk.HORIZONTAL, variable=password_length)
slider_length.grid(row=0, column=1)

# Чекбоксы
var_digits = tk.BooleanVar(value=True)
var_letters = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=True)

tk.Checkbutton(frame_settings, text="Цифры", variable=var_digits).grid(row=1, column=0, sticky="w")
tk.Checkbutton(frame_settings, text="Буквы", variable=var_letters).grid(row=1, column=1, sticky="w")
tk.Checkbutton(frame_settings, text="Спецсимволы", variable=var_symbols).grid(row=1, column=2, sticky="w")

# Кнопка генерации
generate_btn = tk.Button(root, text="Сгенерировать пароль", command=generate_password)
generate_btn.pack(pady=10)

# Поле для отображения пароля
password_entry = tk.Entry(root, width=50, font=("Arial", 12))
password_entry.pack(pady=5)

# Таблица истории
history_frame = tk.Frame(root)
history_frame.pack(pady=10, fill=tk.BOTH, expand=True)

columns = ("#", "Пароль")
history_table = ttk.Treeview(history_frame, columns=columns, show="headings")
history_table.heading("#", text="#")
history_table.heading("Пароль", text="Пароль")
history_table.column("#", width=30)
history_table.column("Пароль", width=400)
history_table.pack(fill=tk.BOTH, expand=True)


# Загрузка истории

history = load_history()
update_history_table()

# Запуск приложения

root.mainloop()