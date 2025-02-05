from models import MaterialCards, TrainingMaterials, TrainingOrganizators
from datetime import date


# peredelat' func edit, get x2


def add_materials():
    training_material_id = input('Enter ID training material: ')
    try:
        training_material = TrainingMaterials.get(TrainingMaterials.training_id == training_material_id)
    except Exception as e:
        print(f'Error! No training material with this ID was found. Detail: {e}')   
        return 
        
    material_name = input('Enter the name of the material: ')
    approval_date = date.today()
    upload_date = date.today()
    status = input('Enter status ("Approved", "Checked", "Canceled"): ')
    material_type = input('Enter the type of material: ')
    area = input('Enter the area of the material: ')
    author_id = int(input('Enter the ID of the author of the material (organizer): '))
    
    try:
        author = TrainingOrganizators.get(TrainingOrganizators.organizator_id == author_id)
    except Exception as e:
        print(f'Error! The organizer with this ID was not found! Detail: {e}')
        return
    
    description = input('Enter a description (you can leave it blank): ')
    
    try:
        material = MaterialCards.create(
            training_material_id=training_material,
            material_name=material_name,
            approval_date=approval_date,
            upload_date=upload_date,
            status=status,
            material_type=material_type,
            area=area,
            author=author,
            description=description
        )
        
        print(f'Material {material.material_name} successfully added!')
        
    except Exception as e:
        print(f'Error when adding material: {e}')
        
def edit_material():
    material_id = int(input('Enter the ID of the material you want to edit: '))
    material = TrainingMaterials.get_or_none(TrainingMaterials.material_id == material_id)
    
    if not material:
        print('Error! Material not found!')
        return
    
    training_id = int(input(f'Enter the new training ID ({material.training_id}): '))
    material_name = input(f'Enter a new name for the material ({material.material_name}): ')
    file_path = input(f'Enter the new file path ({material.file_path}): ')
    description = input(f'Enter a new description ({material.description}): ')
    
    try:
        material.training_id = training_id
        material.material_name = material_name
        material.file_path = file_path
        material.description = description
        material.save()
        
        print(f'Material {material.material_name} successfully updated!')
    
    except Exception as e:
        print(f'Error! Material data not updated: {e}!')

def get_all_materials():
    materials = TrainingMaterials.select()
    
    if materials:
        for material in materials:
            print(f'ID: {material.material_id} | training_id: {material.training_id} | file_path: {material.file_path} | description: {material.description}')
    else:
        print('There are no materials available for viewing!')
        
def get_material():
    material_id = int(input('Enter material ID: '))
    material = TrainingMaterials.get_or_none(TrainingMaterials.material_id == material_id)
    
    if material:
        print('Material Details:')
        
        print(f'Material name: {material.material_name}')
        print(f'Training ID: {material.training_id}')
        print(f'File path: {material.file_path}')
        print(f'Description: {material.description}')
        

        
    
    
