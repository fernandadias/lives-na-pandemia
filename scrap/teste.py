#!/usr/bin/env python
# -*- coding: utf-8 -*- 

### Codigo Python de Scraping no Cifras.com e Letras.com ###

# Packages:
import urllib.request as Request, urllib  # copia paginas html
from bs4 import BeautifulSoup  # functions to parse the data returned from the website
import re
import pandas as pd
import numpy as np

# Step 1: Funcoes
# 1. Pega lista de artistas do site a partir da letra do alfabeto
def pega_lista_artistas(letra):
    link_artista_letra = ("http://www.cifras.com.br/letra/" + letra)
    req = Request(link_artista_letra, headers={'User-Agent': 'Mozilla/5.0'})

    pagina_artista = urllib.urlopen(req)
    for line_number, line in enumerate(pagina_artista):
        # Because this is 0-index based
        if line_number == 419:
            linha_1 = line
        elif line_number == 420:
            linha_2 = line
        # Stop reading
        elif line_number > 420:
            break
    return (linha_1, linha_2)

print(pega_lista_artistas('a'))