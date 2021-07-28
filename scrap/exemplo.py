### Codigo Python de Scraping no Cifras.com e Letras.com ###

# Packages:
import urllib.request as urllib  # copia paginas html
from bs4 import BeautifulSoup  # functions to parse the data returned from the website
import re
import pandas as pd
import numpy as np


# Step 1: Funcoes
# 1. Pega lista de artistas do site a partir da letra do alfabeto
def pega_lista_artistas(letra):
    link_artista_letra = ("http://www.cifras.com.br/letra/" + letra)
    pagina_artista = urllib.urlopen(link_artista_letra)
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


# 2. Pega informacoes do artista (qtde de musicas, genero, posicao inicial e final das musicas) a partir do arquivo baixado:
def pega_info_artista_1(file):
    line_number = 0
    for line in open(file, encoding="ISO-8859-1"):
        line_number += 1
        if line_number == 365:
            genero = line
            genero = genero.replace("\t", "")
            genero = genero.replace(" <br />\n", "")
        if line_number == 368:
            qtde_musicas = line
            qtde_musicas = qtde_musicas.replace("\t", "")
            qtde_musicas = qtde_musicas.replace("\r", "")
            qtde_musicas = qtde_musicas.replace("\n", "")
            qtde_musicas = qtde_musicas.replace(" ", "")
            qtde_musicas = int(qtde_musicas.replace("músicas", ""))
        elif "</h3>" in line:
            inicio = line_number
        elif "<p>Não encontrou a música que você está procurando?<br>" in line:
            final = line_number
            break

    return (genero, qtde_musicas, inicio, final)

# 3. Pega lista de links de musica a partir da posicao no arquivo baixado:

def pega_info_artista_2(posicao):
    line_number = 0
    for line in open(file, encoding="ISO-8859-1"):
        line_number += 1
        if line_number == posicao:
            start_link = line.find("href=")
            start_quote = line.find('"', start_link)
            end_quote = line.find('"', start_quote + 1)
            link_musica = line[start_quote + 1:end_quote]


            #link_musica = line
            #link_musica = link_musica.replace("\t", "")
            #link_musica = link_musica.replace("<a href=", "")
            #link_musica = link_musica.replace(" class=\"list-group-item\" style=\'font-size:18px;  font-weight:bold\' >\n", "")
            #link_musica = link_musica.replace(" class=\"list-group-item\" ", "")
            #link_musica = link_musica.replace("style=\'font-size:18px;  font-weight:bold\'", "")
            #link_musica = link_musica.replace(" >\n", "")
            #link_musica = link_musica.replace("\"", "")
            break
    return (link_musica)


def pega_info_artista_3(file):
    lista_links_letras = []
    line_number = 0
    for line in open(file, encoding="ISO-8859-1"):
            line_number += 1
            if "<li class=\"c" in line:
                start_link = line.find("href=")
                start_quote = line.find('"', start_link)
                end_quote = line.find('"', start_quote + 1)
                link_letra = line[start_quote + 1:end_quote - 1]
                lista_links_letras.append(link_letra)
    return lista_links_letras

# 4. Pega cifra e letra a partir do link da musica:

def pega_cifra(link_musica) :
    page = urllib.urlopen(link_musica)  # copia a pagina
    soup = BeautifulSoup(page)  # transforma a pagina em um objeto beautiful soup
    song = soup.pre  # copiando o conteudo da tag <pre>
    song = str(song)  # convertendo pra string
    result = re.findall("<u>(.*)</u>", song)  # copiando o trecho dos acordes, pela tag <u>
    result = str(result)  # convertendo de lista pra string, para permitir fazer algumas mudancas
    result = result.replace("</u>", ",").replace("<u>", ",").replace("/ ", ",").replace("//", "/").replace(" ",
                                                                                                           "").replace(
        ",,", ",").replace(",,", ",").replace(",,", ",").replace(",,", ",").replace(",,", ",").replace(",,",
                                                                                                       ",").replace(
        ",,", ",").replace(",,", ",").replace("'", "").replace(";", "").replace("\\", "").replace("t", "")

    result = result[1:-1]
    result_list = result.split(",")  # transformando em lista de novo
    return result_list

