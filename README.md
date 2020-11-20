# Coches.com WEB SCRAPING

_En este proyecto vamos a realizar un web scraping en la web: coches.com consiguiendo un archivo 
.csv final con los datos de los coches disponibles en la web (de km0 y segunda mano)_

https://www.coches.com/

## Comenzando 🚀

Lo primero que hemos hecho es analizar la web, encontrando las etiquetas HTML necesarias para llegar a las páginas
de interés. Nosotros accederemos a los datos de los coches de km0 y de segunda mano, accesibles mediante una barra
superior. Dentro de cada tipo, encontraremos las diferentes marcas de los coches y yendo a cada marca podremos encontrar
las listas d elos coches divididas en muchas páginas.

### Estructura del código

Lo primero a mencionar es que hemos optado por usar la libreria selenium la cual nos ha facilitado mucho la exploración
de las páginas web al ser dinámicas.

Tenemos una función _write_data_ para escribir los datos recolectados en un archivo _csv_.

Una clase _Car_ la cual usamos para almacenar los datos de cada coche creando un objeto de esta clase. Además,
incluimos una función para transformar la clase en un diccionario que se utilizará para introducir los datos  en el -csv.

Por último, y mas importante. La clase CarsScrapper, la cual incluye todas las funciones necesarias para realizar el web
de la pagina web. Se incluye una función _din_scraper_ que abrirá los distintos navegadores y se encargará de cerrar
un pop_up de cookies que no nos dejaba continuar adecuadamente (arreglar esto ha sido uno de las cosas que más tiempo 
nos ha tomado). Otra función importante es _get_links_, la cual encuentra los links de la página de coches de km0 y de
segunda mano. La salida de esta función se la daremos a la función _brand_links_ la cual encontrará, dentro de cada link, 
los links para las distintas marcas (36) para cada página (km0 o segunda mano).

La función _get_all_navigation_ es una de las más elavoradas, con ella hemos conseguido guardar los datos de cada coche
de los distintos tipos (km0 y segunda mano) y marca. Se han recorrido las distintas páginas mediante _clicks dinamicos_
evitando así cerrar y abrir nevagores constantemente y ahorrando mucho tiempo y recursos.

Finalmente, comentar que hemos usado parallelismo para acelerar el proceso. Usamos 4 procesadores al mismo tiempo lo que
se traduce en 4 navegadores distintos ejecutandose a la vez.

El resultado final ha dado en más de 100 mil coches almacenados en el archivo csv. Y el tiempo transcurrido en este proceso 
con estas configuraciones fue de aproximadamente 5 horas.

## DOI del data set: 10.5281/zenodo.4247442


## Construido con PyCharm 🛠️

## Integrantes 

Reynel López Lantigua [/rllantigua](https://github.com/rllantigua)

Jaime Gimeno Ferrer   [/jaimegf98](https://github.com/JaimeGimeno)
   
## Estructura del repositorio 

/csv : Contiene el _data set_ obtenido de la ejecución de la herramienta.

/drivers : Contiene el _chromedriver.exe_ , herramienta utilizada para lanzar una instancia del navegador (_Google Chrome_), tarea necesaria para realizar el scraping de esta página de contenido dinámico.
 
/pdf : Contiene el archivo con la respuesta a las cuestiones planteadas en la práctica.

/src : Contiene el código fuente de la herramienta.


## Bibliografía 
1. Lawson, R. (2015). Web Scraping with Python. Packt Publishing Ltd. Chapter 2. Scraping the Data.

2. Subirats, L., Calvo, M. (2018). Web Scraping. Editorial UOC. 

3. Selenium Web Driver Documentation. [https://www.selenium.dev/documentation/en/](https://www.selenium.dev/documentation/en/)
