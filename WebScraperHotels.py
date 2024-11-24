#Librerías
import requests
import re
import ssl
import socket
from urllib.parse import urlparse
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import uuid
import os
from tabulate import tabulate
import sys
import validators
import tkinter as tk
from tkinter import filedialog
import jellyfish


def es_url(cadena):
    if validators.url(cadena):
        return True
    else:
        return False

def obtener_hoteles(hotel):
    hotel = hotel.replace(' ','%25')
    url = 'https://www.google.com/travel/search?q=' + hotel + "&ved=0CAAQ5JsGahcKEwiYo5a-2tn_AhUAAAAAHQAAAAAQCw"
    # Realizar la solicitud HTTP
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Obtener el contenido HTML de la respuesta
        html = response.text

        return html
    except requests.exceptions.ConnectionError:
        imprimir_recuadro("Ocurrió un error. Revise su conexión a Internet.")
        main()
    

def obtener_html_enlace(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Obtener el contenido HTML de la respuesta
        html = response.text

        return html
    except requests.exceptions.ConnectionError:
        imprimir_recuadro("Ocurrió un error. Revise su conexión a Internet.")
        main()

    # Obtener el contenido HTML de la respuesta
    html = response.text

    return html

#Funciones auxiliares

def imprimir_recuadro(mensaje):
    longitud = len(mensaje)

    print("╔" + "═" * (longitud + 2) + "╗")
    print("║ " + mensaje + " ║")
    print("╚" + "═" * (longitud + 2) + "╝")

#Evita los precios que no siguen la misma estructura
def estandarizar_lista(lista):
    lista_estandarizada = []

    for elemento in lista:
        precio, proveedor = elemento

        # Eliminar caracteres no deseados y estandarizar el formato
        precio = precio.replace('MX$', '').replace('MXN', '').replace('\xa0', '').replace('.', '').strip()
        precio = int(precio.replace(',', ''))  # Convertir a entero

        lista_estandarizada.append((precio, proveedor))
    return lista_estandarizada

def verificar_certificado_ssl(url):
    # Obtener el dominio y el puerto del URL
    dominio, puerto = obtener_dominio_puerto(url)
    
    # Establecer una conexión segura SSL
    contexto = ssl.create_default_context()
    with socket.create_connection((dominio, puerto)) as sock:
        with contexto.wrap_socket(sock, server_hostname=dominio) as ssock:
            # Verificar si se estableció una conexión segura SSL
            certificado = ssock.getpeercert()
            if certificado:
                return True
            else:
                return False

def obtener_dominio_puerto(url):
    parsed_url = urlparse(url)
    dominio = parsed_url.hostname
    puerto = parsed_url.port if parsed_url.port else 443
    return dominio, puerto

#Reconoce si el url es de google maps
def es_url_google_maps(url):
    patron = r"(?:https?:\/\/)?(?:www\.)?maps\.google\.com\/maps\/?[^\s]+"
    es_google_maps = re.match(patron, url)
    return es_google_maps is not None


#Identifica si es una url
def es_url(cadena):
    try:
        resultado = urlparse(cadena)
        return all([resultado.scheme, resultado.netloc])
    except ValueError:
        return False
    
#Funciones de scraping
def scrap_nombre(soup):
    try:
        nombre_hotel = soup.find('h1', class_='QORQHb fZscne')
        nombre_hotel = nombre_hotel.text
    except:
        nombre_hotel = np.nan
    
    return nombre_hotel

def scrap_direccion_numero(soup):
    direccion_numero = soup.find('div', class_='K4nuhf')
    
    if direccion_numero is None:
        direccion = np.nan
        numero = np.nan
    else:
        try:
            direccion = direccion_numero.find_all('span')[0].text
        except IndexError:
            direccion = np.nan
        
        try:
            numero = direccion_numero.find_all('span')[2].text
        except IndexError:
            numero = np.nan
    
    return direccion, numero
    
def scrap_rating(soup):
    try:
        rating = soup.find('div', class_='iDqPh BgYkof')
        rating = float(rating.text)
    except:
        rating = np.nan
        
    return rating

def scrap_precios(soup):
    
    # Buscar los elementos <div> con la clase "CcERhd hGTXTe"
    divs = soup.find_all('div', class_='zIL9xf xIAdxb')
    
    resultados = []
        
    #Buscar si tiene precio de sitio oficial
    try:
        nombre_oficial = soup.find('span', class_='FjC1We ogfYpf zUyrwb uhWwJd')
        precio_oficial = soup.find('span', class_='MW1oTb')
        resultados.append((precio_oficial.get_text(), nombre_oficial.get_text()))
        precio_normalizado = precio_oficial.get_text().replace('MX$', '').replace('MXN', '').replace('\xa0', '').replace('.', '').strip()
        precio_normalizado = int(precio_normalizado.replace(',', ''))  # Convertir a entero
        sitio_oficial = (precio_normalizado, nombre_oficial.get_text())
    except:
        sitio_oficial = np.nan
    
    # Iterar sobre los elementos <div> encontrados
    for div in divs:
        # Buscar los elementos <span> con la clase "MW1oTb" dentro de cada <div>
        #FjC1We ogfYpf zUyrwb uhWwJd
        #FjC1We ogfYpf zUyrwb
        
        precios = div.find_all('span', class_='MW1oTb')
        empresas = div.find_all('span', class_='FjC1We ogfYpf zUyrwb')
        
        min_length = min(len(empresas), len(precios))
        # Obtener el texto dentro de cada <span> encontrado
        for i in range(min_length):
            resultados.append((precios[i].get_text(), empresas[i].get_text()))
    
    #Hacer los precios en un unico formato
    resultados = estandarizar_lista(resultados)
    
    #Eliminar lista de elementos repetidos
    resultados = list(set(resultados))
    
    return resultados, sitio_oficial
    
def scrap_sitioWeb(soup):
    sitioWeb = soup.find_all('a', class_='WpHeLc VfPpkd-mRLv6 VfPpkd-RLmnJb')[:2]
    
    if len(sitioWeb) > 0:
        if es_url_google_maps(sitioWeb[0].get('href')):
            href = np.nan
            google_maps_url = sitioWeb[0].get('href')
        
        elif es_url_google_maps(sitioWeb[1].get('href')):
            href = sitioWeb[0].get('href')
            google_maps_url = sitioWeb[1].get('href')
        else:
            href = sitioWeb[0].get('href')
            google_maps_url = np.nan
    else:
        href = np.nan
        google_maps_url = np.nan
        
    try:
        if verificar_certificado_ssl(href):
            ssl = 'True'
        else:
            ssl = 'False'
    except:
        ssl = np.nan

    return href, ssl, google_maps_url

def buscar_contenido(html):
    # Analizar el contenido HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Buscar los contenedores específicos
    contenedores = soup.find_all('a', {'class': 'PVOOXe'})

    return contenedores[:10]  # Retorna los primeros diez contenedores encontrados

def buscar_entity(a_tag):
    
    if a_tag and 'href' in a_tag.attrs:
        href = 'https://www.google.com' + a_tag['href']
        #print(href)
        return(href)
    else:
        print("No se encontró el atributo href en el elemento <a>.")

def scrap_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    nombre_hotel = scrap_nombre(soup)
    
    direccion,numero = scrap_direccion_numero(soup)
    
    url,ssl,google_maps_url = scrap_sitioWeb(soup)
    
    rating = scrap_rating(soup)
    
    precios, sitio_oficial = scrap_precios(soup)
    
    return nombre_hotel, direccion, numero, url, ssl, google_maps_url, rating, precios,sitio_oficial


#Funcion para guardar informacion

def guardar_variables_en_dataframe(nombre_hotel, direccion, numero, url, ssl, google_maps_url, rating, precios, sitio_oficial):
    data = {'id': str(uuid.uuid4()),
            'Fecha':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Nombre Hotel': [nombre_hotel],
            'Direccion': [direccion],
            'Google Maps': [google_maps_url],
            'Numero': [numero],
            'URL': [url],
            'SSL': [ssl],
            'Rating': [rating],
            'Precio web official':[sitio_oficial],
            'Precios(MXN)': [precios]}
    
    df = pd.DataFrame(data)
    return df

def crear_dataframe_vacio():
    data = {'id': [],
            'Fecha': [],
            'Nombre Hotel': [],
            'Direccion': [],
            'Google Maps': [],
            'Numero': [],
            'URL': [],
            'SSL': [],
            'Rating': [],
            'Precio web oficial': [],
            'Precios(MXN)': []}
    
    df = pd.DataFrame(data)
    return df

def actualizar_dataframe(df, nombre_hotel, direccion, numero, url, ssl, google_maps_url, rating, precios, sitio_oficial):
    # Ordenar las tuplas en base al precio
    precios_ordenados = sorted(precios, key=lambda tup: tup[0])

    nueva_fila = {'id': [str(uuid.uuid4())],
                  'Fecha': [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                  'Nombre Hotel': [nombre_hotel],
                  'Direccion': [direccion],
                  'Google Maps': [google_maps_url],
                  'Numero': [numero],
                  'URL': [url],
                  'SSL': [ssl],
                  'Rating': [rating],
                  'Precio web oficial': [sitio_oficial],
                  'Precios(MXN)': [precios_ordenados]}
    
    df = pd.concat([df, pd.DataFrame(nueva_fila)], ignore_index=True)
    return df

def guardar_en_csv(df, nombre_archivo):
    # Obtener la ruta de la carpeta actual
    ruta_actual = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta completa de la carpeta "datos"
    ruta_datos = os.path.join(ruta_actual, 'datos')

    # Asegurarse de que la carpeta "datos" exista, si no, crearla
    if not os.path.exists(ruta_datos):
        os.makedirs(ruta_datos)

    # Construir la ruta completa del archivo CSV en la carpeta "datos"
    ruta_archivo = os.path.join(ruta_datos, nombre_archivo)

    nombre_archivo = nombre_archivo.lower()  # Normalizar entrada a minúsculas
    try:
        if os.path.isfile(ruta_archivo):
            opciones = ["Si", "No", "Salir"]
            imprimir_opciones_recuadro(opciones)
            respuesta = input("Ya existe un archivo con el mismo nombre. ¿Desea reemplazarlo? ")
            respuesta = normalizar_entrada(respuesta)

            if (respuesta == "1"):
                df.to_csv(ruta_archivo, index=False)
                print("Archivo CSV reemplazado exitosamente.")

            elif (respuesta == "2"):
                opcion_dataframe_opcion4(df)
                
            elif (respuesta == "3"):
                opcion_dataframe(df)

            else:
                print("\nNo ha seleccionado ninguna de las opciones\n")
                guardar_en_csv(df, nombre_archivo)
        else:
            df.to_csv(ruta_archivo, index=False)
            print("Archivo CSV guardado exitosamente en ",ruta_archivo)
    except:
        print("El nombre de archivo no es válido, asegúrese de que no contenga caracteres inválidos")
        nuevo_nombre = input("Ingrese un nuevo nombre de archivo: ")
        nuevo_nombre = nuevo_nombre + ".csv"
        guardar_en_csv(df, nuevo_nombre)

def agregar_a_csv(nuevos_datos, nombre_archivo):
    # Obtener la ruta de la carpeta actual
    ruta_actual = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta completa de la carpeta "datos"
    ruta_datos = os.path.join(ruta_actual, 'datos')

    # Asegurarse de que la carpeta "datos" exista, si no, crearla
    if not os.path.exists(ruta_datos):
        os.makedirs(ruta_datos)

    # Construir la ruta completa del archivo CSV en la carpeta "datos"
    ruta_archivo = os.path.join(ruta_datos, nombre_archivo)

    try:
        # Intentar leer el archivo CSV existente
        existing_df = pd.read_csv(ruta_archivo)
        df_final = pd.concat([existing_df, nuevos_datos], ignore_index=True)
    except FileNotFoundError:
        # Si el archivo no existe, utilizar los nuevos datos directamente
        df_final = nuevos_datos
    
    # Guardar el DataFrame en el archivo CSV
    df_final.to_csv(ruta_archivo, index=False)
    print("Datos agregados al archivo CSV exitosamente.")

#Opciones de usuario
def opcion1(df):
    entrada = input("Escriba el nombre del hotel o coloque el link: ")
    imprimir_recuadro("NOTA: Asegurese de seleccionar el hotel al momento de colocar el link para obtener la informacion correctamente")

    if es_url(entrada):
        html =  obtener_html_enlace(entrada)
    else:
        contenedores_encontrados = buscar_contenido(obtener_hoteles(entrada))

        if contenedores_encontrados:
            print("Resultados encontrados: ")
            data = []
            i = 1
            for contenedor in contenedores_encontrados:
                nombre_hotel = contenedor.get('aria-label')
                data.append([i, nombre_hotel])
                i += 1
            headers = ["Número de hotel", "Nombre"]
            print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

        else:
            print("No se encontraron resultados en la página.")
            opcion1()

        seleccion = input("Seleccione el numero de un hotel: ")
        seleccion = normalizar_entrada(seleccion)

        while True:
            try:
                seleccion = int(seleccion)
                if seleccion > 0 and seleccion <= len(contenedores_encontrados):
                    break
                else:
                    print("\nAsegúrese de que su respuesta sea el número de una opción.\n")
                    seleccion = input("Seleccione el numero de un hotel: ")
            except ValueError:
                print("\nAsegúrese de que su respuesta sea el número de una opción.\n")
                seleccion = input("Seleccione el numero de un hotel: ")
                seleccion = normalizar_entrada(seleccion)

        hotel_selec = contenedores_encontrados[seleccion-1]
        buscar_entity(hotel_selec)

        html = obtener_html_enlace(buscar_entity(hotel_selec))

    nombre_hotel, direccion, numero, url, ssl, google_maps_url, rating, precios, sitio_oficial = scrap_info(html)

    df_impresion = guardar_variables_en_dataframe(nombre_hotel, direccion, numero, url, ssl, google_maps_url, rating, precios, sitio_oficial)
    
    # Ajustar la configuración de visualización
    imprimir_dataframe(df_impresion)

    agregar_cola(df,nombre_hotel, direccion, numero, url, ssl, google_maps_url, rating, precios, sitio_oficial)
    
    opcion_dataframe(df)

def opcion2():
    print()
    imprimir_recuadro("Nombre del programa")
    print("Web Scraper Google Hotels")
    imprimir_recuadro("Descripción del programa")
    print("Este programa está hecho para obtener la información del nombre, dirección, número de teléfono, URL, SSL, rating y precios de los hoteles que el usuario busque haciendo web scarping a la página de Google Hotels.")

    imprimir_recuadro("Creador")
    print("ANGEL DANIEL LOPEZ ALVAREZ")
                
    imprimir_recuadro("Información de contacto")
    print("agdaniel019@gmail.com")
    print("200300611@ucaribe.edu.mx")
    print()

def agregar_cola(df,nombre_hotel, direccion, numero, url, ssl, google_maps_url, rating, precios, sitio_oficial):
    opciones = ["Sí", "No"]
    imprimir_opciones_recuadro(opciones)


    opcion = input("¿Desea agregarlo a la cola? Escriba el numero la opcion que desee hacer: ")
    opcion = normalizar_entrada(opcion)

    if (opcion == "1"):
        df = actualizar_dataframe(df,nombre_hotel, direccion, numero, url, ssl, google_maps_url, rating, precios, sitio_oficial)
        opcion_dataframe(df)

    elif(opcion == "2"):
        opcion_dataframe(df)
        
    else:
        print("\nNo ha seleccionado ninguna de las opciones\n")
        agregar_cola(df)

def eliminar_hotel_cola(df):
    
    mostrar_cola(df)
    id_eliminar = input("Escriba el id del hotel (o 'cancelar' para abortar): ")
    id_eliminar = normalizar_entrada(id_eliminar)
        
    if id_eliminar.lower() == "cancelar":
        opcion_dataframe(df)
    else:
        indices = df.index[df['id'] == id_eliminar].tolist()

        if indices:
            # Eliminar la fila con el ID encontrado
            df = df.drop(indices)     
            print("\nLa fila se ha eliminado correctamente.\n")
            opcion_dataframe(df)
        else:
            print("\nEl ID no se encuentra dentro de la cola.\n")
            eliminar_hotel_cola(df)
        return df

def mostrar_cola(df):
    headers = ["ID", "Nombre Hotel", "Fecha"]
    data = df[["id", "Nombre Hotel", "Fecha"]].values.tolist()
    print(tabulate(data, headers, tablefmt="grid"))

def opcion_dataframe_opcion4(df):
    nombre_archivo = input("Escriba el nombre del archivo (o 'cancelar' para abortar): ")
        
    if nombre_archivo.lower() == "cancelar":
        opcion_dataframe(df)
    else:
        nombre_archivo = nombre_archivo + ".csv"
        guardar_en_csv(df, nombre_archivo)

def opcion_dataframe(df):

    opciones = ["Agregar otro hotel","Eliminar hotel de la cola","Mostrar cola", "Guardar archivo CSV", "Actualizar CSV", "Salir"]
    imprimir_opciones_recuadro(opciones)


    opcion = input("Escriba el numero la opcion que desee hacer: ")
    opcion = normalizar_entrada(opcion)

    if(opcion == "1"):
        opcion1(df)

    elif(opcion == "2"):
        df = eliminar_hotel_cola(df)
        opcion_dataframe(df)

    elif (opcion == "3"):
        mostrar_cola(df)
        opcion_dataframe(df)
        
    elif (opcion == "4"):
        opcion_dataframe_opcion4(df)
        
    elif (opcion == "5"):
        carpeta_actual = os.path.dirname(os.path.abspath(__file__))
        # Construir la ruta de la carpeta "datos"
        ruta_datos = os.path.join(carpeta_actual, 'datos')
        # Buscar archivos CSV en la carpeta "datos"
        archivos_csv = [archivo for archivo in os.listdir(ruta_datos) if archivo.endswith('.csv')]
        # Imprimir los nombres de los archivos CSV numerados
        # Crear una lista de opciones con los nombres de los archivos CSV
        opciones = []
        for i, archivo in enumerate(archivos_csv, 1):
            opciones.append([i, archivo])

        # Agregar opción de salir
        num_opcion_salir = len(archivos_csv) + 1
        opciones.append([num_opcion_salir, "Salir"])

        # Imprimir la tabla de opciones
        print(tabulate(opciones, headers=["Opción", "Archivo"], tablefmt="fancy_grid"))

        # Validar la selección del usuario
        seleccion = input("Seleccione un archivo (ingrese el número): ") 
        seleccion = normalizar_entrada(seleccion)
        while not seleccion.isdigit() or int(seleccion) < 1 or int(seleccion) > len(archivos_csv) + 1:
            print("Selección inválida. Por favor, ingrese un número válido.")
            seleccion = input("Seleccione un archivo (ingrese el número): ")
            seleccion = normalizar_entrada(seleccion)
            
        if int(seleccion) == len(archivos_csv) + 1:
            opcion_dataframe(df)
        else:
            # Obtener el nombre del archivo seleccionado
            indice_seleccionado = int(seleccion) - 1
            nombre_archivo = archivos_csv[indice_seleccionado]
            agregar_a_csv(df, nombre_archivo)
                
    elif (opcion == "6"):
        # Código para agregar otro hotel
        main()

    else:
        print("\nNo ha seleccionado ninguna de las opciones\n")
        opcion_dataframe(df)

def imprimir_dataframe(df):
    for column in df.columns:
        column_name = " {} ".format(column)  # Nombre de la columna con espacios en ambos lados
        print("┌" + "─" * len(column_name) + "┐")  # Línea superior del cuadrado
        print("│" + column_name + "│")  # Nombre de la columna dentro del cuadrado
        print("└" + "─" * len(column_name) + "┘")  # Línea inferior del cuadrado
        if column == 'Precios(MXN)':
            data = []
            headers = ["Precio", "Empresa"]
            for lista_precios in df['Precios(MXN)']:
                for precio,empresa in lista_precios:
                    data.append([precio,empresa])
            data_ordenada = sorted(data, key=lambda x: x[0])
            print(tabulate(data_ordenada, headers=headers, tablefmt="fancy_grid"))

        else:    
            for value in df[column]:
                print(value)
        print()


def imprimir_opciones_recuadro(opciones):
    ancho_recuadro = max(len(opcion) for opcion in opciones) + 7  # 7 caracteres adicionales para los bordes y números
    numero_opcion = 1

    print("╔" + "═" * ancho_recuadro + "╗")
    print("║" + " MENU".center(ancho_recuadro) + "║")
    print("╠" + "═" * ancho_recuadro + "╣")
    for opcion in opciones:
        print("║ {} | {} ║".format(str(numero_opcion).rjust(2), opcion.ljust(ancho_recuadro - 7)))
        numero_opcion += 1
    print("╚" + "═" * ancho_recuadro + "╝")

def normalizar_entrada(entrada):
    entrada = entrada.replace(" ","")
    return entrada

def abrir_archivo_csv(columna):
    # Crear la ventana principal
    ventana_principal = tk.Tk()

    # Ocultar la ventana principal
    ventana_principal.withdraw()

    # Abrir el explorador de archivos y obtener la ruta del archivo seleccionado
    archivo_csv = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])

    # Leer el archivo CSV y crear un DataFrame de pandas
    dataframe = pd.read_csv(archivo_csv, usecols=[columna],encoding='latin-1')

    # Mostrar el archivo seleccionado
    print("Archivo seleccionado:", archivo_csv)

    # Retornar el DataFrame
    return dataframe

