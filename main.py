# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 13:30:54 2020

@author: Sergi, Luis
"""

from webscrapingclass import WebScraping
from urllib.request import urlopen
#from bs4 import BeautifulSoup as bs

#Inicializamos la clase donde que contendrá los métodos necesarios
ws = WebScraping()
#ws.prueba()

def __download_html(url):
    response = urlopen(url)
    html = response.read()
    return html

# Download HTML
url = "https://www.mustang.es/es/"
html = ws.download_html(url)

# Get the names and links of navmenu
# navmenu ---> [[("Hombre", url), ("Zapatos", url)], [("Mujer", url)] ...]
navmenu = ws.get_nav_menu(html)

# Entrar categoría que se quiere hacer scraping
link_scraping = ws.read_category(navmenu)

link_scraping = "https://www.mustang.es/es/mujer/botas/"
html_category = ws.download_html(link_scraping)

#obtener los enlaces de la paginacion de la categoria
enlaces = ws.get_links_pagination(html_category)

productos = ws.get_productos(enlaces[0]) #primera página
#todos_productos = ws.get_productos(enlaces[len(enlaces) - 1]) #ultima página
    