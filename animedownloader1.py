import requests
from findid import findid
from bs4 import BeautifulSoup
from qbittorrent import Client
import time
qb = Client('http://127.0.0.1:8080/')
qb.login('admin', 'adminadmin')
num = 0
n = 0
nd=-1
name= input("Please enter show name: ")
q = input("Please choose the quality: \n 1- 1080 \n 2- 720 \n 3- 480 \nYour choice: ")
howmuch= input("Please enter the amount of episodes you want to download: ")
start = input("Please enter the episode number to start at: ")
start = int(start)
if q=='1':
    q="1080p"
elif q=='2':
    q="720p"
elif q=='3':
    q="480p"
n=0
#---FindId-----
x = findid(name)
download=requests.get("https://horriblesubs.info/api.php?method=getshows&type=show&showid="+x[1]+"&nextid="+str(nd))
downloads = str(download.content)
#---Get number of pages---
while downloads != "b'DONE'":
    nd = nd+1
    download=requests.get("https://horriblesubs.info/api.php?method=getshows&type=show&showid="+x[1]+"&nextid="+str(nd))
    downloads = str(download.content)
while nd >=0:
    if int(start) != 0:
        if int(start)<=2:
            nd = (nd-(int(start)/12))
        else: 
            nd = (nd-(int(start)/12))-1
            if nd < 0:
                nd = -nd
        nd = int(nd)
        print(nd)
    download=requests.get("https://horriblesubs.info/api.php?method=getshows&type=show&showid="+x[1]+"&nextid="+str(nd))
    downloads = str(download.content)
    if n == 0 and int(start) != 0:
        inc = (int(start)%12)-2
        if inc < 0:
            inc = -inc
        inc = int(inc)
        print(inc)
        start =0
    elif n ==0 and int(start) == 0:
        inc = 0
    else :
        inc = 1
    nd = nd-1
    soup = BeautifulSoup(download.content, "lxml")
    episode= soup.find_all("div", class_="link-"+q)
    number = soup.find_all("a",class_="rls-label")
    while inc < len(episode):
        if n == int(howmuch):
            print("Done!")
            exit()
        torrent = episode[-inc].find("span",class_="hs-magnet-link")
        number1= number[-inc].get_text().split("S")
        n = n+1
        torrent = torrent.find('a')
        print(f"Magnet link for your {number1[0]} Episode: ")
        #torrents = qb.download_from_link(torrent.get('href'))
        inc = inc+1
        if inc == len(episode) :
            inc = 0
            torrent = episode[0].find("span",class_="hs-magnet-link")
            number1= number[0].get_text().split("S")
            torrent = torrent.find('a')
            #torrents = qb.download_from_link(torrent.get('href'))
            print(f"Magnet link for your {number1[0]} Episode: ")
            break
    