def scrap_lote_url(df,hotel):
    
    return df




def scrap(df):
    try:
        print("\nA tomar en cuenta al usar esta opción:")
        print("\t1. Asegúrese de que el archivo se encuentre en formato .csv")
        print("\t2. Escriba el nombre de la columna donde está la información tal cual el documento, puede ser un URL o nombre")
        print("\t3. Si es URL, que haya seleccionado el hotel y copiado el URL correctamente de Google Hotels")
        print("\t4. Si es nombre de hotel: \n\t-Que el nombre se parezca lo más posible al que tenga en Google Hotels. \n\t-El algoritmo compara el nombre al resultado que más se parezca, por lo que puede obtenerse un hotel diferente.")

        input("\nColoque el nombre de que contenga la información y luego se abrirá el explorador de archivos (presione Enter para continuar)")
        nombre_columna = input("Escriba el nombre de la columna donde se encuentran los URL de hotel: ")
        df_scrap = abrir_archivo_csv(nombre_columna)

        for hotel in df_scrap[nombre_columna].values:
            if(es_url(hotel)):
                print("Esurl")
                print("Scraping hotel: ", hotel,"...")
                html =  obtener_html_enlace(hotel)
                nombre_hotel, direccion, numero, url, ssl, google_maps_url, rating, precios, sitio_oficial = scrap_info(html)
                df = actualizar_dataframe(df, nombre_hotel, direccion, numero, url, ssl, google_maps_url, rating, precios, sitio_oficial)
                
            else:
                nombres = []
                print("Scraping hotel: ", hotel,"...")
                contenedores_encontrados = buscar_contenido(obtener_hoteles(hotel))
                if contenedores_encontrados:
                    for contenedor in contenedores_encontrados:
                        nombre_hotel = contenedor.get('aria-label')
                        nombres.append(nombre_hotel)
                else:
                    next
                hotel_selec = contenedores_encontrados[encontrar_indice_similar(hotel, nombres)]
                html = obtener_html_enlace(buscar_entity(hotel_selec))
                nombre_hotel, direccion, numero, url, ssl, google_maps_url, rating, precios, sitio_oficial = scrap_info(html)
                df = actualizar_dataframe(df, nombre_hotel, direccion, numero, url, ssl, google_maps_url, rating, precios, sitio_oficial)
        opcion_dataframe(df)
    except Exception as e:
        print("Se produjo un error: ",str(e))
        

