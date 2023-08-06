'''
this files purpose is to find the geographic location of a web server
'''
#!/usr/local/bin/python3
import os
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import ssl
import sys
import colorama 
from urllib.parse import urlparse, urljoin
import socket
import urllib
import siteinfo as urlinfo
import sitemapping as urlmapping
import json
import re
import geopy
from geopy.geocoders import Nominatim


#color scheme
colorama.init()
BLUE = colorama.Fore.BLUE
GRAY = colorama.Fore.LIGHTBLACK_EX
RED = colorama.Fore.RED
GREEN = colorama.Fore.GREEN
YELLOW = colorama.Fore.YELLOW
RESET = colorama.Fore.RESET

def payload(url):
    load = list()
    newload = list()
    ip, port = urlinfo.ipandport(url)
    agent = urljoin('https://whatismyipaddress.com/ip/', ip)
    #use Mozilla user-agent to bypass bot-detection
    r = (requests.get(agent, headers={'User-Agent': 'Mozilla/5.0'}))
    soup = BeautifulSoup(r.text, 'html.parser')
    for i in soup.select('td'):
        load.append(i.getText())
    loadlen = len(load)
    for i in range(loadlen):
        i -= 1
        if load[i] == '':
            load.remove(load[i])
    for i in range(loadlen):
        if i == 11 or i == 12:
            newload.append(load[i])
    ne, lat = newload[0].split('\n')
    newlat, old = lat.split('\xa0\xa0')
    ne, long = newload[1].split('\n')
    newlong, old = long.split('\xa0\xa0')
    coordinates = (newlat + ',' +  newlong)
    locator = Nominatim(user_agent='myGeocoder')
    location = locator.reverse(coordinates)
    print(f'{BLUE}{location}{RESET}') 




