from flask import Flask, jsonify, render_template, request
from services.get.all import get_all
from services.get.countries import get_country
import datetime

app = Flask(__name__)
app.debug = True

@app.route('/country', methods = ["POST"])
def country():
    country_name = request.form.get("country")
    if country_name == None:
        country_name = 'India'
    countryName = country_name
    data = get_country(country_name)
    #print(data)
    return render_template('index.html', countryName=countryName, cases=data['cases'], todayCases=data['todayCases'], deaths=data['deaths'], todayDeaths=data['todayDeaths'], recovered=data['recovered'], todayRecovered=data['todayRecovered'], active=data['active'])

@app.route('/')
@app.route('/all')
def all():
    # {"active":4486275,"activePerOneMillion":578.17,"affectedCountries":215,"cases":11841626,"casesPerOneMillion":1519,"critical":57952,
    # "criticalPerOneMillion":7.47,"deaths":543433,"deathsPerOneMillion":69.7,"oneCasePerPeople":0,"oneDeathPerPeople":0,
    # "oneTestPerPeople":0,"population":7759460558,"recovered":6811918,"recoveredPerOneMillion":877.89,"tests":257622036,
    # "testsPerOneMillion":33201.02,"todayCases":108404,"todayDeaths":3293,"todayRecovered":174452,"updated":1594142967355}
    data = get_all()
    #print(data)
    return render_template('index.html', cases=data['cases'], todayCases=data['todayCases'], deaths=data['deaths'], todayDeaths=data['todayDeaths'], recovered=data['recovered'], todayRecovered=data['todayRecovered'], active=data['active'])
if __name__ == '__main__':
    app.run()
