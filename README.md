# WebScraperHotels
Repositorio con la aplicación WebScraperHotels en versiones para Windows y MacOs

Este programa está hecho para obtener la información del nombre, dirección, número de teléfono, URL, SSL, rating y precios de los hoteles que el usuario busque haciendo web scarping a la página de Google Hotels.
![image](https://github.com/user-attachments/assets/98a38da5-c9c2-42f0-a9c0-f9655b7920bb)

La aplicación puede buscar a aprtir de una lista de nombres y links o puede hacerlo al hacer una busqeuda con el nombre o usando el link.

* Haciendo búsqueda con el link
![image](https://github.com/user-attachments/assets/1aea7ffc-ce8d-48f7-9eab-768780532c49)

* Haciendo búsqueda con una lista de hoteles y links

![image](https://github.com/user-attachments/assets/6a0a6f71-42d4-4d44-b765-646b657fda95)

Finalmente el usuario selecciona si quiere guardar el archivoe wn csv o en excel.
![image](https://github.com/user-attachments/assets/4e6df020-146d-4f12-9ca1-392999e9f982)

![image](https://github.com/user-attachments/assets/a1ff4360-d7df-4174-b6bd-e7c378e99559)

---

[Descargar archivo comprimido con la aplicación para Windows](https://drive.google.com/file/d/1DI4-eTEVmrAR7AI3Sjul_zvBnvCpzfJk/view?usp=sharing)


[Descargar archivo comprimido con la aplicación para MacOS](https://drive.google.com/file/d/1CpK4pioerCk6DSIT2tFuZiDf4vN3hq5r/view?usp=drive_link)

Para la versión de MacOS en caso de que al intentar abrir el archivo descomprimido salga un aviso como el siguiente haga los siguientes pasos:

<p align="center">
  <img src="https://github.com/AngelDann/WebScraperHotels/assets/135011459/2e13d4e4-7524-43d2-a406-42910598ca07" alt="Texto alternativo" width="300" height="300">
</p>

Asegurese de tener habilitada la opción activada dentro de los ajustes de Seguridad y Privacidad.
<p align="center">
  <img src="https://github.com/AngelDann/WebScraperHotels/assets/135011459/fd64ed94-1d9c-48cb-817a-82f80b848d71" alt="Texto alternativo" width="350" height="300">
</p>

Si la opción no le aparece puede ejecutar el siguiente comando en terminal:

```sudo spctl --master-disable```

Coloque su contraseña de administrador y al volver a entrar al mismo apartado le debe aparecer la opción disponible para elegir.

Si el archivo aparece como archivo de texto únicamente y no como ejecutable abra su terminal y coloque el siguiente comando:

```chmod +x [ruta del archivo]```

Por ejemplo: ```chmod +x /Users/danlo/Documents/WebScraperHotels```
La ruta depernderá de donde tenga el archivo y seguerese re respetar los espacions del comando.

Para colocar la ruta del archivo descomprimido puede abrirlo en Finder y arrastrarlo a la terminal, una vez hecho presione enter y el archivo se tendrá que ver como el siguiente:

![archivo_ruta](https://github.com/AngelDann/WebScraperHotels/assets/135011459/ca7e996a-fb25-4276-a4e7-b67fb6d4331f)

Al final el archivo debe verse como un ejecutable como el siguiente que podrá abrir y usar la aplicación:

<p align="center">
  <img src="https://github.com/AngelDann/WebScraperHotels/assets/135011459/5c6920ce-3984-4528-a1e1-580b53489730" alt="Imagen archivo aplicación" width="350" height="300">
</p>

---

El repositorio también incluye 3 archivos ejemplo para probar el funcionamiento de la inicial de Scrapear por lotes. Esta función permite elegir un archivo que contenga en una columna con los URLs o nombres de los hoteles que se quiere obtener la información. 
Basta con colocar el nombre de la columna y después elegir el archivo para que el programa obtenga la información.

- ejemplo_NOMBRES.csv
- ejemplo_URL.csv
- hoteles.csv
