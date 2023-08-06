'''
this files purpose is to export all info on the site
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

#color scheme
colorama.init()
BLUE = colorama.Fore.BLUE
GRAY = colorama.Fore.LIGHTBLACK_EX
RED = colorama.Fore.RED
GREEN = colorama.Fore.GREEN
YELLOW = colorama.Fore.YELLOW
RESET = colorama.Fore.RESET

def statuscode(url):
    r = requests.get(url)
    status = r.status_code
    st = str(status)
    if st[0] == '2':
        color = GREEN
        print(f"{color}[!] Status Code: SUCCESS {status}{RESET}")
    elif st[0] == '3':
        color = YELLOW
        print(f"{color}[!] Status Code: REDIRECTION {status}{RESET}")
    elif st[0] == '4' or '5':
        color = RED
        print(f"{color}[!] Status Code: ERROR {status}{RESET}")
    else:
        color = GRAY
        print(f"{color}[!] Status Code: UNKNOWN {status}{RESET}")
def encoding(url):
    r = requests.get(url)
    print(f"{BLUE}[!] Encoding: {r.encoding}{RESET}")

def cookies(url):
    r = requests.get(url)
    cookiejar = str(r.cookies)
    cookies = 0
    cookiejar = cookiejar.split()
    for i in range(len(cookiejar)):
        if '<' in cookiejar[i]:
            cookies += 1
    print(f"{BLUE}[!] amount of cookies: {cookies}{RESET}")

def ipandport(url):
    r = urllib.request.urlopen(url)
    mysockno = r.fileno()
    mysock = socket.fromfd(mysockno, socket.AF_INET, socket.SOCK_STREAM)
    (ip, port) = mysock.getpeername()
    print(f'{GREEN}[*] ip: {ip}\n[*] port: {port}{RESET}')   
    return mysock.getpeername()

def header(url):
    r = requests.get(url)
    head = r.request.headers
    print(f"{BLUE}[!] Header: {head}{RESET}")

def siteinfo(url):
    statuscode(url)
    encoding(url)
    cookies(url)
    header(url)
    ipandport(url)

