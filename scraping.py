from bs4 import BeautifulSoup
from registro import Registro
import requests
import csv
import re

capitales = ['a-coruna', 'albacete', 'alicante', 'almeria', 'avila', 'badajoz', 'barcelona', 'bilbao', 'burgos', 'caceres', 'cadiz', 'castellon-de-la-plana', 'ciudad-real', 'cordoba', 'cuenca', 'girona', 'granada', 'guadalajara', 'huelva', 'huesca', 'jaen', 'las-palmas-de-gran-canaria', 'leon', 'lleida', 'logroño', 'lugo', 'madrid', 'malaga', 'murcia', 'ourense', 'oviedo', 'palencia', 'palma-de-mallorca', 'pamplona', 'pontevedra', 'salamanca', 'san-sebastian', 'santa-cruz-de-tenerife', 'santander', 'segovia', 'sevilla', 'soria', 'tarragona', 'teruel', 'toledo', 'valencia', 'valladolid', 'vitoria', 'zamora', 'zaragoza']


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

def saveCSV(dias, horasCapitales, previsionesCapitales, velocidadesCapitales, rachasCapitales, lluviasCapitales, nievesCapitales, nubesCapitales, tormentasCapitales, registrosCapitales):
    """Función que guarda en un csv los registros obtenidos mediante scraping"""
    with open("/home/mikel/Master/Tipología_y_ciclo_de_vida_de_los_datos/Practica1/Test/Dataset.csv", 'w', encoding='utf8') as mycsv:
        wr = csv.writer(mycsv)
        wr.writerow(['Dia','Hora','Ciudad','Previsión','Velocidad','Rachas','Lluvias','Nieve','Nubes','Tormenta','Humedad','Presión','Sensación térmica','Prob. precipitación','Hora observación', 'Visibilidad'])
        for j in range(len(capitales)):
            z = 0
            for i in range(len(horasCapitales[j])):
                if horasCapitales[j][i] == '00:00':
                    z = z + 1
                registro = registrosCapitales[j][i]
                if i == 0:
                    wr.writerow([dias[z], horasCapitales[j][i], capitales[j], previsionesCapitales[j][i], velocidadesCapitales[j][i], rachasCapitales[j][i], lluviasCapitales[j][i], nievesCapitales[j][i], nubesCapitales[j][i], tormentasCapitales[j][i], registro[1], registro[3], registro[7], 'NULL', registro[5], registro[9]])
                else:
                    if 'Prob. de precipitación' in registro:
                        wr.writerow([dias[z], horasCapitales[j][i], capitales[j], previsionesCapitales[j][i], velocidadesCapitales[j][i], rachasCapitales[j][i], lluviasCapitales[j][i], nievesCapitales[j][i], nubesCapitales[j][i], tormentasCapitales[j][i], registro[1], registro[3], registro[7], registro[5], 'NULL', 'NULL'])
                    else:
                        wr.writerow([dias[z], horasCapitales[j][i], capitales[j], previsionesCapitales[j][i], velocidadesCapitales[j][i], rachasCapitales[j][i], lluviasCapitales[j][i], nievesCapitales[j][i], nubesCapitales[j][i], tormentasCapitales[j][i], registro[1], registro[3], registro[5], 'NULL', 'NULL', 'NULL'])

