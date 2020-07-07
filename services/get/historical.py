import requests

HISTORICAL_URL = 'https://corona.lmao.ninja/v2/historical'

def get_historical(country=""):
    if country != '':
        URL = HISTORICAL_URL + "/" + country
    else:
        URL = HISTORICAL_URL
    
    r = requests.get(url = URL) #, params = PARAMS)
    data = r.json()
    
    return data
