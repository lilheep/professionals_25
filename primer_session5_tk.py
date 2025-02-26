import tkinter as tk
from tkinter import ttk

# Создание главного окна
root = tk.Tk()
root.title("Корпоративный портал")
root.geometry("1920x1080")
root.configure(bg="#E8F5E9")  # Светло-зеленый фон

# --- Верхняя панель ---
top_frame = tk.Frame(root, bg="#DCEFD8", height=80)
top_frame.pack(fill="x")

logo = tk.Label(top_frame, text="ЛОГОТИП", bg="#DCEFD8", font=("Arial", 20, "bold"))
logo.pack(side="left", padx=20, pady=20)

search_entry = tk.Entry(top_frame, font=("Arial", 16), width=80)
search_entry.pack(side="right", padx=20, pady=20)

# --- Сотрудники ---
employees_frame = tk.Frame(root, bg="#E8F5E9")
employees_frame.pack(fill="x", padx=20, pady=20)

tk.Label(employees_frame, text="Сотрудники", font=("Arial", 18, "bold"), bg="#E8F5E9").pack(anchor="w")

employees_list = ["Петров Адмирал Иванович\nИнженер\n+7 999 333 2233"] * 5

emp_container = tk.Frame(employees_frame, bg="#E8F5E9")
emp_container.pack()

for i, emp in enumerate(employees_list):
    emp_label = tk.Label(emp_container, text=emp, bg="#8BC34A", fg="white", font=("Arial", 14), width=25, height=4, relief="solid")
    emp_label.grid(row=0, column=i, padx=10, pady=5)

# --- Основной контент (Календарь, События, Новости) ---
main_frame = tk.Frame(root, bg="#E8F5E9")
main_frame.pack(fill="both", expand=True, padx=20, pady=10)

# --- Левая часть: Календарь и события ---
left_frame = tk.Frame(main_frame, bg="#E8F5E9")
left_frame.pack(side="left", fill="y", padx=10)

tk.Label(left_frame, text="Календарь событий", font=("Arial", 16, "bold"), bg="#E8F5E9").pack(anchor="w")

calendar = tk.Label(left_frame, text="📅 Май 2024\nПн Вт Ср Чт Пт Сб Вс\n 1  2  3  4  5  6  7\n 8  9 10 11 12 13 14\n15 16 17 18 19 20 21",
                    bg="#8BC34A", fg="white", font=("Arial", 14), width=25, height=6, relief="solid")
calendar.pack(pady=10)

tk.Label(left_frame, text="События", font=("Arial", 16, "bold"), bg="#E8F5E9").pack(anchor="w")

events_list = ["Общее собрание в актовом зале\nПетров И. И.\n20.05.2024"] * 3
for event in events_list:
    event_label = tk.Label(left_frame, text=event, bg="#8BC34A", fg="white", font=("Arial", 14), width=45, height=3, relief="solid")
    event_label.pack(pady=5)

# --- Правая часть: Новости ---
right_frame = tk.Frame(main_frame, bg="#E8F5E9")
right_frame.pack(side="right", fill="both", expand=True, padx=10)

tk.Label(right_frame, text="Новости", font=("Arial", 16, "bold"), bg="#E8F5E9").pack(anchor="w")

news_list = ["Водители на трассе М-12 сыграли 'Полный шлем!'\n04.05.2024"] * 3
for news in news_list:
    news_label = tk.Label(right_frame, text=news, bg="#8BC34A", fg="white", font=("Arial", 14), width=60, height=6, relief="solid")
    news_label.pack(pady=10)

# Запуск приложения
root.mainloop()