def pega_letra(link_letra) :
    page = urllib.urlopen(link_letra)  # copia a pagina
    soup = BeautifulSoup(page)  # transforma a pagina em um objeto beautiful soup
    letra = soup.find(id="letra").string
    letra = letra.replace("\n\t", "").replace("\r", "").replace("\t", "").replace("\n", "|").replace("| |", "|").replace("| |", "|").replace("| |", "|")
    for p in soup.find_all("p", attrs={'class':'artCompositor'}):
        compositor = p.text.replace(" Compositor:", "")
    return (letra, compositor)

# 5. Executa funcao de lista de artistas
alfabeto = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
                "v", "w", "x", "y", "z", "[0-9]"]

lista_artistas = []

for letra in alfabeto:
    soup = BeautifulSoup(str(pega_lista_artistas(letra)))
    for ptag in soup.find_all('p'):
        try:
            lista_artistas.append(ptag.a["href"] + ": " + ptag.img["src"].replace("http://e-chords.com/t/", ""))
        except:
            pass
    print(letra)
lista_artistas = dict(map(str, x.split(':')) for x in lista_artistas)
lista_artistas = {k: v for k, v in lista_artistas.items() if v == " f1.gif"}
lista_artistas = list(lista_artistas.keys())
lista_artistas = ['chiclete-com-banana', 'asa-de-aguia', 'ivete-sangalo', 'babado-novo', 'harmonia-do-samba', 'banda-eva', 'claudia-leitte', 'daniela-mercury', 'banda-grafith', 'ricardo-chaves', 'timbalada', 'araketu', 'chicabana', 'netinho', 'oz-bambaz', 'companhia-do-calypso', 'banda-passarela', 'carlinhos-brown', 'parangole', 'banda-cheiro-de-amor', 'psirico', 'tomate', 'olodum', 'chicana', 'bambakere', 'terrasamba', 'rapazolla', 'a-zorra', 'os-charadas', 'fantasmao', 'alexandre-peixe', 'banda-mel', 'ceceu-muniz', 'tchakabum', 'voa-dois', 'ed-motta', 'celso-blues-boy', 'dblack', 'ivan-correa', 'toquinho', 'dick-farney', 'joao-gilberto', 'sylvia-telles', 'joyce', 'baden-powell', 'silvia-telles', 'tito-madi', 'amado-batista', 'banda-calypso', 'reginaldo-rossi', 'adelino-nascimento', 'paulo-sergio', 'wander-wildner', 'ricardo-braga', 'jose-orlando', 'odair-jose', 'cristiano-neves', 'carlos-alexandre', 'barto-galeno', 'roberto-leal', 'balthazar', 'genival-santos', 'banda-floribella', 'jose-ribeiro', 'waldick-soriano', 'paulo-marcio', 'tarcys-andrade', 'alipio-martins', 'evaldo-freire', 'assis-cavalcanti', 'evaldo-braga', 'michelle-melo', 'roberto-muller', 'sidney-magal', 'banda-da-loirinha', 'mauricio-reis', 'avioes-do-forro', 'forro-sotaque-bacana', 'garota-safada', 'luiz-gonzaga', 'limao-com-mel', 'calcinha-preta', 'alceu-valenca', 'desejo-de-menina', 'mastruz-com-leite', 'saia-rodada', 'wesley-safadao', 'morais-do-acordeon', 'emiliano-pordeus', 'elba-ramalho', 'estakazero', 'falamansa', 'forro-do-muido', 'flavio-jose', 'dorgival-dantas', 'banda-magnificos', 'cavaleiros-do-forro', 'dominguinhos', 'rita-de-cassia', 'circulado-de-fulo', 'frank-aguiar', 'geraldinho-lins', 'tayrone-cigano', 'trio-nordestino', 'asas-livres', 'cangaia-de-jegue', 'gabriel-diniz', 'kelvin-do-acordeom', 'mala-100-alca', 'jose-marques', 'forro-100-grillo', 'rastape', 'sirano-sirino', 'solteiroes-do-forro', 'collo-de-menina', 'raiz-do-sana', 'banda-labaredas', 'mulher-sarada', 'banda-treme-terra', 'trio-forrozao', 'trio-virgulino', 'bonde-do-forro', 'cheiro-de-menina', 'novo-tom', 'edigar-mao-branca', 'adelmario-coelho', 'jorge-ben-jor', 'pirata-celestino', 'latino', 'anitta', 'claudinho-buchecha', 'perlla', 'mc-naldo', 'mc-marcinho', 'catolicas', 'harpa-crista', 'corinhos-evangelicos', 'padres', 'comunidades', 'igreja-crista-maranata', 'diante-do-trono', 'renascer-praise', 'padre-zezinho', 'oficina-g3', 'igrejas', 'aline-barros', 'hinario-adventista', 'voz-da-verdade', 'catedral', 'david-quinlan', 'fernanda-brum', 'andre-valadao', 'vencedores-por-cristo', 'ludmila-ferber', 'santa-geracao', 'kleber-lucas', 'cantor-cristao', 'asaph-borba', 'cassiane', 'fernandinho', 'toque-no-altar', 'rosa-de-saron', 'sergio-lopes', 'eyshila', 'filhos-do-homem', 'daniel-souza', 'comunidade-catolica-shalom', 'resgate', 'gerson-rufino', 'novo-som', 'thalles-roberto', 'cristina-mel', 'ouvir-e-crer', 'shirley-carvalhaes', 'louvemos', 'vineyard-music', 'anjos-de-resgate', 'daniel-e-samuel', 'ministerio-koinonya-de-louvor', 'casa-de-davi', 'adhemar-de-campos', 'joao-alexandre', 'carlinhos-felix', 'musicas-infantis', 'cantinho-da-crianca', 'trem-da-alegria', 'dominio-publico', 'cagerio-de-souza', 'turma-do-balao-magico', 'balao-magico', 'assis-valente', 'carlos-rogerio', 'roberto-carlos', 'the-fevers', 'erasmo-carlos', 'renato-e-seus-blue-caps', 'jose-roberto', 'jerry-adriani', 'wanderley-cardoso', 'vanusa', 'wanderlea', 'almir-bezerra', 'ronnie-von', 'golden-boys', 'os-incriveis', 'the-originals', 'carlos-gonzaga', 'celly-campello', 'demetrius', 'eduardo-araujo', 'caetano-veloso', 'chico-buarque', 'djavan', 'elis-regina', 'ze-ramalho', 'gilberto-gil', 'jorge-vercillo', 'fagner', 'milton-nascimento', 'marisa-monte', 'tom-jobim', 'zeca-baleiro', 'tim-maia', 'oswaldo-montenegro', 'simone', 'maria-bethania', 'joao-bosco', 'alcione', 'fabio-junior', 'gal-costa', 'vinicius-de-moraes', 'adriana-calcanhotto', 'ney-matogrosso', 'ivan-lins', 'leoni', 'leila-pinheiro', 'wilson-simonal', 'seu-jorge', 'pery-ribeiro', 'jose-augusto', 'lenine', 'guilherme-arantes', 'belchior', 'flavio-venturini', '14-bis', 'vander-lee', 'paulinho-moska', 'rosana', 'mpb4', 'agostinho-dos-santos', 'clara-nunes', 'gonzaguinha', 'vanessa-da-mata', 'o-teatro-magico', 'leo-magalhaes', 'chico-cesar', 'fernando-mendes', 'nora-ney', 'tom-ze', 'maria-rita', 'emilio-santiago', 'roupa-nova', 'kid-abelha', 'belo', 'daniel', 'ana-carolina', 'sandy-junior', 'biquini-cavadao', 'cazuza', 'rosa-morena-e-platino', 'cristian-castro', 'ls-jack', 'lucas-lucco', 'reacao-em-cadeia', 'emmerson-nogueira', 'claudette-soares', 'mamonas-assassinas', 'alexandre-pires', 'banda-sayonara', 'falcao', 'dibob', 'looppy-neves', 'benito-di-paula', 'agnaldo-rayol', 'cauby-peixoto', 'nubia-lafayette', 'scracho', 'camisa-de-venus', 'high-school-musical', 'klb', 'papas-da-lingua', 'cachorro-grande', 'luiza-possi', 'wanessa-camargo', 'ratto', 'marconi-branco', 'wanda-sa', 'neanderthal', 'tiago-iorc', 'the-flanders', 'marjorie-estiano', 'armando-manzanero', 'clarice-falcao', 'rebeldes-(brasil)', 'frejat', 'moacyr-franco', 'maria-do-relento', 'marcelo-camelo', 'walter-viana', 'areia-lima', 'o-rappa', 'sampa-crew', 'projota', 'planet-hemp', 'bonde-da-stronda', 'kiko-mello', 'willian-bo', 'faccao-central', 'gabriel-pensador', 'marcelo-d2', 'racionais-mcs', 'apocalipse-16', 'mv-bill', 'rappervil', 'emicida', 'natiruts', 'armandinho', 'cidade-negra', 'planta-e-raiz', 'chimarruts', 'edson-gomes', 'maskavo', 'ponto-de-equilibrio', 'dazaranha', 'tribo-de-jah', 'armandinho-banda', 'casaca', 'mato-seco', 'adao-negro', 'macucos', 'onze20', 'nengo-vieira', 'diamba', 'irie', 'reobote-zion', 'beca-arruda', 'maneva', 'rastaclone', 'jah-live', 'namaste', 'nomad', 'digo-cardkamp-', 'raizes-rasta', 'alma-djem', 'salomao-do-reggae', 'sine-calmon', 'vibracoes-rasta', 'yomanaho', 'edu-ribeiro-cativeiro', 'filosofia-reggae', 'java-roots', 'javaroots', 'crombie', 'tche-garotos', 'ze-geraldo', 'brenda-lee', 'luiz-marenco', 'cesar-oliveira-e-rogerio-melo', 'os-monarcas', 'os-serranos', 'teixeirinha', 'boi-garantido', 'garotos-de-ouro', 'joao-luiz-correa', 'tche-barbaridade', 'joca-martins', 'mano-lima', 'grupo-minuano', 'jose-mendes', 'joelson-e-joedson', 'walter-toniosso', 'gaucho-da-fronteira', 'tche-boys', 'porca-veia', 'raca-fandangueira', 'elomar', 'noel-guarany', 'arraial-do-pavulagem', 'pouca-vogal', 'tom-cleber', 'matraca-berg', 'grupo-rodeio', 'os-mirins', 'cascatinha-e-inhana', 'xangai', 'marcelo-oliveira', 'tche-guri', 'alma-serrana', 'boi-caprichoso', 'adalberto-e-adriano', 'br5-49', 'alemao-ronaldo', 'chiquito-e-grupo-bordoneio', 'nando-cordel', 'osvaldir-e-carlos-magrao', 'tradicionais', 'grupo-candieiro', 'jairo-lambari-fernandes', 'lisandro-amaral-', 'os-campeiros', 'serrote-preto', 'cordel-do-fogo-encantado', 'pinduca', 'charlie-brown-jr', 'engenheiros-do-hawaii', 'raul-seixas', 'titas', 'capital-inicial', 'skank', 'legiao-urbana', 'rita-lee', 'paralamas-do-sucesso', 'cpm-22', 'angra', 'nando-reis', 'lulu-santos', 'sepultura', 'raimundos', 'anti-flag', 'detonautas', 'ira', 'pato-fu', 'nx-zero', 'jota-quest', 'cassia-eller', 'forfun', 'los-hermanos', 'barao-vermelho', 'nenhum-de-nos', 'renato-russo', 'arnaldo-antunes', 'novas-bandas', 'lobao', 'tequila-baby', 'dead-fish', 'os-mutantes', 'zelia-duncan', 'wilson-sideral', 'aliados', 'ultraje-a-rigor', 'darvin', 'nei-van-soria', 'matanza', 'marina-lima', 'danni-carlos', 'tihuana', 'carbona', 'rpm', 'tianastacia', 'paulo-ricardo', 'rouge', 'garotos-podres', 'jay-vaquer', 'fundo-de-quintal', 'zeca-pagodinho', 'exaltasamba', 'sorriso-maroto', 'grupo-revelacao', 'beth-carvalho', 'raca-negra', 'art-popular', 'turma-do-pagode', 'jorge-aragao', 'trio-parada-dura', 'so-pra-contrariar', 'martinho-da-vila', 'paulinho-da-viola', 'pique-novo', 'sensacao', 'jeito-moleque', 'molejo', 'pixote', 'trio-irakitan', 'boka-loka', 'gustavo-lins', 'katinguele', 'reinaldo', 'imaginasamba', 'dudu-nobre', 'bezerra-da-silva', 'negritude-junior', 'cartola', 'leci-brandao', 'os-travessos', 'jackson-do-pandeiro', 'arlindo-cruz', 'inimigos-da-hp', 'thiaguinho', 'grupo-bom-gosto', 'grupo-so-ficar', 'soweto', 'agepe', 'sem-compromisso', 'arlindo-cruz-sombrinha', 'luiz-melodia', 'swing-simpatia', 'rodriguinho', 'samprazer', 'jammil-e-uma-noites', 'almir-guineto', 'tentasamba', 'os-originais-do-samba', 'joao-nogueira', 'bruno-e-marrone', 'zeze-di-camargo-e-luciano', 'tiao-carreiro-e-pardinho', 'edson-e-hudson', 'jorge-e-mateus', 'chitaozinho-xororo', 'milionario-e-jose-rico', 'gusttavo-lima', 'chrystian-e-ralf', 'eduardo-costa', 'victor-e-leo', 'guilherme-e-santiago', 'joao-bosco-e-vinicius', 'luan-santana', 'cesar-menotti-e-fabiano', 'gian-e-giovani', 'joao-neto-e-frederico', 'fernando-e-sorocaba', 'leonardo', 'tonico-e-tinoco', 'paula-fernandes', 'rick-e-renner', 'rio-negro-e-solimoes', 'lourenco-e-lourival', 'cristiano-araujo', 'sergio-reis', 'leandro-e-leonardo', 'joao-carreiro-e-capataz', 'teodoro-e-sampaio', 'conrado-e-aleksandro', 'henrique-e-juliano', 'jads-e-jadson', 'humberto-e-ronaldo', 'gino-e-geno', 'marcos-e-belutti', 'munhoz-e-mariano', 'joao-paulo-e-daniel', 'almir-sater', 'michel-telo', 'cezar-e-paulinho', 'ze-henrique-e-gabriel', 'hugo-pena-e-gabriel', 'matogrosso-e-mathias', 'joao-mineiro-e-marciano', 'israel-e-rodolffo', 'paulinho-natureza', 'grupo-tradicao', 'thaeme-e-thiago', 'israel-novaes', 'chico-rey-e-parana', 'elizeth-cardoso', 'altemar-dutra', 'maysa', 'agnaldo-timoteo', 'nelson-goncalves', 'noel-rosa', 'silvio-caldas', 'orlando-silva', 'dolores-duran', 'adoniran-barbosa', 'demonios-da-garoa', 'dalva-de-oliveira', 'ary-barroso', 'lamartine-babo', 'moreira-da-silva', 'velha-guarda-da-portela', 'lupicinio-rodrigues', 'francisco-alves', 'ataulfo-alves', 'paulo-vanzolini', 'carlos-galhardo', 'vicente-celestino', 'mestre-marcal', 'herivelto-martins', 'jamelao', 'pixinguinha', 'ze-keti']

