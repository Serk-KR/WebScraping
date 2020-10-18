# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 19:00:51 2020

@author: Sergi, Luís
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

class WebScraping():

    def __get_nav_names(self,nav):
        #print("PRINT NAV INICIO: -------")
        #print(nav)
        #print("PRINT NAV FIN: -------")
        categorias = []
        for idx, ultag in enumerate(nav.find_all('li')):
            if len(ultag.find_all("li")) > 0:
                #print("Inidice: " + str(idx))
                #print("")
                itemCategoria = []
                categoriaPadre = ultag.find("a")
                itemCategoria.append((categoriaPadre.text, categoriaPadre.get("href")))
                #print(categoriaPadre.text + "-> href: " + str(categoriaPadre.get("href")))
                for idx2, categoriaHijo in enumerate(ultag.find_all("li")):
                    itemCategoria.append((categoriaHijo.text, categoriaHijo.find("a").get("href")))
                    #print(" -" +categoriaHijo.text + "-> href: " + str(categoriaHijo.find("a").get("href")))
                categorias.append(itemCategoria)
        return categorias
    
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
        categorias = self.__get_nav_names(menu_todo)
        return categorias
    
    def read_category(self, navmenu):
        print("Escoger categoria: ")
        for categories in navmenu:
            for item_category in categories:    
                print(item_category[0])
            print("--------")
        
    def get_links_pagination(self, html):
        content = bs(html, 'html.parser')
        enlaces = []
        for item in content.select('div.pagination a[href]'):
            enlaces.append(item.get("href"))
        return enlaces
    
    def get_productos(self, html):
        html = self.download_html(html)
        content = bs(html, 'html.parser')
        productos = []
        for div in content.select("div.meta"):
            
            nombre = div.find("span", attrs={"class": "title"}).contents[0]
            precio = div.find("span", attrs={"class": "precio"})
            
            if precio is None:
                precio = "?"
            else:
                precio = precio.contents[0]
                
            productos.append((nombre, precio))
            
        return productos
        
    
    def prueba(self):
        print("aaa")