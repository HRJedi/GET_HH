# GET_HH
## Загрузчик JSON ответов по запросу вакансий HH.ru

Используются общедоступные методы API HH.RU без передачи токена авторизации:
1. Поиск вакансий: **GET/vacancies**
2. Просмотр конккретной вакансии: **GET/vacancies/{vacancy_id}**

**Сценарий использования:**
Ответы преобразуются в простую модель данных посредством обработчика **local_dashboard.xlsb**, после чего, могут использоваться для создания произвольных отчётов Excel (Исходя из потребности).
Скрипт и обработчик предназначались для частичной автоматизации процедуры анализа рынка труда сотрудниками HR-отдела не имеющими навыков использования более сложных инструментов.