# 6. Executa funcoes de dados do artista

# 6.1. Executando só a primeira parte, para fazer um corte depois e então executar a segunda.

lista_artistas_dados_1 = []
for nome in lista_artistas:
    try:
        artista_page = ("http://www.cifras.com.br/"+nome)
        #file = (nome+".txt")
        file = "artista.txt"
        urllib.urlretrieve(artista_page, file)
        lista_artistas_dados_1.append((nome,) + pega_info_artista_1(file))
        # termo_inicial = list(pega_info_artista_1(file))[2]+5
        # termo_final = list(pega_info_artista_1(file))[3]-16
        # lista_de_posicoes = []
        # line_number = 0
        # for line in open(file, encoding="ISO-8859-1"):
        #     try:
        #         line_number += 1
        #         if "class=\"list-group-item\"" in line and "ver-2" not in line and "versao-2" not in line\
        #                 and "ver2" not in line and "versao2" not in line:
        #             lista_de_posicoes.append(line_number)
        #         elif line_number > termo_final :
        #             break
        #     except:
        #         pass
        # lista_musicas = []
        # for posicao in lista_de_posicoes:
        #     try:
        #         lista_musicas.append(pega_info_artista_2_(posicao))
        #     except:
        #         pass
        #lista_artistas_dados_2.append(nome + ": " + str(lista_musicas).replace("[", "").replace("]", ""))
        print(nome)
        #lista_artistas_dados_2.append((nome,) + tuple([lista_musicas]))
    except:
        pass

