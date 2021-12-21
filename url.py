import urllib.request
from bs4 import BeautifulSoup

def list_url(link):
    fp = urllib.request.urlopen(link)
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()

    soup = BeautifulSoup(mystr, "html.parser")

    new = []
    for tag in soup.find_all(['a']):  # Mention HTML tag names here.

        link = str(tag).replace("<a href", "")
        link = link.replace("\"", "")
        link = link.replace("=", "")
        link = link.replace("</a>", "")
        link = link.replace(">", "$#@%").strip()

        if ("/pantry/" in link and "<a" not in link):
            new.append(link.split("$#@%"))

    # for i in new:
    #     a = "http://mapping.littlefreepantry.org/" + str(new[i][0])
    #     print(new[i][0])
    #     i +=

    only_url = []
    for i in range(len(new)):
        # new[i][0] = ("http://mapping.littlefreepantry.org{}".format(new[i][0]))
        only_url.append("http://mapping.littlefreepantry.org{}".format(new[i][0]))

    return only_url