def encontrar_indice_similar(nombre_hotel, opciones):
    mejor_similitud = 0
    indice_similar = -1

    for i, opcion in enumerate(opciones):
        similitud = jellyfish.jaro_winkler(nombre_hotel, opcion)
        if similitud > mejor_similitud:
            mejor_similitud = similitud
            indice_similar = i

    return indice_similar  

def main():
    try:    
        while(True):
            opciones = ["Buscar hotel", "Información", "Scrapear lote" ,"Salir",]
            imprimir_opciones_recuadro(opciones)

            opcion = input("Escriba el numero la opcion que desee hacer: ")
            opcion = normalizar_entrada(opcion)

            if (opcion == "4"):
                print("\n¿Esta seguro que desea salir de la aplicacion?\n")
                opciones = ["Si", "No"]
                imprimir_opciones_recuadro(opciones)
                pregunta = input("Escriba el numero la opcion que desee hacer:")
                pregunta = normalizar_entrada(pregunta)

                if (pregunta == "1"):
                    sys.exit()

                elif(pregunta == "2"):
                    main()

                else:
                    print("\nNo ha seleccionado ninguna de las opciones\n")
            
            elif(opcion == "1"):
                df = crear_dataframe_vacio()
                opcion1(df)

            elif(opcion == "2"):
                opcion2()

            elif(opcion == "3"):
                df = crear_dataframe_vacio()
                scrap(df)

            else:
                print("\nNo ha seleccionado ninguna de las opciones\n")
    except Exception as e:
        print("Se produjo un error: ",str(e))
        main()  # Regresar a la función main

main()