labels_df_artista_1 = ["artista", "genero", "qtde_musicas", "pos_ini", "pos_fim"]
df_artista_1 = pd.DataFrame.from_records(lista_artistas_dados_1, columns=labels_df_artista_1)
# criando colunas genero_ajustado e rankinkg por genero_ajustado
df_artista_1["genero_ajustado"] = np.where(df_artista_1["genero"] == "Besteirol", "Pop Music",
                                 (np.where(df_artista_1["genero"] == "Blues", "Blues/Soul/Jazz",
                                 (np.where(df_artista_1["genero"] == "Brasil", "Pop Music",
                                 (np.where(df_artista_1["genero"] == "Católicas", "Gospel",
                                 (np.where(df_artista_1["genero"] == "Country", "Regional",
                                 (np.where(df_artista_1["genero"] == "Espíritas", "Gospel",
                                 (np.where(df_artista_1["genero"] == "Gaúchas", "Regional",
                                 (np.where(df_artista_1["genero"] == "Heavy Metal", "Rock'n Roll",
                                 (np.where(df_artista_1["genero"] == "Jazz", "Blues/Soul/Jazz",
                                 (np.where(df_artista_1["genero"] == "Pop Rock", "Rock'n Roll",
                                 (np.where(df_artista_1["genero"] == "Punk Rock", "Rock'n Roll",
                                 (np.where(df_artista_1["genero"] == "Rock Alternativo", "Rock'n Roll",
                                 (np.where(df_artista_1["genero"] == "Rock Clássico", "Rock'n Roll",
                                 (np.where(df_artista_1["genero"] == "Romântica", "Pop Music",
                                 (np.where(df_artista_1["genero"] == "Samba Enredo", "Samba e Pagode",
                                 (np.where(df_artista_1["genero"] == "Soul", "Blues/Soul/Jazz",
                                  df_artista_1["genero"])))))))))))))))))))))))))))))))

