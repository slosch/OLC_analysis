import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

from scrapy import Spider






### data from Tageswertung
Datum = []    # Datum
Punkte = [] # Punkte
Name = []  # Name
km = []   # km
kmh = []    # km/h
fai = []    # fai-km (ab 2011)
Startplatz = []  # Startplatz
Club = []   # Club
Flugzeug = []  # Flugzeug
Start = []  # Start
Ende = []   # Ende
Info = []   # Info

### data from Fluginformation

## Flugweg: Lon, Lat, Alt, Time [UTC]
FW_Start_Lon = []
FW_Start_Lat = []
FW_Start_Alt = []
FW_Start_Time = []
# Flugweg WP1
# Flugweg WP2
# Flugweg WP3
# Flugweg WP4
# Flugweg WP5
# Flugweg Finish

## Statistik: s [km], % Kurbel, N Aufwinde, R/C [m/s], E, Vd [km/h]
# Statistik Leg1
# Statistik Leg2
# Statistik Leg3
# Statistik Leg4
# Statistik Leg5
# Statistik Leg6

## TopMeteo
# Wind FL130
# Wind FL 85
# Wind 3500ft
# Satbild

###
# Functions
###

def read_details(Info):
    detail_page = requests.get(Info)
    detail_soup = BeautifulSoup(detail_page.content, 'html.parser')
    detail_soup = detail_soup.find_all("div", class_="infobox content")
    print(detail_soup)

def fetch_dates(daily_soup):
    # Fetches all dates from the dropdown box
    # find all <option...> tags and reduce result to text only (strips tags)
    olc_date = [th.get_text() for th in
        daily_soup.find_all("option")]
    # remove the separators
    olc_date = [item for item in olc_date if item != "----------------"]

    # filter out the first 10 characters of each string in the list
    olc_date = [e[:10] for e in olc_date]
    return(olc_date)


def read_after_2010(daily_soup, d):
    for row in daily_soup.find_all("tr"):
        col = row.find_all("td")

        column_Datum = d
        Datum.append(column_Datum)

        column_Punkte = col[1].string.strip()
        Punkte.append(column_Punkte)

        column_Name = col[2].find("a").text
        Name.append(column_Name)

        column_km = col[4].string.strip()
        km.append(column_km)

        column_fai = col[5].string.strip()
        fai.append(column_fai)

        column_kmh = col[6].string.strip()
        kmh.append(column_kmh)

        if col[7].find("span", class_=None):
            column_Startplatz = col[7].find('span')['title']
        else:
            column_Startplatz = col[7].find("a").text
        Startplatz.append(column_Startplatz)

        if col[8].string.strip()[-3:] == "...":
            column_Club = col[8].get("title")
        else:
            column_Club = col[8].string.strip()
        Club.append(column_Club)

        if col[9].string.strip()[-3:] == "...":
            column_Flugzeug = col[9].get("title")
        else:
            column_Flugzeug = col[9].string.strip()
        Flugzeug.append(column_Flugzeug)

        column_Start = col[10].string.strip()
        Start.append(column_Start)

        column_Ende = col[11].string.strip()
        Ende.append(column_Ende)

        column_Info = col[12].find('a').get('href')
        column_Info = re.search("Id=\d+", column_Info)
        column_Info = column_Info.group(0)
        column_Info = "http://www.onlinecontest.org/olc-2.0/gliding/flightinfo.html?ds" + str(column_Info)
        Info.append(column_Info)
        read_details(column_Info)

def read_until_2010(daily_soup, d):
    for row in daily_soup.find_all("tr"):
        col = row.find_all("td")

        column_Datum = d
        Datum.append(column_Datum)

        column_Punkte = col[1].string.strip()
        Punkte.append(column_Punkte)

        column_Name = col[2].find("a").text
        Name.append(column_Name)

        column_km = col[4].string.strip()
        km.append(column_km)

        # Year until 2010 do not contain this value
        column_fai = ""
        fai.append(column_fai)

        column_kmh = col[5].string.strip()
        kmh.append(column_kmh)

        if col[6].find("span", class_=None):
            column_Startplatz = col[6].find('span')['title']
        else:
            column_Startplatz = col[6].find("a").text
        Startplatz.append(column_Startplatz)

        if col[7].string.strip()[-3:] == "...":
            column_Club = col[7].get("title")
        else:
            column_Club = col[7].string.strip()
        Club.append(column_Club)

        if col[8].string.strip()[-3:] == "...":
            column_Flugzeug = col[8].get("title")
        else:
            column_Flugzeug = col[8].string.strip()
        Flugzeug.append(column_Flugzeug)

        column_Start = col[9].string.strip()
        Start.append(column_Start)

        column_Ende = col[10].string.strip()
        Ende.append(column_Ende)

        column_Info = col[11].find('a').get('href')
        column_Info = re.search("Id=\d+", column_Info)
        column_Info = column_Info.group(0)
        column_Info = "http://www.onlinecontest.org/olc-2.0/gliding/flightinfo.html?ds" + str(column_Info)
        Info.append(column_Info)
        read_details(column_Info)

###
# Main
###

olc_raw_content = []

for y in range (2011, 2009, -1):

    print("scraping year " + str(y))
    if y > 2010:
        daily_page = requests.get("http://www.onlinecontest.org/olc-2.0/gliding/daily.html?sc=&st=olc&rt=olc&df=" + str(y) + "-04-09&c=ALPS&sp=" + str(y) + "&d-2348235-p=&paging=100000")
    else:
        daily_page = requests.get("http://www.onlinecontest.org/olc-2.0/gliding/daily.html?st=olc&rt=olc&c=C0&sc=&sp=" + str(y) + "&df=" + str(y) + "-04-09#p:0;")

    daily_soup = BeautifulSoup(daily_page.content, 'html.parser')

    olc_date = fetch_dates(daily_soup)

    index = 0

    for d in olc_date:

        if index == 5:
            index = 0
            break
        index = index + 1

        print("Looking at day " + d)
        if (y > 2010):
            olc_url = ("http://www.onlinecontest.org/olc-2.0/gliding/daily.html?sc=&st=olc&rt=olc&df=" + d + "&c=ALPS&sp=" + str(y) + "&d-2348235-p=&paging=100000")
        else:
            olc_url = ("http://www.onlinecontest.org/olc-2.0/gliding/daily.html?st=olc&rt=olc&c=C0&sc=&sp=" + str(y) + "&df=" + d + "#p:0;")


        daily_page = requests.get(olc_url)
        daily_soup = BeautifulSoup(daily_page.content, 'html.parser')
        daily_soup = daily_soup.find("tbody")

        if y > 2010:
            read_after_2010(daily_soup, d)
        else:
            read_until_2010(daily_soup, d)

columns = {"Datum": Datum,
        'Punkte': Punkte,
        'Name': Name,
        'km': km,
        'km/h': kmh,
        'fai-km': fai,
        'Startplatz': Startplatz,
        'Club': Club,
        'Flugzeug': Flugzeug,
        'Start': Start,
        'Ende': Ende,
        'Info': Info
           }


df = pd.DataFrame(columns)
# print(df)

df.to_csv("OLC.csv", sep='\t', index=False, header=True, columns=columns)

# def write_out_main_page():


