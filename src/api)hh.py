from typing import Any
import json
import requests
from mypy.dmypy.client import request


def api_hh_companies (list_id: list[str]) -> list[dict[str, Any]]:
    pass




# params = {'employer_id' :'2523'}
#
# sss = requests.get ('https://api.hh.ru/employers', params=params)
# data = sss.json()
# tttt = data.get('items')
# # for i in tttt:
# #     print(i)
# print(tttt)


def vacansies_work (list_companies: list[dict[str, str]]) -> list[dict[Any]]:
    for i_list in list_companies:
        id_c = i_list['employer_id']
        params = {'employer_id' : id_c}
        sss = requests.get ('https://api.hh.ru/vacancies', params=params)
        data = sss.json()

tttt = data.get('items')
for i in tttt:
    print(i)

# print(tttt)