df_artista_1['rank'] = df_artista_1.groupby(['genero_ajustado'])['qtde_musicas'].rank(ascending=False)

# filtros
df_artista_1_agrupado = df_artista_1.groupby("genero_ajustado").agg({"artista": pd.Series.nunique})
df_artista_1_agrupado = df_artista_1_agrupado.loc[df_artista_1_agrupado['artista'] > 20, :]
df_artista_1_agrupado = df_artista_1_agrupado[df_artista_1_agrupado.index.isin(["Diversos", "Não Informada"]) == False]
df_artista_1_filtrado = df_artista_1[df_artista_1['rank'] <= 50]
df_artista_1_filtrado = df_artista_1_filtrado[df_artista_1_filtrado['qtde_musicas'] > 10]
#df_artista_1_filtrado = df_artista_1_filtrado[df_artista_1_filtrado['genero_ajustado'].isin(list(df_artista_1_agrupado.index))]



# 6.2. Executando a segunda parte, pegando a lista de musicas.
lista_artistas_dados_2 = []
for nome in list(df_artista_1_filtrado["artista"]):
    try:
        artista_page = ("http://www.cifras.com.br/"+nome)
        file = "artista.txt"
        urllib.urlretrieve(artista_page, file)
        #lista_artistas_dados_1.append((nome,) + pega_info_artista_1(file))
        termo_inicial = int(df_artista_1_filtrado.loc[df_artista_1_filtrado['artista'] == nome]['pos_ini'].values+5)
        termo_final = int(df_artista_1_filtrado.loc[df_artista_1_filtrado['artista'] == nome]['pos_fim'].values-16)
        lista_de_posicoes = []
        line_number = 0
        for line in open(file, encoding="ISO-8859-1"):
            try:
                line_number += 1
                if "class=\"list-group-item\"" in line and "ver-2" not in line and "versao-2" not in line\
                        and "ver2" not in line and "versao2" not in line:
                    lista_de_posicoes.append(line_number)
                elif line_number > termo_final :
                    break
            except:
                pass
        lista_musicas = []
        for posicao in lista_de_posicoes:
            try:
                lista_musicas.append(pega_info_artista_2_(posicao))
            except:
                pass
        #lista_artistas_dados_2.append(nome + ": " + str(lista_musicas).replace("[", "").replace("]", ""))
        print(nome)
        lista_artistas_dados_2.append((nome,) + tuple([lista_musicas]))
    except:
        pass

