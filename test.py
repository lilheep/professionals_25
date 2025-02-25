<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Информация о сотрудниках</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
        }
        .employee-container {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            justify-content: center;
        }
        .employee-card {
            width: calc(33% - 20px);
            background-color: #f9f9f9;
            border: 1px solid #ccc;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .employee-card img {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            object-fit: cover;
            margin-bottom: 15px;
        }
        .employee-card h3 {
            font-size: 1.2rem;
            margin-bottom: 10px;
        }
        .employee-card p {
            font-size: 1rem;
            color: #555;
        }
        @media (max-width: 1100px) {
            .employee-card {
                width: calc(50% - 20px);
            }
        }
        @media (max-width: 600px) {
            .employee-card {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <h1>Информация о сотрудниках</h1>
    <div id="employee-container" class="employee-container"></div>

    <script>
        async function fetchEmployees() {
            try {
                // Получаем данные о сотрудниках через API
                let response = await fetch('http://127.0.0.1:8000/api/employees'); // Убедитесь, что адрес правильный
                let employees = await response.json(); // Предполагается, что API возвращает массив сотрудников
                
                renderEmployees(employees); // Отображаем сотрудников
            } catch (error) {
                console.error(`Ошибка загрузки данных о сотрудниках: ${error}`);
            }
        }

        function renderEmployees(employees) {
            const container = document.getElementById("employee-container");
            container.innerHTML = ''; // Очищаем контейнер перед добавлением новых данных
            
            employees.forEach(employee => {
                const employeeCard = document.createElement("div");
                employeeCard.className = 'employee-card';

                // Заполняем карточку данными сотрудника
                employeeCard.innerHTML = `
                    <img src="${employee.photoUrl}" alt="${employee.name}">
                    <h3>${employee.name}</h3>
                    <p>${employee.position}</p>
                    <p>Отдел: ${employee.department}</p>
                `;
                
                container.appendChild(employeeCard); // Добавляем карточку в контейнер
            });
        }

        // Загружаем сотрудников при загрузке страницы
        fetchEmployees();
    </script>
</body>
</html>
