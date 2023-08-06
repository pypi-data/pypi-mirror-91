'''
this files purpose is to extract all live data from site
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
import json
import io


#color scheme
colorama.init()
BLUE = colorama.Fore.BLUE
GRAY = colorama.Fore.LIGHTBLACK_EX
RED = colorama.Fore.RED
GREEN = colorama.Fore.GREEN
YELLOW = colorama.Fore.YELLOW
RESET = colorama.Fore.RESET



def identify(url):
    r = urllib.request.urlopen(url)
    sockno = r.fileno()
    sock = socket.fromfd(sockno, socket.AF_INET, socket.SOCK_STREAM)
    socketinfo = sock.getpeername()
    return socketinfo

def extract(url, mykey):
    APIKEY = mykey
    results = urllib.request.urlopen(f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={url}/&key={APIKEY}'
        .format(url)).read().decode('utf-8')
    results_json = json.loads(results)
    with open('results.json', 'w') as file:
        json.dump(results_json, file)
    print(f'{BLUE}***site data transfered***{RESET}')
    
    