labels_df_artista_2 = ["artista", "lista_de_links_de_musicas"]
df_artista_2 = pd.DataFrame.from_records(lista_artistas_dados_2, columns=labels_df_artista_2)


# 6.3. Pegando a lista de letras
#lista_artistas = ["chico-buarque", "caetano-veloso", "gilberto-gil"]
lista_artistas_links = []
for artista in list(df_artista_1_filtrado["artista"]):
    try:
        artista_page = ("http://www.letras.com.br/" + artista)
        file = "artista_letra.txt"
        urllib.urlretrieve(artista_page, file)
        lista_artistas_links.append((artista,) + tuple([pega_info_artista_3(file)]))
        print(artista)
    except:
        pass

labels_df_artista_letras = ["artista", "lista_de_links_de_letras"]
df_artista_letras = pd.DataFrame.from_records(lista_artistas_links, columns=labels_df_artista_letras)

#Complemento: Lista de links de letras, corrigindo divergencias entre Cigras.com e Letras.com
nomes = ["fabio-junior", "claudinho-buchecha", "sandy-junior", "gabriel-pensador", "armandinho-banda", "chitaozinho-xororo"]
nomes_corrigidos = ["fabio-jr", "claudinho-e-buchecha", "sandy-e-junior", "gabriel-o-pensador", "armandinho", "chitaozinho-e-xororo"]
dic_artista_complemento = {}
for i in range(len(nomes)):
    dic_artista_complemento[nomes[i]] = nomes_corrigidos[i]
