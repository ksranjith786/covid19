from flask import Flask, jsonify, render_template, request, make_response, redirect, url_for
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

# Get the Rate of Change values
def getRate(x, y):
    try:
        rate = round((x / y * 100), 3)
    except ZeroDivisionError as err:
        print('Exception caught: ', err.__class__)
        rate = 0
    
    return rate
# end getRate

# {"active":4486275,"activePerOneMillion":578.17,"affectedCountries":215,"cases":11841626,"casesPerOneMillion":1519,"critical":57952,
# "criticalPerOneMillion":7.47,"deaths":543433,"deathsPerOneMillion":69.7,"oneCasePerPeople":0,"oneDeathPerPeople":0,
# "oneTestPerPeople":0,"population":7759460558,"recovered":6811918,"recoveredPerOneMillion":877.89,"tests":257622036,
# "testsPerOneMillion":33201.02,"todayCases":108404,"todayDeaths":3293,"todayRecovered":174452,"updated":1594142967355}

@app.route('/country', methods = ["GET"])
def country():
    try:
        statusCode = 0
        data = dict()

        #country_name = request.form.get("country") # for POST
        countryName = request.args.get("country", default = '_WORLD_', type = str)
        
        if countryName == '_WORLD_':
            countryName = "Across World"
            statusCode, data = get_all()
        else:
            statusCode, data = get_country(countryName)

    except:
        return make_response('Unsupported request, probably with selected country name', statusCode)

    else:
        try:
            casesPerPopulationRate = getRate(data['cases'], data['population'])
            activeCasesRate = getRate(data['active'], data['cases'])
            recoveryRate = getRate(data['recovered'], data['cases'])
            deathRate = getRate(data['deaths'], data['cases'])

        except KeyError as err:
            return make_response('Error while retrieving data; ' + str(err.__class__.__qualname__) + '! Exception caught: ' + str(err), 500)

        except:
            return make_response('Unexpected Error', 500)

        else:    
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
    return redirect(url_for('country'))
# end all()

if __name__ == '__main__':
    app.run()
