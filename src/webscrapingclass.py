# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 19:00:51 2020

@author: Sergi, Luís
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import codecs

class WebScrapingMustang():
    
    data = []
    header = [("Nombre", "Categoria", "Subcategoria", "Color", "Precio", "Venta", "Tallas", "Referencia", "Otros")]
    categoria = []
    
    def __get_nav_names(self,nav):
        categorias = []
        for idx, ultag in enumerate(nav.find_all('li')):
            if len(ultag.find_all("li")) > 0:
                itemCategoria = []
                categoriaPadre = ultag.find("a")
                itemCategoria.append((categoriaPadre.text, None, categoriaPadre.get("href")))
                for idx2, categoriaHijo in enumerate(ultag.find_all("li")):
                    itemCategoria.append((categoriaPadre.text, categoriaHijo.text, categoriaHijo.find("a").get("href")))
                categorias.append(itemCategoria)
        categorias.pop(); #Quitado último elemento debido a que són url que no tienen productos
        return categorias
    
    def download_html(self, url):
        response = urlopen(url)
        html = response.read()
        return html
    
    def get_nav_menu(self, html):
        content = bs(html, 'html.parser')
        nav_menu = content.find("nav", attrs={"class": "menu dark hero menuhead"})
        menu_todo = nav_menu.find("div", attrs={"class": "middle"})
        
        categorias = self.__get_nav_names(menu_todo)
        return categorias
    
    def read_category(self, navmenu):
        print("Escoger categoria: \n")
        i = 0
        cat = []
        for idx1, categories in enumerate(navmenu):
            for idx2, item_category in enumerate(categories):
                if (item_category[1]):
                    print(str(i) + ": " + item_category[1])
                else: 
                    print(str(i) + ": " + item_category[0])
                cat.append(item_category)
                i+=1
            print("--------")
        while True:
            respuesta = int(input("Introduzca el número de la categoría: \n"))
            if (respuesta >= 0 and respuesta < len(cat)): break
            print("Error! Categoría no válida\n")
        print("Se ha seleccionado la categoria: " + cat[respuesta][0])
        if (cat[respuesta][1]): print("Concretamente la subcategoria: " + cat[respuesta][1] + "\n")
        self.categoria = cat[respuesta]
        return cat[respuesta][2]
        
        
    def get_links_pagination(self, html, enlaces):
        content = bs(html, 'html.parser')
        
        enlaces_paginas = content.find('div', attrs={'class':'pagination'})
        enlace_active = enlaces_paginas.find('a', attrs={'class':'active'})
        
        if enlace_active is None: #si no hay paginación return []
            return []
        else:
            enlaces.append(enlace_active.get("href")) 
            nextLink = enlace_active.find_next("a")
            
            if("T" in nextLink.text): #si es la pagina Todo
                enlaces.append(nextLink.get("href"))
                return enlaces
            else:
                nextLink = self.download_html(nextLink.get("href"))
                self.get_links_pagination(nextLink, enlaces)

            return enlaces
    
    def __get_links_products(self, html, enlaces):
        
        html = self.download_html(html)
        content = bs(html, 'html.parser')
        
        for a in content.select("a.tag_productImpression"):
            enlaces.append(a.get("href"))
        
        return enlaces
    
    def __getInfoProduct(self, html):
        
        html = self.download_html(html)
        content = bs(html, 'html.parser')
        
        catPadre = self.categoria[0]
        
        titulo_div = content.find('div', attrs={'class':'titulo'}).findChildren("h1")[0].text.strip()
        titulo_div = titulo_div.split()
            
        catHijo = titulo_div[0]
        
        nombre = titulo_div[1:len(titulo_div) - 1]
        nombre = ' '.join(nombre)
        
        color = titulo_div[len(titulo_div) - 1] if len(titulo_div) > 2 else "?"
            
        try:
            precio = content.find('div', attrs={'class':'precio'}).findChildren("ins")[0].text.strip()
        except:
            precio = "?"
            nombre = "?"
        
        caract_div = content.find('div', attrs={'id':'caracteristica'}).findChildren("ul")
        caracteriticas = ""
        for ul in caract_div:
            for li in ul.findAll("li"):
                listCaract = li.findChildren("span")
                info_name = listCaract[0].text.strip()
                info_value = listCaract[1].text.strip()
                value = info_name + info_value
                caracteriticas = caracteriticas +  value + "$"
        caracteriticas = caracteriticas[:-1]
        
        ref_div = content.find('div', attrs={'class':'titulo'}).find("p").contents[0].strip()
        ref_div = ref_div.split()
        referencia = ref_div[1]
        
        venta = ""
        
        tallas_div = content.find('div', attrs={'class':'tdtallas'})
        tallas = ""
        if(tallas_div is None):
            venta = "No"
            tallas = "?"
        else:
            venta = "Si"
            tallas_div = tallas_div.findChildren("button")
            for buttonTalla in tallas_div:
                tallas = tallas + buttonTalla.text.strip() + "-"
            
            tallas = tallas[:-1]
        
        return (nombre, catPadre, catHijo, color, precio, venta, tallas, referencia, caracteriticas)
        
    def get_productos(self, html):
        
        enlacesProductos = self.__get_links_products(html, [])
        
        productos = []
        for enlace in enlacesProductos:
            productos.append(self.__getInfoProduct(enlace)) 
            
        #self.data = productos
        
        return productos
    
    def getAllProducts(self, navmenu):
        
        linksCategoriaPadre = []
        self.data = []
        self.categoria = [""]
        listcategorias = []
        
        for categories in navmenu:
            listcategorias.append(categories[0][0]) #se guarda todas las categorias
            linksCategoriaPadre.append(categories[0][2])
        
        linksCategoriaPadre.pop()
        
        for i, link in enumerate(linksCategoriaPadre):
            html_category = self.download_html(link)
            enlaces = self.get_links_pagination(html_category, [])
            self.categoria[0] = listcategorias[i]
            todos_productos_categ = self.get_productos(enlaces[len(enlaces) - 1] if enlaces else link) #última página
            self.data = self.data + todos_productos_categ
        
        return self.data
        
    def data2csv(self, filename):
        self.data = self.header + self.data
        
        file = codecs.open("./" + filename + ".csv", "w+", "utf-8")
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                file.write(self.data[i][j] + ";")
            file.write("\n")