df_artista_complemento = pd.DataFrame(list(dic_artista_complemento.items()), columns=['artista', 'artista_ajustado'])

lista_artistas_links_complemento = []
for artista_ajustado in list(df_artista_complemento["artista_ajustado"]):
    try:
        artista_page = ("http://www.letras.com.br/" + artista_ajustado)
        file = "artista_letra.txt"
        urllib.urlretrieve(artista_page, file)
        lista_artistas_links_complemento.append((artista_ajustado,) + tuple([pega_info_artista_3(file)]))
        print(artista_ajustado)
    except:
        pass

labels_df_artista_complemento_links = ["artista_ajustado", "lista_de_links_de_letras"]
df_artista_complemento_links = pd.DataFrame.from_records(lista_artistas_links_complemento, columns=labels_df_artista_complemento_links)

df_artista_complemento = pd.merge(df_artista_complemento, df_artista_complemento_links, on='artista_ajustado', how='outer')



# atualizando o data frame

df_artista = pd.merge(df_artista_1, df_artista_2, on='artista', how='outer')

# criando subdfs para rodar aos poucos
#df_artista_parte_1 = df_artista.iloc[:151]
#df_artista_parte_2 = df_artista.iloc[151:301]
#df_artista_parte_3 = df_artista.iloc[301:451]
#df_artista_parte_4 = df_artista.iloc[451:590]

# 7. Executa funcao de busca das cifras
lista_acordes = []
for index, row in df_artista.iterrows():
    artista = row["artista"]
    # count = 0
    for link in row["lista_de_links_de_musicas"]:
        #lista_acordes.append((artista,) + (link,) + tuple(pega_cifra(link)))
        try:
            lista_acordes.append(artista + "¬" + link + "¬" + str(pega_cifra(link)))
            # count = count+1
            print(artista + " - " + link)
        except:
            pass

lista_acordes_editada = [s.replace("http://www.cifras.com.br/cifra/", "") for s in lista_acordes]
lista_acordes_editada = [s.replace("http://www.cifras.com.br/tablatura/", "") for s in lista_acordes_editada]

df_cifras = pd.DataFrame({'lista_completa': lista_acordes_editada})
df_cifras = df_cifras['lista_completa'].str.split('¬', expand=True)
df_cifras.columns = ['artista', 'link', 'cifra','x', 'y', 'z']
df_cifras = df_cifras[df_cifras["x"].isnull()]
df_cifras = df_cifras[df_cifras["y"].isnull()]
df_cifras = df_cifras[df_cifras["z"].isnull()]
del df_cifras["x"]
del df_cifras["y"]
del df_cifras["z"]

