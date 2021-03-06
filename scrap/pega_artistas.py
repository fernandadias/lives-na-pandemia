#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import requests
from bs4 import BeautifulSoup
from time import sleep
import csv


_temp_ = []
links = []
iniciais = ['b', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z', '[0-9]']
paises = {
    'https://www.e-chords.com/t/f1.gif': 'Brasil',
    'https://www.e-chords.com/t/f2.gif': 'Inglaterra',
    'https://www.e-chords.com/t/f3.gif': 'Espanha',
    'https://www.e-chords.com/t/f4.gif': 'Italia',
    'https://www.e-chords.com/t/f5.gif': 'França',
    'https://www.e-chords.com/t/f6.gif': 'México',
    'https://www.e-chords.com/t/f7.gif': 'Alemanha',
    'https://www.e-chords.com/t/f8.gif': 'Escócia',
    'https://www.e-chords.com/t/f9.gif': 'Japão',
    'https://www.e-chords.com/t/f10.gif': 'USA',
    'https://www.e-chords.com/t/f11.gif': 'Portugal',
    'https://www.e-chords.com/t/f12.gif': 'Austrália',
    'https://www.e-chords.com/t/f13.gif': 'Jamaica',
    'https://www.e-chords.com/t/f14.gif': 'Canadá',
    'https://www.e-chords.com/t/f15.gif': 'Suécia',
    'https://www.e-chords.com/t/f16.gif': 'Cuba',
    'https://www.e-chords.com/t/f17.gif': 'Colombia',
    'https://www.e-chords.com/t/f18.gif': 'Chile',
    'https://www.e-chords.com/t/f19.gif': 'Finlândia',
    'https://www.e-chords.com/t/f20.gif': 'Noruega',
    'https://www.e-chords.com/t/f21.gif': 'China',
    'https://www.e-chords.com/t/f22.gif': 'Peru',
    'https://www.e-chords.com/t/f23.gif': 'cabo Verde',
    'https://www.e-chords.com/t/f24.gif': 'Suiça',
    'https://www.e-chords.com/t/f25.gif': 'desconhecido',
    'https://www.e-chords.com/t/f26.gif': 'Porto Rico',
    'https://www.e-chords.com/t/f27.gif': 'Argentina',
    'https://www.e-chords.com/t/f28.gif': 'Irlanda',
    'https://www.e-chords.com/t/f29.gif': 'Polônia',
    'https://www.e-chords.com/t/f30.gif': 'Dinamarca',
    'https://www.e-chords.com/t/f31.gif': 'Islândia',
    'https://www.e-chords.com/t/f32.gif': 'Austria',
    'https://www.e-chords.com/t/f33.gif': 'Hungria',
    'https://www.e-chords.com/t/f34.gif': 'Africa do Sul',
    'https://www.e-chords.com/t/f35.gif': 'Uruguai',
    'https://www.e-chords.com/t/f36.gif': 'Iraque',
    'https://www.e-chords.com/t/f37.gif': 'Nicaragua',
    'https://www.e-chords.com/t/f38.gif': 'Filipinas',
    'https://www.e-chords.com/t/f39.gif': 'Arábia Saudíta',
    'https://www.e-chords.com/t/f40.gif': 'Venezuela',
    'https://www.e-chords.com/t/f41.gif': 'Rússia',
    'https://www.e-chords.com/t/f42.gif': 'Bolívia',
    'https://www.e-chords.com/t/f43.gif': 'Irã',
    'https://www.e-chords.com/t/f44.gif': 'Austrália',
    'https://www.e-chords.com/t/f45.gif': 'Costa Rica',
    'https://www.e-chords.com/t/f46.gif': 'India',
    'https://www.e-chords.com/t/f47.gif': 'Belgica',
    'https://www.e-chords.com/t/f48.gif': 'Indonesia',
    'https://www.e-chords.com/t/f49.gif': 'Rep. Dominicana',
    'https://www.e-chords.com/t/f50.gif': 'Panamá',
    'https://www.e-chords.com/t/f51.gif': 'Paraguai',
    'https://www.e-chords.com/t/f52.gif': 'Koryakia',
    'https://www.e-chords.com/t/f53.gif': 'Koryakia',
    'https://www.e-chords.com/t/f53.gif': 'Luxemburgo',
    'https://www.e-chords.com/t/f54.gif': 'Israel',
    'https://www.e-chords.com/t/f55.gif': 'Austria',
    'https://www.e-chords.com/t/f56.gif': 'Turquia',
    'https://www.e-chords.com/t/f57.gif': 'Grécia',
    'https://www.e-chords.com/t/f58.gif': 'Croácia',
    'https://www.e-chords.com/t/f59.gif': 'Slovenia',
    'https://www.e-chords.com/t/f60.gif': 'Equador',
    'https://www.e-chords.com/t/f61.gif': 'El Salvador',
    'https://www.e-chords.com/t/f62.gif': 'Wales',
    'https://www.e-chords.com/t/f63.gif': 'Paquistão',
    'https://www.e-chords.com/t/f64.gif': 'Andorra',
    'https://www.e-chords.com/t/f65.gif': 'Estonia',
    'https://www.e-chords.com/t/f66.gif': 'Coreia do Sul',
    'https://www.e-chords.com/t/f67.gif': 'Angola',
    'https://www.e-chords.com/t/f68.gif': 'desconhecido',
}

aux = 0

#Python class for declaring movie attributes. 
class ExtrairArtistas(object):      
    def __init__(self, link, nome,  pais, foto, estilo, musicas ):
        self.link = link
        self.nome = nome
        self.pais = pais
        self.foto = foto
        self.estilo = estilo
        self.musicas = musicas

def pega_links_dos_artistas(inicial):
    baseUrl_cifras = 'https://www.cifras.com.br/letra/'+inicial
    response = requests.get(baseUrl_cifras)

    sleep(5)

    artistas_links_pagina = BeautifulSoup(
        response.text, 'html.parser'
        ).find(
            'table', attrs={'class': 'pages'}).find_all('p')

    for artista in artistas_links_pagina:
        links.append(artista.find('a')['href']) 

    return(links)




def pega_artistas_na_pagina(inicial):

    baseUrl_cifras = 'https://www.cifras.com.br/letra/'+inicial
    response = requests.get(baseUrl_cifras)

    sleep(3)

    artistas_pagina = BeautifulSoup(
        response.text, 'html.parser'
        ).find(
            'table', attrs={'class': 'pages'}).find_all('p')

    for artista in artistas_pagina:
        link = artista.find('a')['href']
        nome = artista.find('a').text
        bandeira = artista.find('img')['src']
        pais = paises[bandeira]
        
        print('>>>>>>>INICIO:')
        print('Link:', link)
        print('Artista:', nome)
        print('Pais:', pais)

        foto, estilo, musicas = pega_detalhes(link)

        print('Foto:', foto)
        print('Estilo:', estilo)
        print('Musicas:', musicas)

        artista_atual = ExtrairArtistas(link, nome, pais, estilo, musicas, foto)

        #print(vars(artista_atual))
        print('\n\n')

        _temp_.append(artista_atual)

        global aux
        aux = aux + 1;
        if aux == 10:
            break

    return _temp_


        
        


def pega_detalhes(link):
    response = requests.get(link)

    artista_detalhe = BeautifulSoup(
        response.text, 'html.parser'
        ).find(
            'div', attrs={'id': 'artista-info'})

    sleep(3)

    el_foto = artista_detalhe.find('img')
    foto = el_foto['src'] if el_foto else ''

    detalhes = artista_detalhe.find('p', attrs={'class':'infomustit'})

    el_musicas = detalhes.find('span')
    musicas = el_musicas.text.strip() if el_musicas else ''
    
    remover = detalhes.find('span').extract()
    estilo = detalhes.text.strip() if detalhes.text.strip() else ''

    #print('Foto:', foto)
    #print('Estilo:', estilo)
    #print('Musicas:', musicas)
    #print('\n\n\n\n')

    return (foto, estilo, musicas)


def start():
    for inicial in iniciais:
        pag = pega_artistas_na_pagina(inicial)
        write_data(pag, inicial+'_results.csv')

#pega_artistas_na_pagina('a')

#pega_artistas_na_pagina('a')
#teste = pega_links_dos_artistas('a')
#print(dir(teste))

start()

def write_data(data,name):
    file_name =name
    with open(file_name,'a',errors='ignore',newline='') as f:
        f_csv =csv.writer(f)
        f_csv.writerows(data)

#pega_detalhes('https://www.cifras.com.br/a-balladeer')