from bs4 import BeautifulSoup
import requests
from classe import Pais
from operator import attrgetter
import json

def Raspar():
  url= 'https://www.worldometers.info/coronavirus/'
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')

  #Pega o as informações e cria os objetos
  paises = []
  for row in soup.table.find_all('tr')[8:]:
    tudo = row.text.split('\n')

    #Exceção para os totais
    if tudo[2] != 'Total:':
      tudo [2] = Pais(tudo[2],int(tudo[3].replace(',','')),tudo[5].strip().replace(',',''),tudo[7].replace(',','.'),tudo[13].replace(',','.'),'','',tudo[16])

      if tudo[2] != 'Diamon Princess':
        paises.append(tudo[2])

  #Substitui países que tem valores vazios por '0'
  for i in paises:
    if i.morte == '':
      i.morte = '0'
    if i.curado == '':
      i.curado = '0'
    if i.teste == '':
      i.teste = 'Indisponível'

  #Determinar fatalidade do país
  for i in paises:
    i.morte = int(i.morte)
    i.fatalidade = (i.morte / i.caso) * 100
    i.fatalidade = "%.1f" % i.fatalidade

  #Altera o nome de países que estão colocados de forma diferente
  for i in paises:
    if i.nome == 'USA':
      i.nome = 'United States'
    elif i.nome == 'S. Korea':
      i.nome = 'South Korea'
    elif i.nome == 'UK':
      i.nome = 'United Kingdom'
    elif i.nome == 'UAE':
      i.nome = 'United Arab Emirates'
    elif i.nome == 'Ivory Coast':
      i.nome = "Côte d'Ivoire (Ivory Coast)"

  
  arq_json = open('emojis.json', 'r', encoding='utf-8')
  emojis_json = json.loads(arq_json.read())
  arq_json.close()
  for pais in paises:
    for emoji in emojis_json:
      if pais.nome == emoji['name']:
        pais.emoji = emoji['emoji']


  #Organizar os objetos pelo número casos
  paises.sort(key= attrgetter('caso'),reverse=True)
  for i in paises:
    i.caso = '{0:,}'.format(i.caso).replace(',','.')
    i.morte = '{0:,}'.format(i.morte).replace(',','.')

  #Organiza os países por continente e traduz o nome dos continentes para Português
  europa = []
  asia = []
  america_sul = []
  america_norte = []
  africa = []
  oceania = []

  for i in paises:
    if i.continente == 'North America':
      i.continente = 'América do Norte'
      america_norte.append(i)
    elif i.continente == 'South America':
      i.continente = 'América do Sul'
      america_sul.append(i)
    elif i.continente == 'Africa':
      i.continente = 'África'
      africa.append(i)
    elif i.continente == 'Europe':
      i.continente = 'Europa'
      europa.append(i)
    elif i.continente == 'Asia':
      i.continente = 'Ásia'
      asia.append(i)
    elif i.continente == 'Australia/Oceania':
      i.continente = 'Oceania'
      oceania.append(i)

  #Retira os totais da lista de países
  for i in paises:
    if i.nome == 'Total:':
      paises.remove(i)
  for i in paises:
    if i.nome == 'Total:':
      paises.remove(i)

  return([oceania,africa,asia,europa,america_norte,america_sul,paises])