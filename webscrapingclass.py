# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 19:00:51 2020

@author: Sergi, Luís
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

class WebScraping():
    
    def download_html(self, url):
        response = urlopen(url)
        html = response.read()
        return html
    
    def get_nav_menu(self, html):
        content = bs(html, 'html.parser')
        nav_menu = content.find("nav", attrs={"class": "menu dark hero menuhead"})
        #menu_todo = nav_menu.find("div", attrs={"class": "middle"}).find("ul").find_all("li")[0]
        menu_todo = nav_menu.find("div", attrs={"class": "middle"}).find_all("ul")[0]
        menu_todo3 = nav_menu.find("div", attrs={"class": "middle"}).find_all("ul")
        
        for idx, ultag in enumerate(menu_todo3):
            print("Inidice: " + str(idx))
            print("ultag-------------------")
            print(ultag)
            if idx == 0:
                print(ultag.find_all("a", hrefs=True))
            
        
        print("menu_todo")
        print(menu_todo)
        print(menu_todo.find_all('ul'))
        for idx, ultag in enumerate(menu_todo.find_all('ul')):
            print("Inidice: " + str(idx))
            hrefs = ultag
            print("hrefs")
            print(hrefs)
        #for idx, ultag in enumerate(menu.find_all('ul')):
        #    print("Inidice: " + str(idx))
        #
        #    print("111111111111111111111111111111111111111111111111111111")
        #    print(ultag)
        #    for litag in ultag.find_all('li'):
        #        print("2222222222222")
        #        print("  - " + litag.text + ": " + litag.find("a").text)
    
    def prueba(self):
        print("aaa")