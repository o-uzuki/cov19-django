import sys
import csv

#dataroot = '/jobs/jhu-cov19/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/'
dataroot = './cov19diff/datas/'

def readDaily(day):
    with open(dataroot + day + '.csv', newline='', encoding='utf-8') as csvfile:
        datas = dict()
        reader = csv.DictReader(csvfile)
        for row in reader:
            cr = row['Country_Region']
            if cr not in datas:
                datas[cr] = {'Confirmed': 0, 'Deaths': 0,'Recovered': 0}
            #datas[cr]['Confirmed'] = datas[cr]['Confirmed'] + row['Confirmed']
            data = datas[cr]
            data['Confirmed'] = data['Confirmed'] + int(row['Confirmed'])
            data['Deaths'] = data['Deaths'] + int(row['Deaths'])
            data['Recovered'] = data['Recovered'] + int(row['Recovered'])

        return datas
