import psycopg2


def create_database ()-> None:
    """Функция создает базу данных в PostgreSQL"""
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

def create_tables() -> None:
    """Функция создает таблицы в базе данных"""
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
    cur.close()

def employees_insert(list_companies : list) -> None:
    """Функция заполнения таблицы employees"""
    conn2 = psycopg2.connect(
        host="localhost",
        database="job_openings",
        user="postgres",
        password="12345"
    )
    conn2.autocommit = True
    cur = conn2.cursor()
    for record in list_companies:
        cur.execute(
            "INSERT INTO employees (employer_id, employer_name) VALUES (%s, %s)",
            (record['employer_id'], record['employer_name'])
        )
    conn2.commit()
    cur.close()


def vacancies_insert(list_vac : list) -> None:
    """Функция получает список вакансий по каждой компании и заполняет таблицу vacancies"""
    conn2 = psycopg2.connect(
        host="localhost",
        database="job_openings",
        user="postgres",
        password="12345"
    )
    conn2.autocommit = True
    cur = conn2.cursor()

    for i in list_vac:
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


