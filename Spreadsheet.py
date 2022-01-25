from xlsxwriter import Workbook
from bs4 import BeautifulSoup
import requests
import address

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

def find_address(url):
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')

    para = ""
    for link in soup.find_all('script'):
        para += str(link)
    num = para.find("center: new google.maps.LatLng")
    precise = para[num:num + 80]
    for i in precise:
        if (not i.isdigit()) and (i != ',') and (i != '.') and (i != '-'):
            precise = precise.replace(i, "")
    precise = precise.replace("..", "")
    Latitude, Longitude = precise.split(",")[0], precise.split(",")[1]
    return [Latitude, Longitude]

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
    #     remove = ['Type', 'Shipping', 'Description', 'Contact', 'Address']

    h1tags_main = soup.find_all('h1')

    for singleTag in h1tags_main:
        phrase = singleTag.text.replace("Mini Pantry Movement", "").replace("\n", "")
        phrase = str(" ".join(phrase.split()))
        if phrase != "":
            elements.insert(0, phrase)

    for singleTag in h1tags:
        phrase = str(" ".join(singleTag.text.split()))

        elements.append("")
        elements.append("")
        elements.append("")
        elements.append("")

        if "Type" in phrase[:20]:
            elements.insert(1, phrase)
        elif "Shipping" in phrase[:20]:
            elements.insert(2, phrase)
        elif "Description" in phrase[:20]:
            elements.insert(3, phrase)
        elif "Contact" in phrase[:20]:
            elements.insert(4, phrase)


    try:
        if ("Description" in elements[4]):
            elements.insert(4, elements[3])
            elements.insert(3, "")
    except:
        print("An exception occurred")

    #         for i in remove:
    #             phrase = phrase.replace(i,"")
    #         elements.append(phrase)

    return elements


def none_element(ele):
    if (len(ele) != 11):
        for i in range(0, 11 - len(ele)):
            ele.append("")
    return ele


def excel():
    items = []
    headers = {
        'id': 'User Id',
        'name': 'Full Name',
        'type': 'Type',
        'address': 'Address',
        'description': 'Description',
        'contract': 'Contract',
        'lat': 'Latitude',
        "lon": "Longitude",
        'street': 'Street',
        'city': 'County/Suburb/Neighbourhood/City',
        'state': 'State',
        'zipcode': 'Zip Code'

    }

    urls = url()
    n = 0
    for i in urls:
        n += 1
        elements = ele(i)
        try:
            Latitude = find_address(i)[0]
        except:
            Latitude = ""

        try:
            Longitude = find_address(i)[1]
        except:
            Longitude = ""
        print(n)
        print(Latitude + " " + Longitude)
        if (Longitude != "" or Longitude != ""):
            street, city, state, zipcode = address.find(Latitude, Longitude)
            elements.insert(5, Latitude)
            elements.insert(6, Longitude)
            elements.insert(7, street)
            elements.insert(8, city)
            elements.insert(9, state)
            elements.insert(10, zipcode)

        print(elements)

        elements = none_element(elements)
        # print(elements)
        items.append({'id': n, 'name': elements[0], 'type': elements[1], 'address': elements[2],
                      'description': elements[3], 'contract': elements[4], 'lat': elements[5], 'lon': elements[6],
                      'street': elements[7], 'city': elements[8], 'state': elements[9], 'zipcode': elements[10]})

    create_xlsx_file("my-xlsx-file.xlsx", headers, items)


excel()
