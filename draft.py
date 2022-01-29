from xlsxwriter import Workbook
from bs4 import BeautifulSoup
import requests
import address

def last(lis):
    if lis[len(lis)-1] == "":
        lis = lis[:-1]
        return last(lis)
    else:
        return lis



def every(url):
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
            elements.insert(0, "(NAME) " + phrase)
    all = []
    for singleTag in h1tags:
        new = " ".join(singleTag.text.split("<td>"))
        new = new.replace("\n","").replace("  ","$^&").replace("Type$^&","(TYPE) ").replace("Shipping Address$^&","(SHIPPING ADDRESS) ").replace("Address$^&","(ADDRESS) ").replace("Description$^&","(DESCRIPTION) ").replace("Contact$^&","(CONTACT) ").replace("$^&","")
        # print(new)
        elements.append(new)

    result = []
    result.insert(0,"")
    result.insert(1,"")
    result.insert(2, "")
    result.insert(3, "")
    result.insert(4, "")
    result.insert(5, "")

    for i in range (0, len(elements)):
        if "(NAME) " in elements[i]:
            result.insert(0,elements[i])
        elif "(TYPE) " in elements[i]:
            result.insert(1,elements[i])
        elif "(ADDRESS) " in elements[i]:
            result.insert(2,elements[i])
        elif "(DESCRIPTION) " in elements[i]:
            result.insert(3,elements[i])
        elif "(CONTACT) " in elements[i]:
            result.insert(4,elements[i])
        elif "(SHIPPING ADDRESS) " in elements[i]:
            result.insert(5,elements[i])

    return last(result)

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

print(find_address("http://mapping.littlefreepantry.org/pantry/2781"))