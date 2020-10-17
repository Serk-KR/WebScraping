# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 13:30:54 2020

@author: Sergi, Luis
"""

from webscrapingclass import WebScraping
#from bs4 import BeautifulSoup as bs

#Inicializamos la clase donde que contendrá los métodos necesarios
ws = WebScraping()
ws.prueba()

def download_html(url):
    response = urlopen(url)
    html = response.read()
    return html

# Download HTML
url = "https://www.mustang.es/es/"
html = ws.download_html(url)
#beautsoup = bs(html, 'html.parser')

# Get the names and links of navmenu
navmenu_links = ws.get_nav_menu(html)