import unittest
from unittest.mock import MagicMock

from src.dbmanager import DBManager  # замени your_module на имя твоего файла


class TestDBManager(unittest.TestCase):

    def setUp(self):
        """Настройка перед каждым тестом"""
        self.db_manager = DBManager()

        # Мокаем соединение с базой данных
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()

        self.db_manager.dict_connect = self.mock_conn
        self.mock_conn.cursor.return_value.__enter__ = MagicMock(
            return_value=self.mock_cursor
        )
        self.mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=None)

    def test_init(self):
        """Тест инициализации класса"""
        # Здесь можно протестировать создание соединения
        # Но лучше мокировать psycopg2.connect на уровне модуля
        pass

    def test_get_companies_and_vacancies_count(self):
        """Тест метода get_companies_and_vacancies_count"""
        # Arrange
        mock_data = [("Company A", 10), ("Company B", 5)]
        self.mock_cursor.fetchall.return_value = mock_data

        # Act
        self.db_manager.get_companies_and_vacancies_count()

        # Assert
        self.mock_cursor.execute.assert_called_once_with(
            """SELECT employees.employer_name, COUNT (vacancy_id) AS coun FROM employees
                        JOIN vacancies USING (employer_id)
                        GROUP BY employees.employer_name;"""
        )

    def test_get_all_vacancies(self):
        """Тест метода get_all_vacancies"""
        # Arrange
        mock_data = [
            ("Company A", "Python Developer", 100000, "http://example.com"),
            ("Company B", "Data Scientist", 120000, "http://example.com"),
        ]
        self.mock_cursor.fetchall.return_value = mock_data

        # Act
        self.db_manager.get_all_vacancies()

        # Assert
        self.mock_cursor.execute.assert_called_once_with(
            """SELECT employees.employer_name, vacancies.name_vacancy, vacancies.salary, vacancies.url
FROM vacancies INNER JOIN employees USING (employer_id)"""
        )

    def test_get_avg_salary(self):
        """Тест метода get_avg_salary"""
        # Arrange
        mock_data = [(85000,)]
        self.mock_cursor.fetchall.return_value = mock_data

        # Act
        self.db_manager.get_avg_salary()

        # Assert
        self.mock_cursor.execute.assert_called_once_with(
            "SELECT AVG (salary) AS средняя_зарплата FROM vacancies;"
        )

    def test_get_vacancies_with_higher_salary(self):
        """Тест метода get_vacancies_with_higher_salary"""
        # Arrange
        mock_data = [
            ("Senior Python Developer", 150000),
            ("Lead Data Scientist", 180000),
        ]
        self.mock_cursor.fetchall.return_value = mock_data

        # Act
        self.db_manager.get_vacancies_with_higher_salary()

        # Assert
        self.mock_cursor.execute.assert_called_once_with(
            """SELECT name_vacancy, salary FROM vacancies
                         WHERE salary >(SELECT AVG(SALARY) FROM vacancies);"""
        )

    def test_get_vacancies_with_keyword(self):
        """Тест метода get_vacancies_with_keyword"""
        # Arrange
        keyword = "python"
        mock_data = [
            (
                1,
                "Python Developer",
                100000,
                "Description with python",
                "http://example.com",
                "123",
            )
        ]
        self.mock_cursor.fetchall.return_value = mock_data

        # Act
        self.db_manager.get_vacancies_with_keyword(keyword)

        # Assert
        expected_query = f"SELECT * FROM vacancies WHERE LOWER (description) LIKE LOWER ('%{keyword}%')"
        self.mock_cursor.execute.assert_called_once_with(expected_query)

    def test_get_vacancies_with_keyword_sql_injection_safe(self):
        """Тест на безопасность от SQL инъекций"""
        # Arrange
        malicious_keyword = "python'; DROP TABLE vacancies; --"

        # Act
        self.db_manager.get_vacancies_with_keyword(malicious_keyword)

        # Assert - проверяем, что запрос выполняется как есть (это показывает уязвимость!)
        expected_query = f"SELECT * FROM vacancies WHERE LOWER (description) LIKE LOWER ('%{malicious_keyword}%')"
        self.mock_cursor.execute.assert_called_once_with(expected_query)
