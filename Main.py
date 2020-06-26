import bs4
from requests import get

#Estou criando uma variavel chamada URL e apartir do request/get estou salvando tudo dentro de uma response
url = 'http://www.imdb.com/search/title?release_date=2017&sort=num_votes,desc&page=1'
response = get(url)

from bs4 import BeautifulSoup

# Usando o modulo do Python BeautifulSoup para analisar o conteúdo HTML e extrais os 50 divs
# o html.parser é um argumento que iremos usar para analisar o html
html_soup = BeautifulSoup(response.text, 'html.parser')

# Antes disso verificamos que os distingue dos outros elementos div na página. Geralmente, a principal diferença está no atributo class.. verificamps que class_='lister-item mode-advanced' tem exatamente o valor de 50, total de filmes.
movie_containers = html_soup.find_all('div', class_='lister-item mode-advanced')

# Utilizo os argumentos para achar o que eu quiser e ele me tras a primeira tag do primeiro filme ele ignora todas as outras
first_movie = movie_containers[0]

# Agora procuramos o ano do lançamento, entao descobrimos que esta na taf span
first_year = first_movie.h3.find('span', class_='lister-item-year text-muted unbold')
first_year = first_year.text

# Agora procuramos a avaliação do filme - localizado na tag <strong> e por sorte era o primeiro strong que contem a avaliacao
first_imdb = float(first_movie.strong.text)

# Agora procuramos o metascore - usei da mesma técnica que achei o ano
metascore = first_movie.find('span', class_='metascore favorable')
metascore = int(metascore.text)

# Agora iremos procurar o numero de votos - diferente do parametro class o "attrs" eu uso para nao precisar converter o text e tirar virgula, pois trata-se de um dicionario
first_votes = first_movie.find('span', attrs={'name':'nv'})
first_votes = int(first_votes['data-value'])

# Agora iremos testar um conteiner que nao tenha "Metascore"
twent_movie_mscore = movie_containers[21].find('div', class_='ratings-metascore')

print(first_movie.h3.a.text)
print(first_year)
print(first_imdb)
print(metascore)
print(first_votes)
print(type(twent_movie_mscore))

names = []
years = []
imdb_ratings = []
metascores = []
votes = []

# se o container nao possuir Metascore nao iremos pegar o filme
for container in movie_containers:
    # If the movie has Metascore, then extract:
    if container.find('div', class_='ratings-metascore') is not None:
        # The name
        name = container.h3.a.text
        names.append(name)

        # The year
        year = container.h3.find('span', class_='lister-item-year').text
        years.append(year)

        # The IMDB rating
        imdb = float(container.strong.text)
        imdb_ratings.append(imdb)

        # The Metascore
        m_score = container.find('span', class_='metascore').text
        metascores.append(int(m_score))

        # The number of votes
        vote = container.find('span', attrs={'name': 'nv'})['data-value']
        votes.append(int(vote))

print(names)