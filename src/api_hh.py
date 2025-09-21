import requests


def vacansies_work(list_companies: list[dict[str, str]]) -> list[dict]:
    """Функция получает список словарей и выводит по id вакансии с сайта hh.ru
    и далее формирует список словарей"""
    dict_vac_comp = []
    count_e = 1000
    for i_list in list_companies:
        id_c = i_list["employer_id"]
        params = {"employer_id": id_c}
        list_vac = requests.get("https://api.hh.ru/vacancies", params=params)
        data = list_vac.json()
        hh_vacancies = data.get("items", [])
        list_vacancy = []
        count_v = count_e
        for i in hh_vacancies:
            nam = i.get("name")
            if i.get("salary") == None:
                salary = 0
            else:
                if i.get("salary").get("to") != None:
                    salary = i.get("salary").get("to")
                else:
                    salary = i.get("salary").get("from")

            description = i.get("snippet").get("responsibility")
            url = i.get("area").get("url")

            dict_vacancy = {
                "vacancy_id": count_v,
                "name_vacancy": nam,
                "salary": salary,
                "description": description,
                "url": url,
            }
            count_v += 1
            list_vacancy.append(dict_vacancy)
        dict_list_vac = {"employer_id": id_c, "list_vacancy": list_vacancy}
        count_e += 100
        dict_vac_comp.append(dict_list_vac)
    return dict_vac_comp
