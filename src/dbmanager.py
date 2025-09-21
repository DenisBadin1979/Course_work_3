import psycopg2


class DBManager:
    """"Класс DBManager подключатеся к БД PostgreSQL """
    def __init__(self) -> None:
        self.dict_connect = psycopg2.connect(
            host="localhost", database="job_openings", user="postgres", password="12345"
        )
        self.autocommit = True

    def get_companies_and_vacancies_count(self) -> None:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        with self.dict_connect.cursor() as cur:
            cur.execute(
                """SELECT employees.employer_name, COUNT (vacancy_id) AS coun FROM employees
                        JOIN vacancies USING (employer_id)
                        GROUP BY employees.employer_name;"""
            )
            rows = cur.fetchall()
            for row in rows:
                print(row)

    def get_all_vacancies(self) -> None:
        """Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        with self.dict_connect.cursor() as cur:
            cur.execute(
                """SELECT employees.employer_name, vacancies.name_vacancy, vacancies.salary, vacancies.url
FROM vacancies INNER JOIN employees USING (employer_id)"""
            )
            rows = cur.fetchall()
            for row in rows:
                print(row)

    def get_avg_salary(self) -> None:
        """Получает среднюю зарплату по вакансиям."""
        with self.dict_connect.cursor() as cur:
            cur.execute("SELECT AVG (salary) AS средняя_зарплата FROM vacancies;")
            rows = cur.fetchall()
            print(rows)

    def get_vacancies_with_higher_salary(self) -> None:
        """Список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        with self.dict_connect.cursor() as cur:
            cur.execute(
                """SELECT name_vacancy, salary FROM vacancies
                         WHERE salary >(SELECT AVG(SALARY) FROM vacancies);"""
            )
            rows = cur.fetchall()
            for row in rows:
                print(row)

    def get_vacancies_with_keyword(self, keyword) -> None:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        with self.dict_connect.cursor() as cur:
            cur.execute(
                f"SELECT * FROM vacancies WHERE LOWER (description) LIKE LOWER ('%{keyword}%')"
            )
            rows = cur.fetchall()
            for row in rows:
                print(row)
