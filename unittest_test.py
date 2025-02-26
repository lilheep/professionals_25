import unittest

def get_project_details(name):
    """Заглушечка, возвращает данные по проекту"""
    if not name:
        return None
    return {
        "Наименование": name,
        "Руководитель": "Иванов Иван Иванович",
        "Дата начала": "2024-01-01",
        "Дата фактического окончания": "2024-12-31"
    }
    
def get_project_timeline(name):
    """Загулшечка, возвращает данные по этапам проекта"""
    if not name:
        return []
    return [
        {"этап": "Анализ", "цвет": "желток"},
        {"этап": "Разработка", "цвет": "краснуха"},
        {"этап": "Тестирование", "цвет": "синька"}
    ]
    
def export_project_card(name):
    """Возвращает карточку проекта"""
    if not name:
        return None
    return {
        "Наименование": name,
        "Руководитель": "Иванов Иван Иванович",
        "Дата начала": "2024-01-01",
        "Дата фактического окончания": "2024-12-31"
    }
    
class TestProjectManager(unittest.TestCase):
    def test_project_details_director_exists(self):
        "Проверка наличия руководителя у проекта"
        details = get_project_details("Проект примерчек")
        self.assertIn("Руководитель", details)
        self.assertIsNotNone(details["Руководитель"])
        
    def test_project_details_dates(self):
        """"Проверка наличия дат начала и конца проекта"""
        details = get_project_details("Project example")
        self.assertIn("Дата начала", details)
        self.assertIsNotNone(details["Дата начала"])
        self.assertIn("Дата фактического окончания", details)
        self.assertIsNotNone(details["Дата фактического окончания"])
        self.assertLessEqual(details["Дата начала"], details["Дата фактического окончания"])
        
    def test_project_timeline_project(self):
        """Проверка наличия этапов проекта"""
        timeline = get_project_timeline("Вахунтрахен")
        self.assertIsInstance(timeline, list)
        for stage in timeline:
            self.assertIsNotNone(stage["этап"])
        self.assertGreater(len(timeline), 0)
    
    def test_project_vizual_stages(self):
        """Проверка цветовой индикации"""
        timeline = get_project_timeline("Гомункул")
        for stage in timeline:
            self.assertIn("цвет", stage)
            self.assertIsNotNone(stage["цвет"])
    
    def test_project_export_card(self):
        """"Проверка правильности выгрузки карточки проекта"""
        card = export_project_card("Геракл")
        self.assertIn("Наименование", card)
        self.assertIsNotNone(card["Наименование"])
        self.assertIn("Руководитель", card)
        self.assertIsNotNone(card["Руководитель"])
        self.assertIn("Дата начала", card)
        self.assertIsNotNone(card["Дата начала"])
        self.assertIn("Дата фактического окончания", card)
        self.assertIsNotNone(card["Дата фактического окончания"])
        
    def test_empty_project_name(self):
        """Проверка отображения пустого названия проекта"""
        project = get_project_details("")
        self.assertEqual(project, None)
        
    def test_empty_project_in_timeline(self):
        """"Проверка отображения пустого названия проекта для таймлайна"""
        timeline = get_project_timeline("")
        self.assertEqual(len(timeline), 0)
    
    def test_empty_project_employee_card(self):
        """Проверка отображения карточки проекта с пустым названием project'a"""
        card = export_project_card("")
        self.assertIsNone(card)
    
    def test_project_timeline_stage_names(self):
        """Проверка, что все этапы содержат название"""
        timeline = get_project_timeline("Aboba")
        for stage in timeline:
            self.assertIsNotNone(stage['этап'])
        
    def test_project_timeline_stage_colors(self):
        """Проверка, что цветовая индикция содержит строковые значения"""
        timeline = get_project_timeline("bobiboba")
        for stage in timeline:
            self.assertIsInstance(stage['цвет'], str)
        
    