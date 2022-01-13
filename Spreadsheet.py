from xlsxwriter import Workbook
from bs4 import BeautifulSoup
import requests


def url():
    url = 'http://mapping.littlefreepantry.org/'
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    urls = []
    remove = ['http://www.littlefreepantry.org/', 'http://www.littlefreepantry.org/', '/', '/account/login',
              'http://www.littlefreepantry.org/',
              'http://www.littlefreepantry.org/news/2019/1/24/how-to-map-your-mini-pantry', '/pantry/add',
              'https://www.facebook.com/littlefreepantry/', 'http://instagram.com/littlefreepantry',
              'https://doc4design.com']
    for link in soup.find_all('a'):
        if link.get('href') not in remove:
            urls.append('http://mapping.littlefreepantry.org' + str(link.get('href')))

    return urls


def create_xlsx_file(file_path: str, headers: dict, items: list):
    with Workbook(file_path) as workbook:
        worksheet = workbook.add_worksheet()
        worksheet.write_row(row=0, col=0, data=headers.values())
        header_keys = list(headers.keys())
        for index, item in enumerate(items):
            row = map(lambda field_id: item.get(field_id, ''), header_keys)
            worksheet.write_row(row=index + 1, col=0, data=row)


def ele(url: str):
    respons = requests.get(url).content

    soup = BeautifulSoup(respons, 'lxml')

    h1tags = soup.find_all('tr')

    elements = []
    remove = ['Type ', 'Address ', 'Description ', 'Contact ', 'Shipping Address ']

    h1tags_main = soup.find_all('h1')

    for singleTag in h1tags_main:
        phrase = singleTag.text.replace("Mini Pantry Movement", "").replace("\n", "")
        phrase = str(" ".join(phrase.split()))
        if phrase != "":
            elements.append(phrase)

    for singleTag in h1tags:
        phrase = str(" ".join(singleTag.text.split()))
        for i in remove:
            phrase = phrase.replace(i, "")
        elements.append(phrase)

    return elements


def none_element(ele):
    if (len(ele) != 6):
        for i in range(0, 6 - len(ele)):
            ele.append("")
    return ele


def excel():
    headers = {
        'id': 'User Id',
        'name': 'Full Name',
        'type': 'Type',
        'address': 'Address',
        'description': 'Description',
        'contract': 'Contract',
        'address': 'Shipping Address',
    }

    urls = url()
    n = 0
    for i in urls:
        n += 1
        elements = ele(i)
        elements = none_element(elements)
        print(elements)


#         items.append({'id': n, 'name': elements[0], 'type': elements[1], 'address': elements[2],
#          'description': elements[3], 'contract': elements[4], 'address': elements[5]})

#     create_xlsx_file("my-xlsx-file.xlsx", headers, items)

excel()