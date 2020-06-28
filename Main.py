from requests import get
import pandas as pd
from time import sleep, time
from random import randint
from IPython.core.display import clear_output
from bs4 import BeautifulSoup
from warnings import warn

headers = {"Accept-Language": "en-US, en;q=0.5"}

# Estou criando uma variavel chamada URL e apartir do request/get estou salvando tudo dentro de uma response
url = 'http://www.imdb.com/search/title?release_date=2017&sort=num_votes,desc&page=1'
response = get(url)

# Declarando as listas que iremos armazenar os dados dos filmes.
#names = []
#years = []
#imdb_ratings = []
#metascores = []
#votes = []


# Usando o modulo do Python BeautifulSoup para analisar o conteúdo HTML e extrais os 50 divs
# o html.parser é um argumento que iremos usar para analisar o html
html_soup = BeautifulSoup(response.text, 'html.parser')

# Antes disso verificamos que os distingue dos outros elementos div na página. Geralmente, a principal diferença está no atributo class.. verificamps que class_='lister-item mode-advanced' tem exatamente o valor de 50, total de filmes.
# aqui somente encontrei na pagina que " class_='lister-item mode-advanced')" é o que separa os 50 filmes ... ele é o inicio e o fim
movie_containers = html_soup.find_all('div', class_='lister-item mode-advanced')

# Utilizo os argumentos para achar o que eu quiser e ele me tras a primeira tag do primeiro filme ele ignora todas as outras
first_movie = movie_containers[0]

# Agora procuramos o ano do lançamento, entao descobrimos que esta na tag span
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

#print(first_year)
#print(first_imdb)
#print(metascore)
#print(first_votes)
#print(type(twent_movie_mscore))


# se o container nao possuir Metascore nao iremos pegar o filme
# Abaixo foi so um teste com um conteiner apenas

#for container in movie_containers:
    # If the movie has Metascore, then extract:
    #if container.find('div', class_='ratings-metascore') is not None:
        # The name
        #name = container.h3.a.text
        #names.append(name)

        # The year
        #year = container.h3.find('span', class_='lister-item-year').text
        #years.append(year)

        # The IMDB rating
        #imdb = float(container.strong.text)
        #imdb_ratings.append(imdb)

        # The Metascore
        #m_score = container.find('span', class_='metascore').text
        #metascores.append(int(m_score))

        # The number of votes
        #vote = container.find('span', attrs={'name': 'nv'})['data-value']
        #votes.append(int(vote))

# Aqui usamos o panda para organizar os dados
#test_df = pd.DataFrame({'movie': names,
                      # 'year': years,
                     #  'imdb': imdb_ratings,
                      # 'metascore': metascores,
                     #  'votes': votes})
#print(test_df.info())
#print(test_df)



# Criado duas listas para fazermos um teste de monitoramente, considerando o quantidade de paginas a serem lidas.
# Realizando uma amostra com apenas 4 paginas
# Monitoramento

pages = [str(i) for i in range(1, 5)]
years_url = [str(i) for i in range(2000, 2018)]

start_time = time()
requests = 0

for _ in range(5):
    # A request would go here
    requests += 1
    sleep(randint(1, 3))# simula um usuario
    elapsed_time = time() - start_time
    clear_output(wait=True)
    #print(time(), 'time')
    #print(start_time,'tempo inicial, start time')
    #print(elapsed_time)
    print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    #warn("Warning Simulation")





# Redeclaring the lists to store data in
names = []
years = []
imdb_ratings = []
metascores = []
votes = []
# Preparing the monitoring of the loop
start_time = time()
requests = 0
# For every year in the interval 2000-2017
for year_url in years_url:
    # For every page in the interval 1-4
    for page in pages:
        # Make a get request
        response = get('http://www.imdb.com/search/title?release_date=' + year_url +
                       '&sort=num_votes,desc&page=' + page, headers=headers)
        # Pause the loop
        sleep(randint(8, 15))

        # Monitor the requests
        requests += 1
        elapsed_time = time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests / elapsed_time))
        clear_output(wait=True)

        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))

        # Break the loop if the number of requests is greater than expected
        if requests > 72:
            warn('Number of requests was greater than expected.')
            break

            # Parse the content of the request with BeautifulSoup
        page_html = BeautifulSoup(response.text, 'html.parser')

        # Select all the 50 movie containers from a single page
        mv_containers = page_html.find_all('div', class_='lister-item mode-advanced')

        # For every movie of these 50
        for container in mv_containers:
            # If the movie has a Metascore, then:
            if container.find('div', class_='ratings-metascore') is not None:
                # Scrape the name
                name = container.h3.a.text
                names.append(name)

                # Scrape the year
                year = container.h3.find('span', class_='lister-item-year').text
                years.append(year)
                # Scrape the IMDB rating
                imdb = float(container.strong.text)
                imdb_ratings.append(imdb)
                # Scrape the Metascore
                m_score = container.find('span', class_='metascore').text
                metascores.append(int(m_score))
                # Scrape the number of votes
                vote = container.find('span', attrs={'name': 'nv'})['data-value']
                votes.append(int(vote))

movie_ratings = pd.DataFrame({'movie': names,
                              'year': years,
                              'imdb': imdb_ratings,
                              'metascore': metascores,
                              'votes': votes})
print(movie_ratings.info())
movie_ratings.head(10)