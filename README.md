# Task tracker for employees
Трекер задач сотрудников

## Технологии
![alt text](https://img.shields.io/badge/fastapi-0.104.1-%23009688?logo=fastapi&labelColor=hsl)
![alt text](https://img.shields.io/badge/pydantic-2.5.2-%23E92063?logo=pydantic&labelColor=hsl)
![alt text](https://img.shields.io/badge/alembic-1.12.1-%23E95420?logo=alembic&labelColor=hsl)
![alt text](https://img.shields.io/badge/sqlalchemy-2.0.23-%23D71F00?logo=sqlalchemy)
![alt text](https://img.shields.io/badge/swagger-1.7.1-%2385EA2D?logo=swagger)


## Установка

1. Скачайте проект в домашнюю директорию. 
```ini
https://github.com/Pvl1307/Task_tracker_for_employees.git
```
2. Активируйте виртуальное окружение командой: 
```ini
poetry shell
```
Если poetry не установлен, пропишите 
```ini
pip install poetry
```

3. Установите зависимости командой: poetry install.

Создайте Базу данных (в данной работе используется PostgreSQL) и перейдите в src/core/.env.sample и пропишите переменные
окружения в формате(все данные после "=" в виде примера):

```ini
DB_NAME=ttfe
DB_USER=postgres
DВ_PASS=postgres
DB_HOST=localhost
DB_PORT=5432
```
После создания пропишите команду 
```ini
alembic upgrade head
```
***

## Работа кода

Зайди в src/main.py и прожмите **RUN** или в терминале пропишите команду 
```ini
python3 src/main.py
```
 
или 
```ini
uvicorn src.main:app --reload
```

## Для завершения работы

Прожмите кнопку **STOP** или в терминале прожмите комбинацию ```CTRL + C```
