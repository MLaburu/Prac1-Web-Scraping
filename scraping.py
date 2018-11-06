from bs4 import BeautifulSoup
from registro import Registro
import requests
import csv
import re
# Here, we're just importing both Beautiful Soup and the Requests library

page_link = 'https://www.eltiempo.es/bilbao.html?v=por_hora'
# this is the url that we've already determined is safe and legal to scrape from.

page_response = requests.get(page_link, timeout=5)
# here, we fetch the content from the url, using the requests library

page_content = BeautifulSoup(page_response.content, "html.parser")
#we use the html parser to parse the url content and store it in a variable.

def preprocesarTormentas(tormenta):
    # Eliminar saltos de linea y tabulaciones
    tormenta = re.sub(r'[\n\t]', "", tormenta)
    # Eliminar múltiples espacios
    tormenta = re.sub(' +',' ',tormenta)
    return tormenta

def limpiarRegistros(registros):
    for i in range(len(registros)):
        # Si es el primer elemento de la lista, eliminar el antepenúltimo
        if i == 0:
            registros[i].pop(len(registros[i])-4)
        # De lo contrario, borrar el último elemento 
        else:
            registros[i].pop(len(registros[i])-1)
    return registros

def preprocesarRegistros(registros):
    """Funcion que se encarga de limpiar la lista que se obtiene de múltiples registros"""
    l = []
    l2 = []
    # Dividir la lista en listas en función de los registros
    for i in range(len(registros)):
        if registros[i] != "Humedad":
            l2.append(registros[i])
        else:
            if l2 != []:
                l.append(l2)
                l2 = []
            l2.append('Humedad')
        if i == len(registros)-1:
            l.append(l2)
    l = limpiarRegistros(l)
    return l

def saveCSV(registros, dias):
    j=0
    with open("/home/mikel/Master/Tipología_y_ciclo_de_vida_de_los_datos/Practica1/Test/Dataset.csv", 'w', encoding='utf8') as mycsv:
        wr = csv.writer(mycsv)
        wr.writerow(['Dia','Hora','Previsión','Velocidad','Rachas','Lluvias','Nieve','Nubes','Tormenta','Humedad','Presión','Sensación térmica','Prob. precipitación','Hora observación', 'Visibilidad'])
        for i in range(len(horas)):
            if horas[i] == '00:00':
                j = j + 1
            registro = registros[i]
            if i == 0:
                wr.writerow([dias[j], horas[i],previsiones[i], velocidades[i], rachas[i], lluvias[i], nieves[i], nubes[i], tormentas[i], registro[1], registro[3], registro[7], 'NULL', registro[5], registro[9]])
            else:
                if 'Prob. de precipitación' in registro:
                    wr.writerow([dias[j], horas[i],previsiones[i], velocidades[i], rachas[i], lluvias[i], nieves[i], nubes[i], tormentas[i], registro[1], registro[3], registro[7], registro[5], 'NULL', 'NULL'])            
                else:
                    wr.writerow([dias[j], horas[i],previsiones[i], velocidades[i], rachas[i], lluvias[i], nieves[i], nubes[i], tormentas[i], registro[1], registro[3], registro[5], 'NULL', 'NULL', 'NULL'])            

#Dias
dias = []
for i in range(0, 4):
    title = page_content.find_all("h2")[i].text
    dias.append(title)

#Horas
horas = page_content.findAll('div',attrs={"class":"m_table_weather_hour_detail_hours"})
horas = [hora.text for hora in horas if hora.text != 'Horas']

#Previsiones
previsiones = page_content.findAll('div',attrs={"class":"m_table_weather_hour_detail_pred"})
previsiones = [prevision.text for prevision in previsiones if prevision.text != 'Previsión']

#Velocidades
velocidades = page_content.findAll('div',attrs={"class":"m_table_weather_hour_detail_med"})
velocidades = [velocidad.text for velocidad in velocidades if velocidad.text != 'Velocidad']

#Rachas
rachas = [racha.text for datos in page_content.findAll('div',attrs={"class":"m_table_weather_hour_detail_gust m_table_weather_hour_detail_child_mobile"}) for racha in datos.findAll('span', attrs={"data-wind-include-units":"1"})]

#Lluvias
lluvias = [lluvia.text for datos in page_content.findAll('div',attrs={"class":"m_table_weather_hour_detail_rain m_table_weather_hour_detail_child_mobile"}) for lluvia in datos.findAll('span') if lluvia.text != "Lluvias"]

#Nieves
nieves = [nieve.text for datos in page_content.findAll('div',attrs={"class":"m_table_weather_hour_detail_snow m_table_weather_hour_detail_child_mobile"}) for nieve in datos.findAll('span') if nieve.text != "Nieve"]

#Nubes
nubes = [nube.text for datos in page_content.findAll('div',attrs={"class":"m_table_weather_hour_detail_clouds m_table_weather_hour_detail_child_mobile"}) for nube in datos.findAll('span') if nube.text != "Nubes"]

#Tormentas
tormentas = [preprocesarTormentas(tormenta.text) for datos in page_content.findAll('div',attrs={"class":"m_table_weather_hour_detail_thunder m_table_weather_hour_detail_child_mobile"}) for tormenta in datos.findAll('span') if tormenta.text != "Tormenta"]
print(tormentas)


#Humedad, Presion, Sensacion terminca, Prob. precipitación, Hora observación, Visibilidad
registros = [datosInternos.text for datos in page_content.findAll('div', attrs={"class":"m_table_weather_hour_detail_child"}) for datosInternos in datos.findAll('span')]
registros = preprocesarRegistros(registros)


saveCSV(registros, dias)
