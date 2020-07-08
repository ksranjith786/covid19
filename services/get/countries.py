import requests

COUNTRY_URL='https://corona.lmao.ninja/v2/countries'

def get_country(country=""):
    if country != '':
      URL = COUNTRY_URL + "/" + country
    else:
      URL = COUNTRY_URL

    # print(URL)
    r = requests.get(url = URL) #, params = PARAMS)
    
    if r.status_code != 200:
        raise Exception

    return r.status_code, r.json()
