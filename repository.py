import requests


r = requests.get("https://api.statbank.dk/v1/data/STRAF10/JSONSTAT?OVERTR%C3%86D=1289%2C3820&Tid=2021K1%2C2021K2%2C2021K3%2C2021K4%2C2022K1%2C2022K2")

print(r.json())
