#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# > EXEMPLO
# - Obtendo produtos do Mercado Livre a partir de uma busca realizada pelo usuário

import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

links = []
todos_os_links = []
iniciais = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z', '[0-9]']

def pega_links_por_inicial(inicial):
    baseUrl_cifras = 'https://www.cifras.com.br/letra/'+inicial
    response = requests.get(baseUrl_cifras)

    sleep(10)

    artistas_links_pagina = BeautifulSoup(
        response.text, 'html.parser'
        ).find(
            'table', attrs={'class': 'pages'}).find_all('p')

    for artista in artistas_links_pagina:
        novo_link = artista.find('a')['href']
        print(novo_link)
        links.append(novo_link)

    return(links)



def pega_todos_os_links():
    for inicial in iniciais:
        pega_links_por_inicial(inicial)

d = pega_links_por_inicial('a')

df = pd.DataFrame(data={'link': d})
df.to_csv('./teste.csv', sep=',',index=False)


todos_os_links = pega_todos_os_links()

#pega_detalhes('https://www.cifras.com.br/a-balladeer')