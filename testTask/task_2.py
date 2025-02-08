import psycopg2
import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine

from db_config import db_name, db_user, db_password

# путь к CSV файлу с данными
path_to_csv_file = "C:\\google_dataset.csv"
# --- --- ---


# функция для добавления значений на столбцы диаграммы (сколько чел. пришло за конкретную дату)
def addlabels(x, y):
    for i in range(len(x)):
        plt.text(i, y.iloc[i] // 2, y.iloc[i], ha='center')
# --- --- ---


# создание движка для импорта данных из PostgreSQL в Pandas с сохранением названий столбцов
engine = create_engine(f'postgresql+psycopg2://{db_user}:{db_password}@localhost/{db_name}')
# --- --- ---

conn = psycopg2.connect(dbname=db_name, user=db_user,
                        password=db_password, host='localhost')

with conn:
    with conn.cursor() as cursor:
        # создание таблицы для копирования в неё существующего CSV файла
        create_table_query = '''CREATE TABLE IF NOT EXISTS test_task_table
                                  (event_id INT NOT NULL,
                                  event_date TEXT NOT NULL, 
                                  customer_id INT NOT NULL,
                                  is_attend INT,
                                  group_ids INT NOT NULL,
                                  teacher_ids INT NOT NULL,
                                  attendance_id INT NOT NULL);'''
        cursor.execute(create_table_query)
        conn.commit()
        # --- --- ---

        # заполнение таблицы данными из CSV файла (делается 1 раз, чтобы не было повторного копирования всех данных)

        # copy_file_query = f'''COPY test_task_table FROM
        #         '{path_to_csv_file}'
        #         DELIMITER ',' CSV HEADER'''
        # cursor.execute(copy_file_query)
        # conn.commit()

        # --- --- ---

        # выбор колонок "дата" и "тренировка посещена"
        sort_by_query = '''SELECT event_date, is_attend FROM test_task_table 
        ORDER BY event_date;'''
        # --- --- ---

        # создание и группировка датафрейма на основе выбранных данных
        df = pd.read_sql_query(sort_by_query, engine)
        grouped_df = df.groupby("event_date", dropna=False).sum()
        print(grouped_df)
        # --- --- ---

        # визуализация итогового датафрейма
        plt.bar(grouped_df.index, grouped_df["is_attend"])
        plt.xticks(rotation=90)
        plt.ylabel("Посетили за день (чел.)")
        plt.xlabel("Дата")
        plt.tight_layout()
        addlabels(grouped_df.index, grouped_df["is_attend"])
        plt.show()
        # --- --- ---

conn.close()
