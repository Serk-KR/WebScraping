# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 13:30:54 2020

@author: Sergi
"""

# Hacemos los imports necesarios
import requests
from bs4 import BeautifulSoup as bs

# Cargamos la información de la página web
pag_web = requests.get("https://www.mustang.es/es/")
code_req = pag_web.status_code

if code_req != 200:
    print("Página web inaccesible")
    exit -1
else:
    print("Página web accesible")

content = bs(pag_web.content)
#print(content.prettify)

nav_menu = content.find("nav", attrs={"class": "menu dark hero menuhead"})
#print(nav_menu.prettify)
#menu = nav_menu.find("div", attrs={"class": "middle"}).find("ul")
menu = nav_menu.find("div", attrs={"class": "middle"})
#print(menu)


for ultag in menu.find_all('ul'):
    print("111111111111111111111111111111111111111111111111111111")
    print(ultag)
    for litag in ultag.find_all('li'):
        print("2222222222222")
        print("  - " + litag.text + ": " + litag.find("a").text)