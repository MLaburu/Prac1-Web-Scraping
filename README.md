# Práctica1: Web Scraping
Esta práctica pertenece a la asignatura _Tipología y Ciclo de los Datos_ impartida en el Master _Data Science_ en la _Universitat Oberta de Catalunya (UOC)_. La practica tiene como objetivo familiarizarse con la técnica y uso de _Web Scraping_ a través del lenguaje **Python**. Para ello se ha seleccionado una página web de la cual extraer datos para así formar un _dataset_ a partir de ellos.

Para esta primera práctica, la pagina web que se ha seleccionado ha sido [eltiempo.es](https://www.eltiempo.es), optando concretamente por la predicción en horas y días que se ofrece según una ciudad que se le indica, en este caso, las capitales de provincias españolas.

## Miembros Desarrolladores
La práctica ha sido desarrollada por los alumnos **Mikel Laburu Haro** y **Unai Mateos Corral**.

## Estructura del Repositorio
El repositorio, contiene los diferentes documentos que se han realizado a lo largo de la practica:
* **Readme.md**: Introducción al contenido del repositorio y su estructura.
* **Scraping.py**: Archivo en el que se encuentra el código Python desarrollado para la práctica.
* **SpanishCapitalForecast.csv**: Archivo que contiene el dataset.
* **Info-Dataset.pdf**: Documentación de la práctica desarrollada.

## Requisitos
Para poder hacer uso de la herramienta desarrollada es necesario tener instalado los siguientes softwares:
Python3
```
sudo apt-get install python3.6
sudo apt-get install python3-pip
```
Librerías
```
pip3 install BeautifulSoup
pip3 install requests
pip3 install re
pip3 install csv
pip3 install datetime
```
## Manual de Usuario
Si se desea utilizar este softaware se han de ejecutar las siguientes instrucciones:
```
git clone https://github.com/MLaburu/Prac1-Web-Scraping.git
cd Prac1-web-scraping
python3 scraping.py
```

## Recursos
1. Subirats, L., Calvo, M. (2018). _Web Scraping_. Editorial UOC.
2. Lawson, R. (2015). _Web Scraping with Python_. Packt Publishing Ltd. Chapter 2. Scraping the Data.
