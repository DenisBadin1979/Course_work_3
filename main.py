# print('Пожалуйста введите id работодателя и его наименование, не менее 10')
#
#
# list_companies = []
# while len(list_companies) < 10:
#     employer_id = str(input('Введите номер id  работодателя:_ '))
#     employer_name = str(input('Введите имч работодателя работодателя:_ '))
#     dict_companies = {'employer_id' : employer_id, 'employer_name' : employer_name}
#     list_companies.append(dict_companies)
#
# print(list_companies)
from mypy.nodes import local_definitions

if __name__ == '__main__':
    l = [{'employer_id': '1', 'employer_name': 'щ'},
         {'employer_id': '2', 'employer_name': 'в'},
         {'employer_id': '3', 'employer_name': 'с'},
         {'employer_id':  '5', 'employer_name': 'в'},
         {'employer_id': '1в', 'employer_name': '1в'},
         {'employer_id': '1в', 'employer_name': '1'},
         {'employer_id': 'вввв', 'employer_name': '1111в'},
         {'employer_id': '166в', 'employer_name': 'ввав'},
         {'employer_id': '1666', 'employer_name': '1366'},
         {'employer_id': '1666', 'employer_name': 'вввв'}]

    fun  = vacansies_work (l)