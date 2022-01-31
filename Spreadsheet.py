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
    h1tags_main = soup.find_all('h1')

    for singleTag in h1tags_main:
        phrase = singleTag.text.replace("Mini Pantry Movement", "").replace("\n", "")
        phrase = str(" ".join(phrase.split()))
        if phrase != "":
            elements.insert(0, "(NAME) " + phrase)

    for singleTag in h1tags:
        new = " ".join(singleTag.text.split("<td>"))
        new = new.replace("\n", "").replace("  ", "$^&").replace("Type$^&", "(TYPE) ").replace("Shipping Address$^&",
                                                                                               "(SHIPPING ADDRESS) ").replace(
            "Address$^&", "(ADDRESS) ").replace("Description$^&", "(DESCRIPTION) ").replace("Contact$^&",
                                                                                            "(CONTACT) ").replace("$^&",
                                                                                                                  "")
        # print(new)
        elements.append(new)

    result = []
    result.insert(0, "")
    result.insert(1, "")
    result.insert(2, "")
    result.insert(3, "")
    result.insert(4, "")
    result.insert(5, "")

    for i in range(0, len(elements)):
        if "(NAME) " in elements[i]:
            result.insert(0, elements[i].replace("(NAME) ",""))
        elif "(TYPE) " in elements[i]:
            result.insert(1, elements[i].replace("(TYPE) ",""))
        elif "(ADDRESS) " in elements[i]:
            result.insert(2, elements[i].replace("(ADDRESS) ",""))
        elif "(DESCRIPTION) " in elements[i]:
            result.insert(3, elements[i].replace("(DESCRIPTION) ",""))
        elif "(CONTACT) " in elements[i]:
            result.insert(4, elements[i].replace("(CONTACT) ",""))
        elif "(SHIPPING ADDRESS) " in elements[i]:
            result.insert(5, elements[i].replace("(SHIPPING ADDRESS) ",""))

    return result


def none_element(ele):
    if (len(ele) != 14):
        for i in range(0, 14- len(ele)):
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
        'contract': 'Contact',
        's_address': 'Shipping Address',
        'lat': 'Latitude',
        "lon": "Longitude",
        "number": "House Number",
        'street': 'Street',
        'typ': "Type",
        'city': 'County/Suburb/Neighbourhood/City',
        'state': 'State',
        'zipcode': 'Zip Code'

    }

    urls = url()
    n = 0
    # print(urls)
    for i in urls:
        n += 1
        elements = ele(i)

        if len(elements) < 6:
            for k in range(len(elements),7):
                elements.append("")
        if len(elements) > 6:
            for asd in range(len(elements),6,-1):
                elements = elements[:-1]


        print(i)
        Latitude = find_address(i)[0]
        Longitude = find_address(i)[1]

        print(n)
        print(Latitude + " " + Longitude)
        number, street, typ, city, state, zipcode = address.find(Latitude, Longitude)
        elements.insert(6, Latitude)
        elements.insert(7, Longitude)
        elements.insert(8, number)
        elements.insert(9, street)
        elements.insert(10, typ)
        elements.insert(11, city)
        elements.insert(12, state)
        elements.insert(13, zipcode)

        print(elements)

        elements = none_element(elements)
        # print(elements)
        items.append({'id': n, 'name': elements[0], 'type': elements[1], 'address': elements[2],
                      'description': elements[3], 'contract': elements[4], 's_address': elements[5], 'lat': elements[6], 'lon': elements[7], 'number': elements[8],
                      'street': elements[9], 'typ': elements[10], 'city': elements[11], 'state': elements[12], 'zipcode': elements[13]})

    create_xlsx_file("my-xlsx-file.xlsx", headers, items)


excel()
