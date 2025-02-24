import tkinter as tk
from tkinter import ttk
from database import db_connection
import os
import tkinter.messagebox as msgbox
import re

os.environ['TCL_LIBRARY'] = r"C:\Users\User\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\User\AppData\Local\Programs\Python\Python313\tcl\tk8.6"

def load_employees_and_departments():
    with db_connection.cursor() as cursor:
        cursor.execute('SELECT last_name, first_name, middle_name, business_phone_number, corporate_mail, cabinet, departments.department_name, departments.parent_department, positions.position_name FROM employees JOIN departments ON employees.department_id = departments.department_id JOIN positions ON employees.position_id = positions.position_id')
        return cursor.fetchall()

def load_employees():
    cursor = db_connection.cursor()
    cursor.execute('SELECT last_name, first_name, middle_name, business_phone_number, corporate_mail, cabinet FROM employees;')
    return cursor.fetchall()

def load_departments():
    cursor = db_connection.cursor()
    cursor.execute('SELECT parent_department, department_name FROM departments;')
    return cursor.fetchall()

def get_all_information_employee():
    with db_connection.cursor() as cursor:
        cursor.execute(f'''SELECT employees.last_name, employees.first_name, employees.middle_name, employees.personal_phone_number, employees.birthday, departments.department_name, positions.position_name, 
                       CONCAT(director.last_name, ' ', director.first_name, ' ', director.middle_name) AS director_name, 
                       CONCAT(assistant.last_name, ' ', assistant.first_name, ' ', assistant.middle_name) AS assistant_name, employees.business_phone_number, employees.corporate_mail, employees.cabinet, employees.other_information FROM employees
JOIN departments
ON employees.department_id = departments.department_id
JOIN positions
ON employees.position_id = positions.position_id
LEFT JOIN employees AS director
ON employees.director_id = director.employee_id
LEFT JOIN employees AS assistant
ON employees.assistant_id = assistant.employee_id''')
        return cursor.fetchall() 

def get_employee_for_department(department_name):
    with db_connection.cursor() as cursor:
        cursor.execute(f'''SELECT employees.last_name, employees.first_name, employees.middle_name, departments.department_name, positions.position_name, employees.business_phone_number, employees.cabinet, employees.corporate_mail FROM employees
JOIN departments
ON employees.department_id = departments.department_id
JOIN positions
ON employees.position_id = positions.position_id
WHERE departments.department_name = "{department_name}"''')
        return cursor.fetchall()
    
def get_all_sub_dep(parent_department):
    employees = []
    employees += get_employee_for_department(parent_department)
    
    if parent_department in department_hierarchy:
        for sub_dep in department_hierarchy[parent_department]:
            employees += get_all_sub_dep(sub_dep)

    return employees
    
def create_employee_card(employee_data, parent_frame):
    last_name, first_name, middle_name, department_name, position_name, phone, cabinet, email = employee_data
    card_frame = tk.Frame(parent_frame, bg='light green', relief='solid', borderwidth=1, width=500)
    card_frame.pack(padx=10, pady=10, fill='x')
    
    tk.Label(card_frame, text=f'{department_name} - {position_name}', font=('Arial', 12), bg='light green').pack(anchor='w')
    tk.Label(card_frame, text=f'{last_name} {first_name} {middle_name}', font=('Arial', 14), bg='light green').pack(anchor='center')
    tk.Label(card_frame, text=f'{phone} {email}', font=('Arial', 12), bg='light green').pack(anchor='w')
    tk.Label(card_frame, text=f'{cabinet}', font=('Arial', 12), bg='light green').pack(anchor='w')

    card_frame.bind("<Button-1>", lambda event, employee_data=employee_data: create_modal_employee_card(parent_frame, employee_data))
def update_right_frame(department_name):
    for widget in frame_right.winfo_children():
        widget.destroy()
    
    employees = get_all_sub_dep(department_name)
    
    for employee in employees:
        create_employee_card(employee, frame_right)
        
