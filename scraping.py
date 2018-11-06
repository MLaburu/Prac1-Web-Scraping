from bs4 import BeautifulSoup
import requests
# Here, we're just importing both Beautiful Soup and the Requests library

page_link = 'https://www.eltiempo.es/bilbao.html?v=por_hora'
# this is the url that we've already determined is safe and legal to scrape from.

page_response = requests.get(page_link, timeout=5)
# here, we fetch the content from the url, using the requests library

page_content = BeautifulSoup(page_response.content, "html.parser")
#we use the html parser to parse the url content and store it in a variable.

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

#Vientos
vientos = page_content.findAll('div',attrs={"class":"m_table_weather_hour_detail_wind"})
vientos = [viento.text for viento in vientos if viento.text != 'Viento']

#Velocidades
velocidades = page_content.findAll('div',attrs={"class":"m_table_weather_hour_detail_med"})
velocidades = [velocidad.text for velocidad in velocidades if velocidad.text != 'Velocidad']

#Vientos
rachas = [racha.text for datos in page_content.findAll('div',attrs={"class":"m_table_weather_hour_detail_gust m_table_weather_hour_detail_child_mobile"}) for racha in datos.findAll('span', attrs={"data-wind-include-units":"1"})]

#Lluvias
lluvias = [lluvia.text for datos in page_content.findAll('div',attrs={"class":"m_table_weather_hour_detail_rain m_table_weather_hour_detail_child_mobile"}) for lluvia in datos.findAll('span') if lluvia.text != "Lluvias"]

#Nieves
nieves = [nieve.text for datos in page_content.findAll('div',attrs={"class":"m_table_weather_hour_detail_snow m_table_weather_hour_detail_child_mobile"}) for nieve in datos.findAll('span') if nieve.text != "Nieve"]

#Nubes
nubes = [nube.text for datos in page_content.findAll('div',attrs={"class":"m_table_weather_hour_detail_clouds m_table_weather_hour_detail_child_mobile"}) for nube in datos.findAll('span') if nube.text != "Nubes"]

#Tormentas
tormentas = [tormenta.text for datos in page_content.findAll('div',attrs={"class":"m_table_weather_hour_detail_thunder m_table_weather_hour_detail_child_mobile"}) for tormenta in datos.findAll('span') if tormenta.text != "Tormenta"]

#Humedades
humedades = [humedad.text for datos in page_content.findAll('div',attrs={"class":"m_table_weather_hour_detail_child m_table_weather_hour_detail_hum"}) for humedad in datos.findAll('span') if humedad.text != "Humedad"]
