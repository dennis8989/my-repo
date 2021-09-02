import requests
from bs4 import BeautifulSoup
r = requests.get("https://renrenbear.com/password-of-payment/")
soup = BeautifulSoup(r.text, "html.parser")
table = soup.select("#tablepress-1")[0]
list_video = table.select("tr")
dict_video = {}
for video in list_video[1:]:
    attr_video = video.select("td")
    name_video = attr_video[1].get_text()
    pwd_video = attr_video[2].get_text()
    dict_video[name_video] = pwd_video

print(dict_video)
for name, pwd in dict_video.items():
    print(pwd)# print(attr_video[2].get_text())
#tablepress-1 > tbody > tr.row-245.odd > td.column-2 > font > font
# id="tablepress-1
pass