from models import TrainingMaterials

def add_materials():
    try:
        traning_id = int(input('Введите ID тренинга: '))
        material_name = input('Введите название материала: ')
        file_path = input('Введите путь к файлу: ')
        description = input('Введите описание (необязательно): ')
        
        material = TrainingMaterials.create(
            traning_id=traning_id,
            material_name=material_name,
            file_path=file_path,
            description=description if description else None
        )
        
        print(f'Материал {material_name} с ID {material.material_id} успешно добавлен.') # english :(
    
    except Exception as e:
        print()



class TrainingMaterials(BaseModel):
    material_id = AutoField()
    training_id = ForeignKeyField(TrainingsCalendar, backref='materials', on_delete='CASCADE')
    material_name = CharField(max_length=255, null=False)
    file_path = CharField(max_length=255, null=False)
    description = CharField(max_length=255, null=True)