# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 19:00:51 2020

@author: Sergi, Luís
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

class WebScraping():
    
    def __get_nav_names(self,nav):
        print("PRINT NAV INICIO: -------")
        print(nav)
        print("PRINT NAV FIN: -------")
        for idx, ultag in enumerate(nav.find_all('li')):
            if len(ultag.find_all("li")) > 0:
                #print("Inidice: " + str(idx))
                print("")
                categoriaPadre = ultag.find("a")
                print(categoriaPadre.text + "-> href: " + str(categoriaPadre.get("href")))
                for idx2, categoriaHijo in enumerate(ultag.find_all("li")):
                    print(" -" +categoriaHijo.text + "-> href: " + str(categoriaHijo.find("a").get("href")))
    
    def download_html(self, url):
        response = urlopen(url)
        html = response.read()
        return html
    
    def get_nav_menu(self, html):
        content = bs(html, 'html.parser')
        nav_menu = content.find("nav", attrs={"class": "menu dark hero menuhead"})
        #menu_todo = nav_menu.find("div", attrs={"class": "middle"}).find("ul").find_all("li")[0]
        #menu_todo = nav_menu.find("div", attrs={"class": "middle"}).find_all("ul")[0]
        menu_todo = nav_menu.find("div", attrs={"class": "middle"})
        
        # Mostramos las categorias del menú y su url
        self.__get_nav_names(menu_todo)
        return menu_todo

    
    def prueba(self):
        print("aaa")