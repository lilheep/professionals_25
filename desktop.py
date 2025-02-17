import tkinter as tk
from tkinter import ttk
from database import db_connection
import os

os.environ['TCL_LIBRARY'] = r"C:\Users\User\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\User\AppData\Local\Programs\Python\Python313\tcl\tk8.6"

def load_employees_and_departments():
    with db_connection.cursor() as cursor:
        cursor.execute('SELECT last_name, first_name, middle_name, business_phone_number, corporate_mail, cabinet, departments.department_name FROM employees JOIN departments ON employees.department_id = departments.department_id')
        return cursor.fetchall()

def load_employees():
    cursor = db_connection.cursor()
    cursor.execute('SELECT last_name, first_name, middle_name, business_phone_number, corporate_mail, cabinet FROM employees;')
    return cursor.fetchall()

def load_departments():
    cursor = db_connection.cursor()
    cursor.execute('SELECT parent_department, department_name FROM departments;')
    return cursor.fetchall()

selected_departments = set()
department_positions = {}

def show_names(parent_name):
    if children_frames[parent_name].winfo_ismapped():
        children_frames[parent_name].grid_remove()
        selected_departments.discard(parent_name)
        remove_line(parent_name)
    else:
        children_frames[parent_name].grid()
        selected_departments.add(parent_name)
        department_positions[parent_name] = (100, 100)
        draw_lines(parent_name)
            
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
        tk.Label(employees_frame, text=f'{full_name}', bg='#E1F4C8', anchor='w', font=('Arial', 12,)).pack(fill='x')
        tk.Label(employees_frame, text=f'{emp[3]} {emp[4]}', bg='#E1F4C8', anchor='w', font=('Arial', 12)).pack(fill='x')
        tk.Label(employees_frame, text=f'{emp[5]}', bg='#E1F4C8', anchor='w', font=('Arial', 12)).pack(fill='x')

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

scrollbar_frame = ttk.Frame(canvas)

canvas.create_window((1920, 0), window=scrollbar_frame, anchor='ne')
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
)

right_frame = tk.Frame(scrollbar_frame, width=960, bg='light gray', pady=50)
right_frame.grid(row=0, column=1, sticky='ne', padx=100)

left_frame = tk.Frame(canvas, width=960, height=1080, pady=50)
left_frame.grid(sticky='nw')

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
