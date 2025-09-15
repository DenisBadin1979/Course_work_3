from typing import Any
import json
import requests
from mypy.dmypy.client import request


def api_hh_companies (list_id: list[str]) -> list[dict[str, Any]]:
    pass




params = {'text' : 'ПАО «НК «Роснефть» - Алтайнефтепродукт" '}

sss = requests.get ('https://api.hh.ru/employers', params=params)
data = sss.json()
tttt = data.get('items')
for i in tttt:
    print(i)