df_cifras["nome_musica"] = df_cifras['link'].apply(lambda x: pd.Series(x.split('/')))[1]
df_cifras = df_cifras[df_cifras["nome_musica"] != ""]

#df_cifras.to_csv('df_cifras.csv', sep=';')


# 8. Juntando df_artista com df_cifras
df_artista_completo = pd.merge(df_artista, df_cifras, on='artista', how='outer')
df_artista_completo_pt1 = df_artista_completo.iloc[:9000]
df_artista_completo_pt2 = df_artista_completo.iloc[9000:18000]
df_artista_completo_pt3 = df_artista_completo.iloc[18000:27000]
df_artista_completo_pt4 = df_artista_completo.iloc[27000:36000]
df_artista_completo_pt5 = df_artista_completo.iloc[36000:44004]



# 9. Pegando letras
lista_letras = []

df_artista_letras_pt1 = df_artista_letras.iloc[:100]
df_artista_letras_pt2 = df_artista_letras.iloc[100:150]
df_artista_letras_pt3 = df_artista_letras.iloc[150:200]
df_artista_letras_pt4 = df_artista_letras.iloc[200:250]
df_artista_letras_pt5 = df_artista_letras.iloc[250:300]
df_artista_letras_pt6 = df_artista_letras.iloc[300:350]
df_artista_letras_pt7 = df_artista_letras.iloc[350:400]
df_artista_letras_pt8 = df_artista_letras.iloc[400:450]
df_artista_letras_pt9 = df_artista_letras.iloc[450:500]
df_artista_letras_pt10 = df_artista_letras.iloc[500:550]
df_artista_letras_pt11 = df_artista_letras.iloc[550:590]


for index, row in df_artista_letras_pt11.iterrows():
    artista = row["artista"]
    try:
        for link in row["lista_de_links_de_letras"]:
        #lista_acordes.append((artista,) + (link,) + tuple(pega_cifra(link)))
            try:
                lista_letras.append(artista + "¬" + link + "¬" + pega_letra(link)[1] + "¬" + pega_letra(link)[0])
                # count = count+1
                print(str(index) + artista + " - " + link)
            except:
                pass
    except:
        pass
    print(str(index) + "-" + artista)

# Complemento
for index, row in df_artista_complemento.iterrows():
    artista = row["artista"]
    try:
        for link in row["lista_de_links_de_letras"]:
        #lista_acordes.append((artista,) + (link,) + tuple(pega_cifra(link)))
            try:
                lista_letras.append(artista + "¬" + link + "¬" + pega_letra(link)[1] + "¬" + pega_letra(link)[0])
                # count = count+1
                print(str(index) + artista + " - " + link)
            except:
                pass
    except:
        pass
    print(str(index) + "-" + artista)


df_letras = pd.DataFrame({'lista_letras': lista_letras})
df_letras = df_letras['lista_letras'].str.split('¬', expand=True)
df_letras.columns = ['artista', 'nome_musica', 'compositor','letra']



# 10. Criando base de análise
#df_analise = df_artista_completo_letras
#del df_analise["lista_de_links_de_musicas"]
#del df_analise["qtde_musicas"]
#del df_analise["pos_ini"]
#del df_analise["pos_fim"]
#del df_analise["rank"]

# 10.1. Base de análise - cifras
df_analise_cifras = df_artista_completo
del df_analise_cifras["lista_de_links_de_musicas"]
del df_analise_cifras["qtde_musicas"]
del df_analise_cifras["pos_ini"]
del df_analise_cifras["pos_fim"]
del df_analise_cifras["rank"]

# 10.2. Base de análise - letras
df_analise_letras = pd.merge(df_letras, df_artista, on='artista', how='inner')
del df_analise_letras["lista_de_links_de_musicas"]
del df_analise_letras["qtde_musicas"]
del df_analise_letras["pos_ini"]
del df_analise_letras["pos_fim"]
del df_analise_letras["rank"]

df_analise_letras = pd.merge(df_analise_letras, df_analise_letras.groupby("artista", as_index = False).agg({"nome_musica": pd.Series.nunique}), on='artista', how='inner')