def create_modal_employee_card(parent_frame, employee_data):
    modal_window = tk.Toplevel(parent_frame)
    modal_window.geometry('500x600')
    modal_window.title('Редактировать информацию сотрудника')
    
    last_name, first_name, middle_name, personal_phone, birthday, department_name, postion_name, director_name, assistant_name, bussines_phone, mail, cabinet, other_information = employee_data
    print(employee_data)
    tk.Label(modal_window, text="Фамилия:").pack(fill='x', pady=5)
    entry_last_name = tk.Entry(modal_window)
    entry_last_name.insert(0, last_name)
    entry_last_name.pack(fill='x', pady=5)

    tk.Label(modal_window, text="Имя:").pack(fill='x', pady=5)
    entry_first_name = tk.Entry(modal_window)
    entry_first_name.insert(0, first_name)
    entry_first_name.pack(fill='x', pady=5)

    tk.Label(modal_window, text="Отчество:").pack(fill='x', pady=5)
    entry_middle_name = tk.Entry(modal_window)
    entry_middle_name.insert(0, middle_name)
    entry_middle_name.pack(fill='x', pady=5)

    tk.Label(modal_window, text="Мобильный телефон:").pack(fill='x', pady=5)
    entry_personal_phone = tk.Entry(modal_window)
    entry_personal_phone.insert(0, personal_phone)
    entry_personal_phone.pack(fill='x', pady=5)

    tk.Label(modal_window, text="Дата рождения:").pack(fill='x', pady=5)
    entry_birthday = tk.Entry(modal_window)
    entry_birthday.insert(0, birthday)
    entry_birthday.pack(fill='x', pady=5)

    tk.Label(modal_window, text="Рабочий телефон:").pack(fill='x', pady=5)
    entry_business_phone = tk.Entry(modal_window)
    entry_business_phone.insert(0, bussines_phone)
    entry_business_phone.pack(fill='x', pady=5)

    tk.Label(modal_window, text="Электронная почта:").pack(fill='x', pady=5)
    entry_corporate_mail = tk.Entry(modal_window)
    entry_corporate_mail.insert(0, mail)
    entry_corporate_mail.pack(fill='x', pady=5)

    tk.Label(modal_window, text="Кабинет:").pack(fill='x', pady=5)
    entry_cabinet = tk.Entry(modal_window)
    entry_cabinet.insert(0, cabinet)
    entry_cabinet.pack(fill='x', pady=5)

    tk.Label(modal_window, text="Прочая информация:").pack(fill='x', pady=5)
    entry_other_info = tk.Entry(modal_window)
    entry_other_info.insert(0, other_information)
    entry_other_info.pack(fill='x', pady=5)
    
    def save_change():
        if not entry_last_name.get() or not entry_first_name.get():
            msgbox.showerror('Ошибка!', 'ФИО - обязательное поле для заполнения!')
        
        if not re.match(r'^[0-9+()\\-#] + $', entry_personal_phone.get()):
            msgbox.showerror('Ошибка!', 'Некорректный номер телефона!')
        
        if not re.match(r'^[0-9+()\\-#] + $', entry_business_phone.get()):
            msgbox.showerror('Ошибка!', 'Некорректный рабочий номер телефона!')
            
        if not re.match(r'^[A-Za-z0-9._%%+-]+@[A-Za-z]\\.[a-z]{2,}$', entry_corporate_mail.get()):
            msgbox.showerror('Ошибка!', 'Некорректный формат почтового ящика!')
        
        if len(entry_cabinet.get()) > 10:
            msgbox.showerror('Ошибка!', 'Значение в поле "Кабинет", не может быть больше 10 символов!')
        
        with db_connection.cursor() as cursor:
            cursor.execute(f'''UPDATE employees SET last_name="{entry_last_name}", first_name="{entry_first_name}", middle_name="{entry_middle_name}", 
                            personal_phone_number="{entry_personal_phone}", birthday="{entry_birthday}", business_phone_number="{entry_business_phone}", corporate_mail="{entry_corporate_mail}", cabinet={entry_cabinet}, 
                            other_information="{entry_other_info}" WHERE last_name="{entry_last_name}" AND first_name="{entry_first_name}"''')
            db_connection.commit()
        modal_window.destroy()
    tk.Button(modal_window, text='Сохранить', command=save_change).pack(side='left', padx=10, pady=10)
    tk.Button(modal_window, text='Закрыть', command=modal_window.destroy).pack(side='right', padx=10, pady=10)

window = tk.Tk()
window.geometry('1920x1080')
window.title('Организационная структура')

header_frame = tk.Frame(window, bg='#E1F4C8', height=500)
header_frame.pack(side='top', fill='x')

header_label = tk.Label(header_frame, text='Организационная структура', font=('Arial', 10, 'bold'), fg='black', bg='white', height=5)
header_label.pack(side='left', fill='x', anchor='center')

canvas = tk.Canvas(window)
canvas.pack(fill='both', expand=True, side='left')
scrollbar = ttk.Scrollbar(window, orient='vertical', command=canvas.yview)
scrollbar.pack(side='right', fill='y')
canvas.configure(yscrollcommand=scrollbar.set)
canvas_frame = tk.Frame(canvas)
canvas_window = canvas.create_window((0, 0), window=canvas_frame, anchor='nw')

canvas_frame.update_idletasks()
canvas_frame.config(width=1900, height=1000)

def update_scrollregion(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))
canvas_frame.bind('<Configure>', update_scrollregion)

frame_left = tk.Frame(canvas_frame, bg='light gray', width=950, height=900)
frame_left.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

frame_right = tk.Frame(canvas_frame, bg='light gray', width=950, height=900)
frame_right.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

canvas_frame.columnconfigure(0, weight=1)
canvas_frame.columnconfigure(1, weight=0)
canvas_frame.columnconfigure(0, minsize=950)
canvas_frame.columnconfigure(1, minsize=950)

canvas_frame.rowconfigure(0, weight=1)

departments = load_departments()
department_hierarchy = {}

for parent_department, department_name in departments:
    if parent_department not in department_hierarchy:
        department_hierarchy[parent_department] = []
    department_hierarchy[parent_department].append(department_name)

def show_department_frame(parent_frame, parent_name, hierarchy):
    frame_department = tk.Frame(parent_frame, background='light green', relief='solid', borderwidth=1)
    frame_department.pack(fill='x', padx=10, pady=10)
    
    label_department = tk.Label(frame_department, text=parent_name, font=('Arial', 16, 'bold'), bg='light green', height=3)
    label_department.pack(anchor='center')
    
    frame_department.bind("<Button-1>", lambda event, department=parent_name: update_right_frame(department))
    label_department.bind("<Button-1>", lambda event, department=parent_name: update_right_frame(department))
    if parent_name in hierarchy:
        for sub_dep in hierarchy[parent_name]:
            sub_frame = tk.Frame(frame_department, background='light green', relief='solid', borderwidth=1)
            sub_frame.pack(fill='x', padx=10, pady=5)
            label_sub_department = tk.Label(sub_frame, text=sub_dep, font=('Arial', 14), bg='light green', height=2)
            label_sub_department.pack(anchor='center')
            sub_frame.bind("<Button-1>", lambda event, department=sub_dep: update_right_frame(department))
            label_sub_department.bind("<Button-1>", lambda event, department=sub_dep: update_right_frame(department))

for department in department_hierarchy:
    show_department_frame(frame_left, department, department_hierarchy)

window.mainloop()
