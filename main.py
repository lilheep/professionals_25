from materials import add_materials, edit_material, get_all_materials, get_material

def main_menu():
    while True:
        print('Menu:')
        print('1. Add material')
        print('2. Edit material')
        print('3. Get all materials')
        print('4. Get material by ID')
        print('5. Exit')
        
        action = int(input('Select an action: '))
        
        if action == 1:
            add_materials()
        
        elif action == 2:
            edit_material()
        
        elif action == 3:
            get_all_materials()
            
        elif action == 4:
            get_material()
            
        elif action == 5:
            break
        
        else:
            print('Incorrect input, try again!')
            
main_menu()
            
