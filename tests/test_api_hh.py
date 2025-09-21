import unittest
from unittest.mock import patch, Mock
from src.api_hh import vacansies_work  # замени your_module на имя твоего файла


class TestVacanciesWork(unittest.TestCase):

    def setUp(self):
        """Подготовка тестовых данных"""
        self.sample_companies = [
            {"employer_id": "123"},
            {"employer_id": "456"}
        ]

        # Пример ответа от API hh.ru
        self.mock_api_response = {
            "items": [
                {
                    "name": "Python Developer",
                    "salary": {"to": 100000, "from": 50000},
                    "snippet": {"responsibility": "Разработка приложений"},
                    "area": {"url": "https://example.com/area1"},
                    "id": "vacancy1"
                },
                {
                    "name": "Data Scientist",
                    "salary": None,
                    "snippet": {"responsibility": "Анализ данных"},
                    "area": {"url": "https://example.com/area2"},
                    "id": "vacancy2"
                },
                {
                    "name": "Frontend Developer",
                    "salary": {"to": None, "from": 70000},
                    "snippet": {"responsibility": "Верстка интерфейсов"},
                    "area": {"url": "https://example.com/area3"},
                    "id": "vacancy3"
                }
            ]
        }

    @patch('src.api_hh.requests.get')
    def test_vacancies_work_success(self, mock_requests_get):
        """Тест успешного выполнения функции"""
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = self.mock_api_response
        mock_requests_get.return_value = mock_response

        # Act
        result = vacansies_work(self.sample_companies)

        # Assert
        self.assertEqual(len(result), 2)  # Две компании

        # Проверяем структуру результата для первой компании
        first_company = result[0]
        self.assertEqual(first_company["employer_id"], "123")
        self.assertEqual(len(first_company["list_vacancy"]), 3)

        # Проверяем корректность преобразования данных
        first_vacancy = first_company["list_vacancy"][0]
        self.assertEqual(first_vacancy["name_vacancy"], "Python Developer")
        self.assertEqual(first_vacancy["salary"], 100000)  # Должен взять "to"
        self.assertEqual(first_vacancy["description"], "Разработка приложений")
        self.assertEqual(first_vacancy["vacancy_id"], 1000)

    @patch('src.api_hh.requests.get')
    def test_vacancies_work_salary_handling(self, mock_requests_get):
        """Тест обработки различных случаев зарплаты"""
        mock_response = Mock()
        mock_response.json.return_value = self.mock_api_response
        mock_requests_get.return_value = mock_response

        result = vacansies_work(self.sample_companies)
        vacancies = result[0]["list_vacancy"]

        # Проверяем зарплату для разных случаев
        self.assertEqual(vacancies[0]["salary"], 100000)  # Есть "to"
        self.assertEqual(vacancies[1]["salary"], 0)  # salary = None
        self.assertEqual(vacancies[2]["salary"], 70000)  # "to" = None, есть "from"

    @patch('src.api_hh.requests.get')
    def test_vacancies_work_id_generation(self, mock_requests_get):
        """Тест генерации vacancy_id"""
        mock_response = Mock()
        mock_response.json.return_value = {"items": [self.mock_api_response["items"][0]]}
        mock_requests_get.return_value = mock_response

        result = vacansies_work(self.sample_companies)

        # Проверяем, что ID генерируются правильно
        first_company_vacancies = result[0]["list_vacancy"]
        second_company_vacancies = result[1]["list_vacancy"]

        self.assertEqual(first_company_vacancies[0]["vacancy_id"], 1000)
        # Вторая компания должна начинаться с 1100 (1000 + 100)
        self.assertEqual(second_company_vacancies[0]["vacancy_id"], 1100)

    @patch('src.api_hh.requests.get')
    def test_vacancies_work_empty_items(self, mock_requests_get):
        """Тест с пустым списком вакансий"""
        mock_response = Mock()
        mock_response.json.return_value = {"items": []}
        mock_requests_get.return_value = mock_response

        result = vacansies_work(self.sample_companies)

        self.assertEqual(len(result[0]["list_vacancy"]), 0)
        self.assertEqual(len(result[1]["list_vacancy"]), 0)

    @patch('src.api_hh.requests.get')
    def test_vacancies_work_api_error(self, mock_requests_get):
        """Тест обработки ошибки API"""
        mock_requests_get.side_effect = Exception("API недоступно")

        with self.assertRaises(Exception):
            vacansies_work(self.sample_companies)

    def test_vacancies_work_empty_input(self):
        """Тест с пустым входным списком"""
        result = vacansies_work([])
        self.assertEqual(result, [])


