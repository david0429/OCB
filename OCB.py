import argparse
from yaml import load, dump
import json
import requests
import urllib.parse

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('CLIENTID')
parser.add_argument('CLIENTSECRET')

URL_MAIN = "https://api.untappd.com/v4"

def searchBrewery(name, CLIENTID, CLIENTSECRET):
    r_list = []
    url = URL_MAIN + "/search/brewery"
    url += "?client_id=" + CLIENTID + "&client_secret=" + CLIENTSECRET
    url += "&q=" + urllib.parse.quote(name)

    r = requests.get(url)
    data = r.json()

    for i in data["response"]["brewery"]["items"]:
        r_list.append({"Name": i["brewery"]["brewery_name"], "ID": i["brewery"]["brewery_id"]})

    return r_list

def main():
    args = parser.parse_args()

    inFile = open("breweries.yaml", 'r')
    data = load(inFile, Loader=Loader)
    inFile.close()

    for name, info in data.items():
        print(name)
        ut_brewery_search = searchBrewery(name, args.CLIENTID, args.CLIENTSECRET)
        if len(ut_brewery_search) == 1:
            print(ut_brewery_search[0]["ID"])
            data[name].update(ut_brewery_search[0])
        else:
            print(ut_brewery_search)

    outFile = open("breweries.yaml", 'w')
    outFile.write(dump(data, Dumper=Dumper))
    outFile.close()

main()