def getCapitalRegistros(page_content):
    """Funcion que obtiene todos los registros de una capital"""
    resultado = []
    #Horas
    horas = page_content.findAll('div',attrs={"class":"m_table_weather_hour_detail_hours"})
    horas = [hora.text for hora in horas if hora.text != 'Horas']
    resultado.append(horas)

    #Previsiones
    previsiones = page_content.findAll('div',attrs={"class":"m_table_weather_hour_detail_pred"})
    previsiones = [prevision.text for prevision in previsiones if prevision.text != 'Previsión']
    resultado.append(previsiones)

    #Velocidades
    velocidades = page_content.findAll('div',attrs={"class":"m_table_weather_hour_detail_med"})
    velocidades = [velocidad.text for velocidad in velocidades if velocidad.text != 'Velocidad']
    resultado.append(velocidades)

    #Rachas
    rachas = [racha.text for datos in page_content.findAll('div',attrs={"class":"m_table_weather_hour_detail_gust m_table_weather_hour_detail_child_mobile"}) for racha in datos.findAll('span') if racha.text != "Rachas"]
    resultado.append(rachas)

    #Lluvias
    lluvias = [lluvia.text for datos in page_content.findAll('div',attrs={"class":"m_table_weather_hour_detail_rain m_table_weather_hour_detail_child_mobile"}) for lluvia in datos.findAll('span') if lluvia.text != "Lluvias"]
    resultado.append(lluvias)

    #Nieves
    nieves = [nieve.text for datos in page_content.findAll('div',attrs={"class":"m_table_weather_hour_detail_snow m_table_weather_hour_detail_child_mobile"}) for nieve in datos.findAll('span') if nieve.text != "Nieve"]
    resultado.append(nieves)

    #Nubes
    nubes = [nube.text for datos in page_content.findAll('div',attrs={"class":"m_table_weather_hour_detail_clouds m_table_weather_hour_detail_child_mobile"}) for nube in datos.findAll('span') if nube.text != "Nubes"]
    resultado.append(nubes)

    #Tormentas
    tormentas = [preprocesarTormentas(tormenta.text) for datos in page_content.findAll('div',attrs={"class":"m_table_weather_hour_detail_thunder m_table_weather_hour_detail_child_mobile"}) for tormenta in datos.findAll('span') if tormenta.text != "Tormenta"]
    resultado.append(tormentas)


    #Humedad, Presion, Sensacion terminca, Prob. precipitación, Hora observación, Visibilidad
    registros = [datosInternos.text for datos in page_content.findAll('div', attrs={"class":"m_table_weather_hour_detail_child"}) for datosInternos in datos.findAll('span')]
    registros = preprocesarRegistros(registros)
    resultado.append(registros)

    return resultado

def getDias(page_content):
    """Función que obtiene el campo dias de cada registro"""
    dias = []
    for i in range(0, 4):
        title = page_content.find_all("h2")[i].text
        dias.append(title)
    return dias

# Inicializar listas
horasCapitales, previsionesCapitales, velocidadesCapitales, rachasCapitales, lluviasCapitales, nievesCapitales, nubesCapitales, tormentasCapitales, registrosCapitales = ([] for i in range(9))
for capital in capitales:
    # URL a la que hacer scraping
    page_link = 'https://www.eltiempo.es/' + capital + '.html?v=por_hora'
    # Respuesta devuelta por requests
    page_response = requests.get(page_link, timeout=5)
    # Contenido html de la URL solicitada
    page_content = BeautifulSoup(page_response.content, "html.parser")
    # Horas, previsiones, velocidades, rachas, lluvias, nieves, nubes, tormentas, Humedad, Presion,
    # Sensacion terminca, Prob. precipitación, Hora observación, Visibilidad
    capitalRegistros = getCapitalRegistros(page_content)
    horasCapitales.append(capitalRegistros[0])
    previsionesCapitales.append(capitalRegistros[1])
    velocidadesCapitales.append(capitalRegistros[2])
    rachasCapitales.append(capitalRegistros[3])
    lluviasCapitales.append(capitalRegistros[4])
    nievesCapitales.append(capitalRegistros[5])
    nubesCapitales.append(capitalRegistros[6])
    tormentasCapitales.append(capitalRegistros[7])
    registrosCapitales.append(capitalRegistros[8])

#Dias
dias = getDias(page_content)

saveCSV(dias, horasCapitales, previsionesCapitales, velocidadesCapitales, rachasCapitales, lluviasCapitales, nievesCapitales, nubesCapitales, tormentasCapitales, registrosCapitales)
