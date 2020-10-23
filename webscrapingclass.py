# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 19:00:51 2020

@author: Sergi, Luís
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

import sys

class WebScraping():
    
    data = []
    
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
        print("Escoger categoria: \n")
        i = 0
        cat = []
        for idx1, categories in enumerate(navmenu):
            for idx2, item_category in enumerate(categories):    
                print(str(i) + ": " + item_category[0])
                cat.append(item_category)
                i+=1
            print("--------")
        while True:
            respuesta = int(input("Introduzca el número de la categoría: \n"))
            if (respuesta >= 0 and respuesta < len(cat)): break
            print("Error! Categoría no vàlida\n")
        print("Se ha seleccionado la categoria: " + cat[respuesta][0] + "\n")
        return cat[respuesta][1]
        
        
    def get_links_pagination(self, html, enlaces):
        content = bs(html, 'html.parser')
        
        enlaces_paginas = content.find('div', attrs={'class':'pagination'})
        enlace_active = enlaces_paginas.find('a', attrs={'class':'active'})
        
        if enlace_active is None: #si no hay paginación return []
            return []
        else:
            enlaces.append(enlace_active.get("href")) 
            
            nextLink = enlace_active.find_next("a")
            
            print(nextLink)
            
            if("T" in nextLink.text): #si es la pagina Todo
                enlaces.append(nextLink.get("href"))
                return enlaces
            else:
                nextLink = self.download_html(nextLink.get("href"))
                self.get_links_pagination(nextLink, enlaces)

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
                
            productos.append((str(nombre), str(precio)))
        
        self.data = productos
        
        return productos
    
    
    def data2csv(self, filename):
        
        self.data = [("Producto", "Precio")] + self.data
        
        file = open("./" + filename + ".csv", "w+")
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                file.write(self.data[i][j] + ";")
            file.write("\n")