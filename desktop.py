import tkinter as tk
from tkinter import ttk
from database import db_connection
import os

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
        cursor.execute('''SELECT employees.last_name, employees.first_name, employees.middle_name, employees.personal_phone_number, employees.birthday, departments.department_name, positions.position_name, CONCAT(director.last_name, ' ', director.first_name, ' ', director.middle_name) AS director_name, CONCAT(assistant.last_name, ' ', assistant.first_name, ' ', assistant.middle_name) AS assistant_name, employees.business_phone_number, employees.corporate_mail, employees.cabinet, employees.other_information FROM employees
JOIN departments
ON employees.department_id = departments.department_id
JOIN positions
ON employees.position_id = positions.position_id
LEFT JOIN employees AS director
ON employees.director_id = director.employee_id
LEFT JOIN employees AS assistant
ON employees.assistant_id = assistant.employee_id''')
        return cursor.fetchall()

information_employee = get_all_information_employee()
information_employee_dict = [employee for employee in information_employee]
print(information_employee_dict)

def show_information_employee(employee):
    card_window = tk.Toplevel(window)
    card_window.title('Карточка сотрудника')
    card_window.geometry('400x300')
    card_window.configure(bg='white')
    
    full_name = ' '.join([employee[0], employee[1], employee[2]])
    personal_phone_number = employee[3]
    birthday = employee[4]
    department_name = employee[5]
    position_name = employee[6]
    director_name = employee[7]
    assistant_name = employee[8]
    business_phone_number = employee[9]
    corporate_mail = employee[10]
    cabinet = employee[11]
    other_information = employee[12]
    
    tk.Label(card_window, text='ФИО: ', font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=5, sticky='w')
    tk.Label(card_window, text=full_name, font=('Arial', 12)).grid(row=0, column=1, padx=10, pady=5, sticky='w')
    tk.Label(card_window, text='Номер телефона: ', font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=5, sticky='w')
    tk.Label(card_window, text=personal_phone_number, font=('Arial', 12)).grid(row=1, column=1, padx=10, pady=5, sticky='w')
    tk.Label(card_window, text='Дата рождения: ', font=('Arial', 12)).grid(row=2, column=0, padx=10, pady=5, sticky='w')
    tk.Label(card_window, text=birthday, font=('Arial', 12)).grid(row=2, column=1, padx=10, pady=5, sticky='w')
    tk.Label(card_window, text='Подразделение: ', font=('Arial', 12)).grid(row=3, column=0, padx=10, pady=5, sticky='w')
    tk.Label(card_window, text=department_name, font=('Arial', 12)).grid(row=3, column=1, padx=10, pady=5, sticky='w')
    tk.Label(card_window, text='Должность: ', font=('Arial', 12)).grid(row=4, column=0, padx=10, pady=5, sticky='w')
    tk.Label(card_window, text=position_name, font=('Arial', 12)).grid(row=4, column=1, padx=10, pady=5, sticky='w')
    tk.Label(card_window, text='Директор: ', font=('Arial', 12)).grid(row=5, column=0, padx=10, pady=5, sticky='w')
    tk.Label(card_window, text=director_name, font=('Arial', 12)).grid(row=5, column=1, padx=10, pady=5, sticky='w')
    tk.Label(card_window, text='Помощник: ', font=('Arial', 12)).grid(row=6, column=0, padx=10, pady=5, sticky='w')
    tk.Label(card_window, text=assistant_name, font=('Arial', 12)).grid(row=6, column=1, padx=10, pady=5, sticky='w')
    tk.Label(card_window, text='Рабочий номер телефона: ', font=('Arial', 12)).grid(row=7, column=0, padx=10, pady=5, sticky='w')
    tk.Label(card_window, text=business_phone_number, font=('Arial', 12)).grid(row=7, column=1, padx=10, pady=5, sticky='w')
    tk.Label(card_window, text='Почта: ', font=('Arial', 12)).grid(row=8, column=0, padx=10, pady=5, sticky='w')
    tk.Label(card_window, text=corporate_mail, font=('Arial', 12)).grid(row=8, column=1, padx=10, pady=5, sticky='w')
    tk.Label(card_window, text='Кабинет: ', font=('Arial', 12)).grid(row=9, column=0, padx=10, pady=5, sticky='w')
    tk.Label(card_window, text=cabinet, font=('Arial', 12)).grid(row=9, column=1, padx=10, pady=5, sticky='w')
    tk.Label(card_window, text='Прочая информация: ', font=('Arial', 12)).grid(row=10, column=0, padx=10, pady=5, sticky='w')
    tk.Label(card_window, text=other_information, font=('Arial', 12), wraplength=300).grid(row=10, column=1, padx=10, pady=5, sticky='w')
    
    close_button = tk.Button(card_window, text='Закрыть', command=card_window.destroy)
    close_button.grid(row=11, column=0, columnspan=2, pady=10)
    
