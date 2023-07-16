# WebScraperHotels
Repositorio con la aplicación WebScraperHotels en versiones para Windows y MacOs

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
