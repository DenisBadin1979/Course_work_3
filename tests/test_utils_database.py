import unittest
from unittest.mock import MagicMock, patch

from src.utils_database import (
    create_database,
    create_tables,
    employees_insert,
    vacancies_insert,
)


class TestDatabaseFunctionsWithMocks(unittest.TestCase):
    """Тесты с мокингом для изоляции от реальной БД"""

    @patch("src.utils_database.psycopg2.connect")
    def test_create_database(self, mock_connect):
        """Тест создания БД с мокингом"""
        # Arrange
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Act
        create_database()

        # Assert
        mock_connect.assert_called_once_with(
            host="localhost", database="postgres", user="postgres", password="12345"
        )
        mock_cursor.execute.assert_called_once_with("CREATE DATABASE job_openings")
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch("src.utils_database.psycopg2.connect")
    def test_create_tables(self, mock_connect):
        """Тест создания таблиц с мокингом"""
        # Arrange
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Act
        create_tables()

        # Assert
        mock_connect.assert_called_once_with(
            host="localhost", database="job_openings", user="postgres", password="12345"
        )
        # Проверяем что было два вызова execute (для двух таблиц)
        self.assertEqual(mock_cursor.execute.call_count, 2)
        mock_conn.commit.assert_called()
        mock_cursor.close.assert_called_once()

    @patch("src.utils_database.psycopg2.connect")
    def test_employees_insert(self, mock_connect):
        """Тест вставки компаний с мокингом"""
        # Arrange
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        test_companies = [
            {"employer_id": "1", "employer_name": "Company A"},
            {"employer_id": "2", "employer_name": "Company B"},
        ]

        # Act
        employees_insert(test_companies)

        # Assert
        # Проверяем что execute вызывался для каждой компании
        self.assertEqual(mock_cursor.execute.call_count, 2)

        # Проверяем параметры первого вызова
        first_call_args = mock_cursor.execute.call_args_list[0]
        self.assertEqual(
            first_call_args[0][0],
            "INSERT INTO employees (employer_id, employer_name) VALUES (%s, %s)",
        )
        self.assertEqual(first_call_args[0][1], ("1", "Company A"))

    @patch("src.utils_database.psycopg2.connect")
    def test_vacancies_insert(self, mock_connect):
        """Тест вставки вакансий с мокингом"""
        # Arrange
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        test_vacancies = [
            {
                "employer_id": "1",
                "list_vacancy": [
                    {
                        "vacancy_id": "1001",
                        "name_vacancy": "Python Developer",
                        "salary": 100000,
                        "description": "Python development",
                        "url": "http://example.com",
                    }
                ],
            }
        ]

        # Act
        vacancies_insert(test_vacancies)

        # Assert
        mock_cursor.execute.assert_called_once()

        # Проверяем параметры вызова
        call_args = mock_cursor.execute.call_args
        expected_sql = """INSERT INTO vacancies (vacancy_id, employer_id, name_vacancy, salary, description, url)
VALUES (%s, %s, %s, %s, %s, %s)"""
        self.assertEqual(call_args[0][0], expected_sql)

        expected_params = (
            "1001",
            "1",
            "Python Developer",
            100000,
            "Python development",
            "http://example.com",
        )
        self.assertEqual(call_args[0][1], expected_params)
