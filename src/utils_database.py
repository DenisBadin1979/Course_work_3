import psycopg2

from src.api_hh import vacansies_work

l = [{'employer_id': '3809', 'employer_name': 'СИБУР'},
         {'employer_id': '3077756', 'employer_name': 'РН-Учет'},
         {'employer_id': '1604297', 'employer_name': 'Башнефть -розница'},
         {'employer_id': '4154423', 'employer_name': 'Изи Лоджистик'},
         {'employer_id': '80073', 'employer_name': 'БУРИНТЕХ'},
         {'employer_id': '73358', 'employer_name': 'МТУ Кристалл'},
         {'employer_id': '3127', 'employer_name': 'Мегафон'},
         {'employer_id': '1147771', 'employer_name': 'АПК Алексеевский'},
         {'employer_id': '2523', 'employer_name': 'М-Видео'},
         {'employer_id': '78638', 'employer_name': 'Т-Банк'}]
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="12345"
)
conn.autocommit = True
cur = conn.cursor()
cur.execute("CREATE DATABASE job_openings")
conn.commit()
cur.close()

#Создание таблицы employees
conn2 = psycopg2.connect(
    host="localhost",
    database="job_openings",
    user="postgres",
    password="12345"
)
conn2.autocommit = True
cur = conn2.cursor()
cur1  = ("""CREATE TABLE employees(
employer_id VARCHAR(10) PRIMARY KEY,
employer_name VARCHAR(100) NOT NULL);""")
cur.execute(cur1)
conn2.commit()


#Создание таблицы vacancies
cur2  = ("""CREATE TABLE vacancies(
vacancy_id CHAR(4) PRIMARY KEY,
employer_id VARCHAR(10) REFERENCES employees (employer_id) NOT NULL,
name_vacancy TEXT NOT NULL,
salary INTEGER NOT NULL,
description TEXT,
url TEXT NOT NULL
);""")
cur.execute(cur2)
conn2.commit()
# Заполняем таблицу employees
for record in l:
    cur.execute(
        "INSERT INTO employees (employer_id, employer_name) VALUES (%s, %s)",
        (record['employer_id'], record['employer_name'])
    )
# Заполняем таблицу vacancies
fun = vacansies_work(l)
for i in fun:
    employer_id = i.get('employer_id')
    for s in i.get('list_vacancy'):
        vacancy_id = s.get('vacancy_id')
        name_vacancy = s.get('name_vacancy')
        salary = s.get('salary')
        description = s.get('description')
        url = s.get('url')

        dict_si = {'vacancy_id': vacancy_id,
                   'employer_id': employer_id,
                   'name_vacancy': name_vacancy,
                   'salary': salary,
                   'description': description,
                   'url': url}
        cur.execute(
            """INSERT INTO vacancies 
            (vacancy_id, employer_id, name_vacancy, salary, description, url) 
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (dict_si['vacancy_id'],
             dict_si['employer_id'],
             dict_si['name_vacancy'],
             dict_si['salary'],
             dict_si['description'],
             dict_si['url'])
        )

conn2.commit()


cur.close()
#
