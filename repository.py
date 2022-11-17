import requests
from io import StringIO
import pandas as pd
import valuecodes


def CreateUmbrellaCrimeCSV():
    data = {}
    crime_str = "%2C".join(valuecodes.Umbrella_crime.values())
    time_str = "%2C".join(valuecodes.times.values())
    base_url = "https://api.statbank.dk/v1/data/STRAF11/CSV?allowCodeOverrideInColumnNames=true&TID=" + time_str + "&OVERTR%C3%86D=" + crime_str
    num_of_municipalties = len(valuecodes.AREA.values())
    for i,k in enumerate(valuecodes.AREA.keys()):
        print(i, "out of ", num_of_municipalties)
        url = base_url + "&OMR%C3%85DE=" + valuecodes.AREA[k]
        r = requests.get(url)
        csvStringIO = StringIO(r.text)
        data[k] = pd.read_csv(csvStringIO, delimiter=";")
        if len(data[k]) > len(valuecodes.times)*len(valuecodes.CRIME):
            print(k)
    df = pd.concat(data.values(), axis=0, ignore_index=True)
    df.to_csv("data/umbrella_terms_crimes.csv", index=False)
    return df


def GetPopulations():
    baseUrl = "https://api.statbank.dk/v1/data/FOLK1A/CSV?allowCodeOverrideInColumnNames=true&Tid=*&OMR%C3%85DE="
    area_str = "%2C".join(valuecodes.AREA.values())
    url = baseUrl+ area_str
    r = requests.get(url)
    csvStringIO = StringIO(r.text)
    df = pd.read_csv(csvStringIO, delimiter=";")
    df.to_csv("data/populations.csv", index=False)

