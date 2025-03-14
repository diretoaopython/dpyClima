import requests

"""
Para mais informações sobre como obter a chave, assista o vídeo abaixo
06 - Aprenda Python com Flet criando a conta da API OpenWeatherMap
https://youtu.be/GLqCFhPm-gU?si=xx5HVgchE888a_Ru
"""
apiKey = "digite sua chave"

def obterCoordPorNome(apiKey,cidade,pais,limite=1):
    """
    07 - Aprenda Python com Flet criando a função da API de Geocodificação OpenWeatherMap
    https://www.youtube.com/watch?v=CbACEn252Fs&list=PLi6TNT5J8PtXotYJBLypBTWoTW7OsXFP4&index=9

    Exemplo de como utilizar a função
    latitude,longitude = obterCoordPorNome(apiKey,"Goiânia", "BR")
    print(latitude,longitude)
    """
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={cidade},{pais}&limit={limite}&appid={apiKey}"
    requisicao = requests.get(url).json()
    return requisicao[0]["lat"],requisicao[0]["lon"]

def obterCoordPorIpUsuario():
    """
    08 - Aprenda Python com Flet criando a função para retornar o IP do usuário
    https://www.youtube.com/watch?v=EmkB5bZFWNY&list=PLi6TNT5J8PtXotYJBLypBTWoTW7OsXFP4&index=9

    Exemplo de como utilizar a função
    lat,lon = obterLocalPorIpUsuario()
    """
    url = f"https://ipinfo.io/"

    resposta = requests.get(url)

    requisicao = resposta.json()

    coordenadas = requisicao['loc'].split(',')
    latitude = coordenadas[0]
    longitude = coordenadas[1]

    cidade = requisicao.get('city', 'Cidade desconhecida')
    regiao = requisicao.get('Região', 'Cidade desconhecida')
    pais = requisicao.get('country', 'País desconhecido')

    return [latitude,longitude,cidade,regiao,pais]

def obterClimaPorNome(apiKey,cidade,pais):
    """
    09 - Aprenda Python com Flet criando a função para obter o clima atual usando a API OpenWeatherMap
    https://www.youtube.com/watch?v=tKFeLXq_IzQ&list=PLi6TNT5J8PtXotYJBLypBTWoTW7OsXFP4&index=10

    Exemplo de como usar a função
    requisicao = obterClimaPorNome(apiKey,"Goiânia","BR")
    print(requisicao)
    print("=======================================================")
    print(requisicao['weather'])
    print("=======================================================")
    print(requisicao['weather'][0])
    print("=======================================================")
    print(requisicao['weather'][0]['description'])
    """
    latitude, longitude = obterCoordPorNome(apiKey, cidade, pais)

    # Vídeo 09
    # url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={apiKey}"

    # Vídeo 11
    # https://www.youtube.com/watch?v=ZP2nXf1Ujtc&list=PLi6TNT5J8PtXotYJBLypBTWoTW7OsXFP4&index=12
    # Adicionado o parâmetro units, que define o formato do dado da temperatura
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&units=metric&appid={apiKey}"
    resposta = requests.get(url)
    return resposta.json()

def obterPrevisaoPorNome(apiKey,cidade,pais):
    """
    10 - Aprenda Python com Flet criando a função que retorna a previsão do do tempo
    https://www.youtube.com/watch?v=3CWzf50UjQ0&list=PLi6TNT5J8PtXotYJBLypBTWoTW7OsXFP4&index=11

    Exemplo de uso
    requisicao = obterPrevisaoPorNome(apiKey,"Goiânia", "BR")
    print(requisicao)
    """
    latitude, longitude = obterCoordPorNome(apiKey, cidade, pais)

    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&units=metric&appid={apiKey}"

    # Usando uma data específica (Api de previsão que pode ser usada se você tiver uma conta de estudante de uma universidade)
    # https://history.openweathermap.org/data/2.5/history/city?lat=41.85&lon=-87.65&appid={API key}
    # url = f"https://history.openweathermap.org/data/2.5/history/city?lat={latitude}&lon={longitude}&start=1732492800&end=1732881600&units=metric&appid={apiKey}"
    resposta = requests.get(url)
    return resposta.json()
