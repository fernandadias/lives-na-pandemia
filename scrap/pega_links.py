#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# > EXEMPLO
# - Obtendo produtos do Mercado Livre a partir de uma busca realizada pelo usuário

import requests
from bs4 import BeautifulSoup
from time import sleep

links = []
iniciais = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z', '[0-9]']

def pega_links_dos_artistas(inicial):
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



def start():
    for inicial in iniciais:
        pega_links_dos_artistas(inicial)

start()

#pega_detalhes('https://www.cifras.com.br/a-balladeer')