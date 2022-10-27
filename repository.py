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


def GetBigChart():
    url = "https://api.statbank.dk/v1/data/STRAF11/CSV?allowVariablesInHead=true&OMR%C3%85DE=101%2C147%2C155%2C185%2C165%2C151%2C153%2C157%2C159%2C161%2C163%2C167%2C169%2C183%2C173%2C175%2C187%2C201%2C240%2C210%2C250%2C190%2C270%2C260%2C217%2C219%2C223%2C230%2C400%2C411%2C085%2C253%2C259%2C350%2C265%2C269%2C320%2C376%2C316%2C326%2C360%2C370%2C306&OVERTR%C3%86D=*&TID=*"
    r = requests.get(url)
    csvStringIO = StringIO(r.text)
    df = pd.read_csv(csvStringIO, delimiter=";")
    return df



def CreateBigCSV():
    data = {}
    crime_str = "%2C".join(valuecodes.CRIME.values())
    base_url = "https://api.statbank.dk/v1/data/STRAF11/CSV?allowCodeOverrideInColumnNames=true&TID=*&OVERTR%C3%86D=" + crime_str
    num_of_municipalties = len(valuecodes.AREA.values())
    for i,k in enumerate(valuecodes.AREA.keys()):
        print(i, "out of ", len(num_of_municipalties))
        url = base_url + "&OMR%C3%85DE=" + valuecodes.AREA[k]
        r = requests.get(url)
        csvStringIO = StringIO(r.text)
        data[k] = pd.read_csv(csvStringIO, delimiter=";")
        if len(data[k]) > len(valuecodes.times)*len(valuecodes.CRIME):
            print(k)
    df = pd.concat(data.values(), axis=0, ignore_index=True)
    df.to_csv("data/crimes.csv", index=False)
    print(len(df))

def CreateBigSexyCSV():
    data = {}
    crime_str = "%2C".join(valuecodes.Sexual_crimes.values())
    base_url = "https://api.statbank.dk/v1/data/STRAF11/CSV?allowCodeOverrideInColumnNames=true&TID=*&OVERTR%C3%86D=" + crime_str
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
    df.to_csv("data/sex_crimes.csv", index=False)
    print(len(df))

def CreateSmallSexyCSV():
    data = {}
    crime_str = "%2C".join(valuecodes.Sexual_crimes.values())
    time_str = "%2C".join(valuecodes.time_from_2013.values())
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
    print(len(df))

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
    print(len(df))

def CreateSmallUmbrellaCrimeCSV():
    data = {}
    crime_str = "%2C".join(valuecodes.Umbrella_crime.values())
    time_str = "%2C".join(valuecodes.time_from_2013.values())
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
    df.to_csv("data/small_umbrella_terms_crimes.csv", index=False)
    print(len(df))

def CreateSmallUmbrellaCrimeFrom2020CSV():
    data = {}
    crime_str = "%2C".join(valuecodes.few_umbrella_crime.values())
    time_str = "%2C".join(valuecodes.time_2021.values())
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
    df.to_csv("data/small_few_umbrella_terms_crimes_2021.csv", index=False)
    print(len(df))


def CreateBigCSVMini():
    data = {}
    #crime_str = "%2C".join(valuecodes.CRIME.values())
    #base_url_json = "https://api.statbank.dk/v1/data/STRAF11/JSONSTAT?TID=2020K3%2C2020K4%2C2021K1%2C2021K2&OVERTR%C3%86D=1336%2C1120"
    base_url = "https://api.statbank.dk/v1/data/STRAF11/CSV?allowCodeOverrideInColumnNames=true&TID=2020K3%2C2020K4%2C2021K1%2C2021K2&OVERTR%C3%86D=1336%2C1120"
    print(valuecodes.AREA)
    for k in valuecodes.AREA.keys():
        url = base_url + "&OMR%C3%85DE=" + valuecodes.AREA[k]

        print(url)
        r = requests.get(url)
        csvStringIO = StringIO(r.text)
        data[k] = pd.read_csv(csvStringIO, delimiter=";")
        if len(data[k]) > len(valuecodes.times)*len(valuecodes.CRIME):
            print(k)
    df = pd.concat(data.values(), axis=0, ignore_index=True)
    df.to_json("data/mini_crimes.csv", index = False)
    print(len(df))



def CreateJsonMini():
    base_url_json = "https://api.statbank.dk/v1/data/STRAF11/JSONSTAT?TID=2020K3%2C2020K4%2C2021K1%2C2021K2&OVERTR%C3%86D=1336%2C1120"
    area_str = "%2C".join(valuecodes.AREA.values())
    url = base_url_json + "&OMR%C3%85DE=" + area_str

    r = requests.get(url)
    df = pd.read_json(r.text)
    df.to_json("data/mini_crimes.json")
    print(len(df))


def GetPopulations():
    baseUrl = "https://api.statbank.dk/v1/data/FOLK1A/CSV?allowCodeOverrideInColumnNames=true&Tid=*&OMR%C3%85DE="
    area_str = "%2C".join(valuecodes.AREA.values())
    url = baseUrl+ area_str
    r = requests.get(url)
    csvStringIO = StringIO(r.text)
    df = pd.read_csv(csvStringIO, delimiter=";")
    df.to_csv("data/populations.csv", index=False)


#CreateBigCSVMini()
#CreateJsonMini()
#CreateSmallSexyCSV()
#CreateSmallUmbrellaCrimeFrom2020CSV()
#print(len(valuecodes.AREA)*len(valuecodes.times)*len(valuecodes.CRIME))
