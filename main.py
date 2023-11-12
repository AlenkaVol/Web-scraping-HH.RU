import requests
import time
import json
from bs4 import BeautifulSoup
from fake_headers import Headers


def get_links():
    headers_gen = Headers(os='win', browser='chrome')
    main_hh = requests.get(
        'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page=0',
        headers=headers_gen.generate())
    if main_hh.status_code != 200:
        return
    main_hh_html = main_hh.text
    main_soup = BeautifulSoup(main_hh_html, 'lxml')
    # вычисляем количество страниц
    count_pages = int(main_soup.find('div', class_="pager").find_all('span', recursive=False)[-1].find('a').
                      find('span').text)
    for page in range(count_pages):
        data = requests.get(
            f'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2&page={page}',
            headers=headers_gen.generate())
        if data.status_code != 200:
            continue
        data_html = data.text
        soup = BeautifulSoup(data_html, 'lxml')
        vacancies = soup.find_all('a', class_="serp-item__title")
        for vacancy in vacancies:
            yield vacancy['href']
        time.sleep(1)


def get_vacancies(link):
    headers_gen = Headers(os='win', browser='chrome')
    data = requests.get(url=link, headers=headers_gen.generate())
    if data.status_code != 200:
        return
    data_html = data.text
    soup = BeautifulSoup(data_html, 'lxml')
    try:
        description = soup.find('div', class_="g-user-content").text
    except:
        description = ''
    if "django" and "flask" in description.lower():
        try:
            name = soup.find(class_='bloko-header-section-1').text
        except:
            name = ''
        try:
            salary = (soup.find('div', class_="vacancy-title").
                      find('span', class_='bloko-header-section-2_lite').text.replace(' ', ' '))
        except:
            salary = 'з/п не указана'
        try:
            сompany_name = soup.find(class_='vacancy-company-name').text.replace(' ', ' ')
        except:
            сompany_name = ''
        try:
            city = soup.find('div', class_='vacancy-company-redesigned').find('p').text.split(', ')[0]
        except:
            city = 'error'
        if city == 'error':
            city = (soup.find('div', class_='vacancy-company-redesigned').find
            ('a', class_='bloko-link_disable-visited').text.split(', ')[0])
        vacancy_data = {
            'name': name,
            'link': link,
            'salary': salary,
            'сompany_name': сompany_name,
            'city': city
            }
        return vacancy_data
    else:
        return "no"


def get_vacancies_dollars(link):
    headers_gen = Headers(os='win', browser='chrome')
    data = requests.get(url=link, headers=headers_gen.generate())
    if data.status_code != 200:
        return
    data_html = data.text
    soup = BeautifulSoup(data_html, 'lxml')
    try:
        description = soup.find('div', class_="g-user-content").text
    except:
        description = ''
    try:
        salary = (soup.find('div', class_="vacancy-title").
                  find('span', class_='bloko-header-section-2_lite').text.replace(' ', ' '))
    except:
        salary = 'з/п не указана'
    if "django" and "flask" in description.lower() and "$" in salary:
        try:
            name = soup.find(class_='bloko-header-section-1').text
        except:
            name = ''
        try:
            сompany_name = soup.find(class_='vacancy-company-name').text.replace(' ', ' ')
        except:
            сompany_name = ''
        try:
            city = soup.find('div', class_='vacancy-company-redesigned').find('p').text.split(', ')[0]
        except:
            city = 'error'
        if city == 'error':
            city = (soup.find('div', class_='vacancy-company-redesigned').find
            ('a', class_='bloko-link_disable-visited').text.split(', ')[0])
        vacancy_data = {
            'name': name,
            'link': link,
            'salary': salary,
            'сompany_name': сompany_name,
            'city': city
            }
        return vacancy_data
    else:
        return "no"


if __name__ == '__main__':
    parsed_data = []
    for link in get_links():
        if get_vacancies(link) != "no":
            parsed_data.append(get_vacancies(link))
            time.sleep(1)
        with open('vacancies_python.json', 'w', encoding='utf-8') as f:
            json.dump(parsed_data, f, indent=4, ensure_ascii=False)

# if __name__ == '__main__':
#     parsed_data_dollars = []
#     for link in get_links():
#         if get_vacancies_dollars(link) != "no":
#             parsed_data_dollars.append(get_vacancies_dollars(link))
#             time.sleep(1)
#         with open('vacancies_python_dollars.json', 'w', encoding='utf-8') as f:
#             json.dump(parsed_data_dollars, f, indent=4, ensure_ascii=False)


