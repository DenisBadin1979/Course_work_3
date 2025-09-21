from src.api_hh import vacansies_work
from src.dbmanager import DBManager
from src.utils_database import (
    create_database,
    create_tables,
    employees_insert,
    vacancies_insert,
)


def dict_companies() -> None:
    """Функция взаимодействия с пользователем"""
    numbers_companies = int(input("Введите количество компаний:_"))
    list_companies : list[dict] = []
    while len(list_companies) < numbers_companies:
        employer_id = str(input("Введите номер id  работодателя:_ "))
        employer_name = str(input("Введите имя работодателя работодателя:_ "))
        dict_companies = {"employer_id": employer_id, "employer_name": employer_name}
        list_companies.append(dict_companies)

    print("# Получаем список вакансий")
    fun = vacansies_work(list_companies)
    print("#Создаем базу данных")
    create_database()
    print("#Создаем таблицы")
    create_tables()
    print("#Заполняем таблицу компаний")
    employees_insert(list_companies)
    print("#Заполняем таблицу с вакансиями")
    vacancies_insert(fun)

    conr = DBManager()
    print("Список всех компаний и количество вакансий у каждой компании")
    conr.get_companies_and_vacancies_count()
    # print("Список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию")
    conr.get_all_vacancies()
    print("Средняя зарплата по вакансиям")
    conr.get_avg_salary()
    print("Список всех вакансий, у которых зарплата выше средней по всем вакансиям.")
    conr.get_vacancies_with_higher_salary()
    keyword = input("Введите ключевое слово, для поиска в описании вакансий:_ ")
    conr.get_vacancies_with_keyword(keyword)


if __name__ == "__main__":
    # Создаем список словарей для проверки, что бы не вызывать функцию взаимодействия с пользователем
    list_i = [
        {"employer_id": "3809", "employer_name": "СИБУР"},
        {"employer_id": "3077756", "employer_name": "РН-Учет"},
        {"employer_id": "1604297", "employer_name": "Башнефть -розница"},
        {"employer_id": "4154423", "employer_name": "Изи Лоджистик"},
        {"employer_id": "80073", "employer_name": "БУРИНТЕХ"},
        {"employer_id": "73358", "employer_name": "МТУ Кристалл"},
        {"employer_id": "3127", "employer_name": "Мегафон"},
        {"employer_id": "1147771", "employer_name": "АПК Алексеевский"},
        {"employer_id": "2523", "employer_name": "М-Видео"},
        {"employer_id": "78638", "employer_name": "Т-Банк"},
    ]

    # print ('# Получаем список вакансий')
    # fun  = vacansies_work (list_i)
    # print ('#Создаем базу данных')
    # create_database()
    # print ('#Создаем таблицы')
    # create_tables()
    # print ('#Заполняем таблицу компаний')
    # employees_insert(l)
    # print ('#Заполняем таблицу с вакансиями')
    # vacancies_insert(fun)

    conr = DBManager()
    # print("Список всех компаний и количество вакансий у каждой компании")
    # conr.get_companies_and_vacancies_count()
    # print("Список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию")
    # conr.get_all_vacancies()
    # conr.get_avg_salary()
    # print("Список всех вакансий, у которых зарплата выше средней по всем вакансиям.")
    # conr.get_vacancies_with_higher_salary()
    keyword = input("Введите ключевое слово, для поиска в описании вакансий:_ ")
    conr.get_vacancies_with_keyword(keyword)
