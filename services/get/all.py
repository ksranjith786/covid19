import requests

ALL_URL='https://corona.lmao.ninja/v2/all'

def get_all():
    URL = ALL_URL
    r = requests.get(url = URL) #, params = PARAMS)
    data = r.json()

    return data
