# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 13:30:54 2020

@author: Sergi, Luis
"""

from webscrapingclass import WebScrapingMustang

import pandas as pd

#Inicializamos la clase donde que contendrá los métodos necesarios
ws = WebScrapingMustang()

# Download HTML
url = "https://www.mustang.es/es/"
html = ws.download_html(url)

# Get the names and links of navmenu
navmenu = ws.get_nav_menu(html)

def __cleanFile(filename):
    
    #drop the last column    
    df = pd.read_csv(filename + ".csv", nrows=1, sep=";") # read just first line for columns
    columns = df.columns.tolist() # get the columns
    cols_to_use = columns[:len(columns)-1] # drop the last one
    df = pd.read_csv(filename + ".csv", usecols=cols_to_use, sep=";")
    
    #to upper Subcategoria name value
    df['Subcategoria'] = df['Subcategoria'].str.upper()
    
    #replace Subcategoria name value
    df['Subcategoria'] = df['Subcategoria'].replace(['BOTÍN'],'BOTINES')
    df['Subcategoria'] = df['Subcategoria'].replace(['BOTIN'],'BOTINES')
    df['Subcategoria'] = df['Subcategoria'].replace(['BOTA'],'BOTAS')
    df['Subcategoria'] = df['Subcategoria'].replace(['DEPORTIVA'],'DEPORTIVAS')
    df['Subcategoria'] = df['Subcategoria'].replace(['DEPORTIVO'],'DEPORTIVAS')
    df['Subcategoria'] = df['Subcategoria'].replace(['DEPORTIVOS'],'DEPORTIVAS')
    df['Subcategoria'] = df['Subcategoria'].replace(['DPEORTIVA'],'DEPORTIVAS')
    df['Subcategoria'] = df['Subcategoria'].replace(['DEPOTIVA'],'DEPORTIVAS')
    df['Subcategoria'] = df['Subcategoria'].replace(['ZAPATO'],'ZAPATOS')
    
    #delete rows with incorrect values
    df = df[df.Nombre != '?']
    
    nan_value = float("NaN")
    df.replace("", nan_value, inplace=True)
    df.dropna(subset = ["Nombre"], inplace=True)
    
    #df = df['Nombre'].replace('', np.nan, inplace=True)
    #df.dropna(subset = ["Nombre"], inplace=True)
    #df = df.dropna()
    #df = df[df.Nombre != '']
    
    #comprovar información del fichero
    # print (df.head())
    # print(df.Categoria.unique())
    # print(df.Subcategoria.unique())
    # print(df.Color.unique())
    
    df.to_csv(filename + ".csv", sep = ";")
    

def __menu():
    while True:
        print("\n\n--------------Menú-------------------")
        print("Que desea hacer: \n" +
          "- Opción 1: Mostrar los productos de una página en concreto\n" +
          "- Opción 2: Mostrar todos los productos\n" +
          "- Opción 3: Guardar en formato csv la información de todos los productos\n" + 
          "- Opcion 4: Volver a escoger una categoria\n" +
          "- Opción 5: Volver al menu anterior\n" +
          "- Opción 6: Salir\n")
        while True:
            respuesta = int(input("Selecciona una opción: \n"))
            if (0 < respuesta < 7): break
            print("Error! Opción no válida\n")
        print("Cargando petición...")
        if (respuesta == 1):
            if (enlaces):
                while True:
                    respuestaPag = int(input("Introduce una página válida. (Páginas disponibles 1 - " + str(len(enlaces)-1) + ")\n"))
                    if (respuestaPag < len(enlaces) and 0 < respuestaPag): 
                        print("Mostramos los productos de la página: " + str(respuestaPag) + "\n")
                        break
                    print("Error! Página no válida\n")
            else: print("Solo hay disponible una única página\n")
            ws.data = ws.get_productos(enlaces[respuestaPag-1] if enlaces else link_scraping) #primera página
            print(ws.data)
        elif (respuesta == 2):
            ws.data = ws.get_productos(enlaces[len(enlaces) - 1] if enlaces else link_scraping) #última página
            print("Mostramos todos productos\n")
            print(ws.data)
        elif (respuesta == 3):
            if (not ws.data):
                print("Para poder guardar los productos en un csv, primero se deben mostrar usando la opción 1 o 2")
                continue
            filename = input("Por favor introducir nombre del fichero\n")
            ws.data2csv(filename)
            __cleanFile(filename)
        elif (respuesta == 4):
            print("Volver al menu de categoría")
        elif (respuesta == 5):
            return "atras"
        else: # #♥respuesta == 6
            print("Muchas gracias! Hasta la próxima!\n")    
            return "exit"




while True:
    
    print("Que desea hacer: \n" +
      "- Opción 1: Mostrar todos los productos\n" +
      "- Opción 2: Mostrar los productos de categorias\n" +
      "- Opción 3: Salir\n")
    while True:
        respuesta = int(input("Selecciona una opción: \n"))
        if (0 < respuesta < 4): break
        print("Error! Opción no válida\n")
    print("Cargando petición...")
    
    if(respuesta == 1):
        filename = input("Por favor introducir nombre del fichero\n")
        print("Esta opción puede tardar unos minutos")
        productos = ws.getAllProducts(navmenu)
        ws.data2csv(filename)
        __cleanFile(filename)
        print(productos)
        resultado = ""
    elif(respuesta == 2):
        # Entrar categoría que se quiere hacer scraping
        link_scraping = ws.read_category(navmenu)
        
        print("Cargando categoria seleccionada...")
        html_category = ws.download_html(link_scraping)
        
        # Obtener los enlaces de la paginación de la categoria
        enlaces = ws.get_links_pagination(html_category, [])
        
        resultado = __menu()
    else:
        resultado = "exit"
    
    if(resultado == "exit"):
        break;


