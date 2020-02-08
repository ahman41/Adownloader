import requests
from findid import findid
from bs4 import BeautifulSoup
from qbittorrent import Client
import time
qb = Client('http://127.0.0.1:8080/')
qb.login('admin', 'adminadmin')
allepisodes =0
epiarray = []
dict = {}
add =0
n = 0
sourcecode="start"
name= input("Please enter show name: ")
q = input("Please choose the quality: \n 1- 1080 \n 2- 720 \n 3- 480 \nYour choice: ")
howmuch= int(input("Please enter the amount of episodes you want to download: "))
start = input("Please enter the episode number to start at: ")
if int(start) < 10:
    start = f"0{start}"
if q=='1':
    q="1080p"
elif q=='2':
    q="720p"
elif q=='3':
    q="480p"
#---FindId-----
x = findid(name)
while sourcecode!= "b'DONE'":
    allepisodes=0
    download=requests.get("https://horriblesubs.info/api.php?method=getshows&type=show&showid="+x[1]+"&nextid="+str(n))
    sourcecode= str(download.content)
    soup = BeautifulSoup(download.content, 'lxml')
    epinumber = soup.find_all("div", class_="rls-info-container")
    quality = soup.find_all("div", class_="link-" +q)
    n = n+1
    #--- Loop and store in array
    while allepisodes<len(epinumber):
        #epiarray.append(epinumber[allepisodes].get("id"))
        dwlink = quality[allepisodes].find('a').get('href')
        dict.update({epinumber[allepisodes].get("id"): dwlink})
        allepisodes = allepisodes+1

while howmuch > 0:
    try:
        download = dict[str(start)]
        print(f"Downloading episode number {start}")
        start = int(start)+1
        if int(start) < 10:
            start = f"0{start}"
        howmuch = howmuch-1
        qb.download_from_link(download)
    except:
        print(f"This anime consists only of {len(dict)} episodes")
        exit()

#---Get number of pages---

