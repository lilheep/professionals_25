import tkinter as tk
from tkinter import ttk
import os
from database import db_connection

os.environ['TCL_LIBRARY'] = r"C:\Users\User\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\User\AppData\Local\Programs\Python\Python313\tcl\tk8.6"

def load_employee_info():
    with db_connection.cursor() as cursor:
        cursor.execute('''SELECT employees.last_name, employees.first_name, employees.middle_name, positions.position_name, employees.corporate_mail, employees.business_phone_number, employees.birthday FROM employees
                        JOIN positions
                        ON employees.position_id = positions.position_id''')
        return cursor.fetchall()

root = tk.Tk()
root.geometry('1920x1080')
root.title('Новости компании')

top_frame = tk.Frame(root, background='light green', height=80)
top_frame.pack(fill='x')

logo = tk.PhotoImage(file='data/Logo.png')

logo_label = tk.Label(top_frame, image=logo)
logo_label.pack(side='left', padx=20, pady=20)

search_entry = tk.Entry(top_frame, font=('Arial', 16), width=150)
search_entry.pack(side='right', padx=20, pady=20)

employees_frame = tk.Frame(root)
employees_frame.pack(fill='x', padx=20, pady=20)

tk.Label(employees_frame, text='Сотрудники', font=('Arial', 18)).pack(anchor='w')

employees_list = list(load_employee_info())

emp_container = tk.Frame(employees_frame)
emp_container.pack()

for i, emp in employees_list:
    emp_name = tk.Label(emp_container, text=f'{emp[0], emp[1], emp[2]}')

root.mainloop()