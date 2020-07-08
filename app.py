from flask import Flask, jsonify, render_template, request
import datetime
from os import environ

from services.get.all import get_all
from services.get.countries import get_country

app = Flask(__name__)
envFLASK = environ.get('FLASK_ENV')

if envFLASK == 'development':
    app.debug = True
else:
    app.debug = False

def getRateValues(data):
    casesPerPopulationRate = round((data['cases'] / data['population'] * 100), 3)
    activeCasesRate = round((data['active'] / data['cases'] * 100), 3)
    recoveryRate = round((data['recovered'] / data['cases'] * 100), 3)
    deathRate = round((data['deaths'] / data['cases'] * 100), 3)

    return casesPerPopulationRate, activeCasesRate, recoveryRate, deathRate
# end getRateValues

# {"active":4486275,"activePerOneMillion":578.17,"affectedCountries":215,"cases":11841626,"casesPerOneMillion":1519,"critical":57952,
# "criticalPerOneMillion":7.47,"deaths":543433,"deathsPerOneMillion":69.7,"oneCasePerPeople":0,"oneDeathPerPeople":0,
# "oneTestPerPeople":0,"population":7759460558,"recovered":6811918,"recoveredPerOneMillion":877.89,"tests":257622036,
# "testsPerOneMillion":33201.02,"todayCases":108404,"todayDeaths":3293,"todayRecovered":174452,"updated":1594142967355}

@app.route('/country', methods = ["GET"])
def country():
    #country_name = request.form.get("country") # for POST
    countryName = request.args.get("country", default = 'India', type = str)
    data = get_country(countryName)
    casesPerPopulationRate, activeCasesRate, recoveryRate, deathRate = getRateValues(data)
    #print(data)
    return render_template('index.html', countryName=countryName, cases=data['cases'], todayCases=data['todayCases'], deaths=data['deaths'],
                todayDeaths=data['todayDeaths'], recovered=data['recovered'], todayRecovered=data['todayRecovered'], active=data['active'],
                critical=data['critical'], population=data['population'],
                casesPerPopulationRate=casesPerPopulationRate,  activeCasesRate=activeCasesRate, recoveryRate=recoveryRate, deathRate=deathRate,
                casesPerOneMillion=data['casesPerOneMillion'], deathsPerOneMillion=data['deathsPerOneMillion'], recoveredPerOneMillion=data['recoveredPerOneMillion'],
                activePerOneMillion=data['activePerOneMillion'], criticalPerOneMillion=data['criticalPerOneMillion'], testsPerOneMillion=data['testsPerOneMillion'])
# end country()

@app.route('/')
@app.route('/all')
def all():
    data = get_all()
    casesPerPopulationRate, activeCasesRate, recoveryRate, deathRate = getRateValues(data)
    #print(data)
    return render_template('index.html', countryName="Across World", cases=data['cases'], todayCases=data['todayCases'], deaths=data['deaths'],
                todayDeaths=data['todayDeaths'], recovered=data['recovered'], todayRecovered=data['todayRecovered'], active=data['active'],
                critical=data['critical'], population=data['population'],
                casesPerPopulationRate=casesPerPopulationRate,  activeCasesRate=activeCasesRate, recoveryRate=recoveryRate, deathRate=deathRate,
                casesPerOneMillion=data['casesPerOneMillion'], deathsPerOneMillion=data['deathsPerOneMillion'], recoveredPerOneMillion=data['recoveredPerOneMillion'],
                activePerOneMillion=data['activePerOneMillion'], criticalPerOneMillion=data['criticalPerOneMillion'], testsPerOneMillion=data['testsPerOneMillion'])
# end all()

if __name__ == '__main__':
    app.run()
