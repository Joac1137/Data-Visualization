import requests
from io import StringIO
import pandas as pd
import valuecodes



#r = requests.get("https://api.statbank.dk/v1/data/STRAF10/JSONSTAT?OVERTR%C3%86D=1289%2C3820&Tid=2021K1%2C2021K2%2C2021K3%2C2021K4%2C2022K1%2C2022K2")

#




def GetBarChartDf(area_str, time_str):
    time = valuecodes.times[time_str]
    area = valuecodes.AREA[area_str]
    crime = "%2C".join(valuecodes.CRIME.values())
    url = "https://api.statbank.dk/v1/data/STRAF11/CSV?allowVariablesInHead=true&" + "OVERTRÆD=" + crime + "&Tid=" + time + "&OMRÅDE=" + area
    r = requests.get(url)
    csvStringIO = StringIO(r.text)
    df = pd.read_csv(csvStringIO, delimiter=";")

    return df

print(GetBarChartDf("København", "2021K1"))