selected_departments = set()
department_positions = {}

def show_names(parent_name):
    if children_frames[parent_name].winfo_ismapped():
        children_frames[parent_name].grid_remove()
        selected_departments.discard(parent_name)
        #remove_line(parent_name)
    else:
        children_frames[parent_name].grid()
        selected_departments.add(parent_name)
        department_positions[parent_name] = (100, 100)
        #draw_lines(parent_name)
            
    update_employees()
    
    print(selected_departments)

def update_employees():
    for widget in right_frame.winfo_children():
        widget.destroy()
         
    filtred_employees = [emp for emp in employees_and_departments if any(emp[6] in department_dict.get(dep, []) for dep in selected_departments)]

    
    for emp in filtred_employees:
        employees_frame = tk.Frame(right_frame, padx=20, pady=10, width=960, height=100)
        employees_frame.pack(fill='x', padx=50, pady=20, anchor='e')
        full_name = ' '.join([emp[0], emp[1], emp[2]])
        dep_and_pos = ' - '.join([emp[7], emp[8]])
        dep_label = tk.Label(employees_frame, text=f'{dep_and_pos}', bg='#E1F4C8', anchor='w', font=('Arial', 12,)).pack(fill='x')
        full_name_label = tk.Label(employees_frame, text=f'{full_name}', bg='#E1F4C8', anchor='w', font=('Arial', 12,)).pack(fill='x')
        contact_label = tk.Label(employees_frame, text=f'{emp[3]} {emp[4]}', bg='#E1F4C8', anchor='w', font=('Arial', 12)).pack(fill='x')
        cabinet_label = tk.Label(employees_frame, text=f'{emp[5]}', bg='#E1F4C8', anchor='w', font=('Arial', 12)).pack(fill='x')
        view_button = tk.Button(employees_frame, text='Подробнее', command=lambda e=emp: show_information_employee(e))
        view_button.pack(pady=5)

def draw_lines(parent_name):
    if parent_name not in department_positions:
        print('Нету паранта в списочке департмент позишион')
        return
    
    parent_x, parent_y = department_positions[parent_name]
    
    if parent_name in department_dict:
        base_y = parent_y
        for index, child in enumerate(department_dict[parent_name]):
            child_x = parent_x + 200
            child_y = base_y + (index * 80)
            department_positions[child] = (child_x, child_y)
            
            line = canvas.create_line(
                parent_x + 100, parent_y + 20, child_x, child_y + 20,
                arrow=tk.LAST, width=2
            )
            
            text = canvas.create_text(child_x, child_y, text=child, font=('Arial', 12, 'bold'))
            print(f'Линия от {parent_x}, {parent_y} к {child_x}, {child_y}')

    canvas.configure(scrollregion=canvas.bbox('all'))

def remove_line(parent_name):
    for item in canvas.find_all():
        canvas.delete(item)
    

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

def update_scrollregion(event=None):
    canvas.configure(scrollregion=canvas.bbox("all"))
canvas_frame.bind('<Configure>', update_scrollregion)


right_frame = tk.Frame(canvas_frame, width=960, bg='light gray', pady=50)
right_frame.grid(row=0, column=1, sticky='ne', padx=100)

left_frame = tk.Frame(canvas_frame, width=960, height=1080, pady=50)
left_frame.grid(row=0, column=0, sticky='nw')

departments = load_departments()
employees_and_departments = load_employees_and_departments()

department_dict = {}
row_index = 0
children_frames = {}

for dep in departments:
    parent = dep[0]
    name = dep[1]
    if parent not in department_dict:
        department_dict[parent] = []
    department_dict[parent].append(name)

col_index = 0
col_parents = 0
parent_frame = tk.Frame(left_frame, pady=10, padx=20, width=960, height=300)
parent_frame.grid(row=row_index, column=0, columnspan=5, sticky='w')

for parent in department_dict.keys():
    parent_button = tk.Button(parent_frame, text=parent, font=('Arial', 14, 'bold'), bg='#E1F4C8', bd=1, command=lambda p=parent: show_names(p))
    
    parent_button.grid(row=0, column=col_parents, padx=10, pady=5, sticky='w')
    col_parents += 1
    
row_index +=1

for parent, children in department_dict.items():

    children_frame = tk.Frame(left_frame, padx=0, pady=5, width=960)
    children_frame.grid(row=row_index, column=0, sticky='w', padx=10)
    children_frame.grid_remove()
    
    children_frames[parent] = children_frame
    
    col_index = 0
    
    for child in children:
        dep_label = tk.Label(children_frame, text=f'{child}', font=('Arial', 12), anchor='w', bd=1, relief='solid', bg='#F0FFF0')
        dep_label.grid(row=0, column=col_index, padx=20, pady=5, sticky='w')
        col_index += 1
    row_index += 1

print(department_dict)
window.mainloop()
