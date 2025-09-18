# print('Пожалуйста введите id работодателя и его наименование, не менее 10')
#
#
from src.api_hh import vacansies_work

def dict_companies () -> list[dict]:
    """Функция взаимодействия с пользователем"""
    numbers_companies = int(input('Введите количество компаний:_'))
    list_companies = []
    while len(list_companies) < numbers_companies:
        employer_id = str(input('Введите номер id  работодателя:_ '))
        employer_name = str(input('Введите имч работодателя работодателя:_ '))
        dict_companies = {'employer_id' : employer_id, 'employer_name' : employer_name}
        list_companies.append(dict_companies)
    return list_companies





if __name__ == '__main__':
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



    fun  = vacansies_work (l)
    for i in fun:
        employer_id = i.get('employer_id')
        for s in i.get('list_vacancy'):
            vacancy_id = s.get('vacancy_id')
            name_vacancy = s.get('name_vacancy')
            salary = s.get('salary')
            description = s.get('description')
            url = s.get('url')


            dict_si = {'vacancy_id' : vacancy_id,
                       'employer_id': employer_id,
                       'name_vacancy' : name_vacancy,
                       'salary' : salary,
                       'description' : description,
                       'url' : url
                       }
            print(dict_si)

