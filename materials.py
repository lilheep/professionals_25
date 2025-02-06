from models import MaterialCards, TrainingMaterials, TrainingOrganizators
from datetime import date

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
    try:
        card_id = int(input('Enter the ID of the material you want to edit: '))
        material = MaterialCards.get(MaterialCards.card_id == card_id)
    except Exception as e:
        print(f'Error, invalid ID! Detail: {e}')
        return
        
    def get_new_value(field_name, old_value):
        new_value = input(f'{field_name} ({old_value})').strip()
        if new_value:
            return new_value
        else:
            return old_value
        
    new_training_material_id = int(input(f'Enter new ID training material ({material.training_material_id.training_id}): '))
    if new_training_material_id:
        try:
            new_training_material = TrainingMaterials.get(TrainingMaterials.training_id == new_training_material_id)
            material.training_material_id = new_training_material
        except Exception as e:
            print(f'Error, invalid training material ID! Detail: {e}')
            return
        
    material.material_name = get_new_value('Material name: ', material.material_name)
    material.approval_date = get_new_value('Approval date (YYYY-MM-DD): ', material.approval_date)
    material.upload_date = date.today()
    material.status = get_new_value('Status(Approved, Checked, Canceled): ', material.status)
    material.material_type = get_new_value('Material type: ', material.material_type)
    material.area = get_new_value('Area: ', material.area)
    new_author_id = int(input(f'Enter new author ID ({material.author.organizator_id if material.author else "None"}): '))
    
    if new_author_id:
        try:
            new_author = TrainingOrganizators.get(TrainingOrganizators.organizator_id == new_author_id)
            material.author = new_author
        except Exception as e:
            print(f'Error, invalid author ID! Detail: {e}')
            return
        
    material.description = get_new_value('Description: ', material.description)
    
    try:
        material.save()
        print(f'Succeffully updated material {material.material_name}')
    except Exception as e:
        print(f'Error updated material! Detail: {e}')
             
def get_material():
    card_id = int(input('Enter the ID of the material you want to get: '))
    try:    
        material = MaterialCards.get(MaterialCards.card_id == card_id)
        print(f'Material ID: {material.card_id}')
        print(f'ID training material: {material.training_material_id}')
        print(f'Material name: {material.material_name}')
        print(f'Approval date: {material.approval_date}')
        print(f'Upload date: {material.upload_date}')
        print(f'Status: {material.status}')
        print(f'Type material: {material.material_type}')
        print(f'Area: {material.area}')
        print(f'Author ID: {material.author}')
        print(f'Description: {material.description}')
    except Exception as e:
        print(f'Error, material not found! Detail: {e}')
        
def get_all_materials():
    materials = MaterialCards.select()
    
    if materials.count() == 0:
        print('Materials not found!')
        return
    
    try:    
        for material in materials:
            print(f'Material ID: {material.card_id} | ID training material: {material.training_material_id} | Material name: {material.material_name} | Approval date: {material.approval_date} | Upload date: {material.upload_date} | Status: {material.status} | Type material: {material.material_type} | Area: {material.area} | Author ID: {material.author.organizator_id if material.author else "None"} | Description: {material.description}')
    except Exception as e:
        print(f'Error! Detail: {e}')     