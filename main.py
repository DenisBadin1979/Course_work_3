# if __name__ == '__main__':
#     print('Hello')
import requests

params = {'employer_id' : '1490605'}

sss = requests.get ('https://api.hh.ru/vacancies', params=params)
data = sss.json()
print(data)
tttt = data.get('items')
for i in tttt:
    print(i)