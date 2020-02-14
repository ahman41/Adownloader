import requests, os, sys
from tkinter import *
from tkinter import messagebox
from findid import findid
from bs4 import BeautifulSoup
from qbittorrent import Client
window = Tk()
window.title("Anime downloader")
try:
    qb = Client('http://127.0.0.1:8080/')
    qb.login('admin', 'adminadmin')
except:
    messagebox.showerror("Error happened!", "couldn't connect to qbitorrent do you have it installed and launched with the web ui ?")
    exit()
allepisodes =0
epiarray = []
dict = {}
add =0
n = 0
name = StringVar()
aq= StringVar()
astart = IntVar()
ahowmuch = StringVar()
def downloader():
    l1.delete(0,END)
    allepisodes =0
    epiarray = []
    dict = {}
    howmuch = int(ahowmuch.get())
    q = aq.get()
    start = astart.get()
    add = 0
    n = 0
    sourcecode="start"
    if start < 10:
        start = f"0{start}"
    if int(start) == 0:
        start = "01"
    #---FindId-----
    x = findid(name.get())
    while sourcecode!= "b'DONE'":
        if x == 0:
            return
        allepisodes = 0
        download=requests.get("https://horriblesubs.info/api.php?method=getshows&type=show&showid="+x[1]+"&nextid="+str(n))
        sourcecode= str(download.content)
        soup = BeautifulSoup(download.content, 'lxml')
        epinumber = soup.find_all("div", class_="rls-info-container")
        quality = soup.find_all("div", class_="link-" +q)
        n = n+1
        #--- Loop and store in array
        while allepisodes<len(epinumber):
            dwlink = quality[allepisodes].find('a').get('href')
            dict.update({epinumber[allepisodes].get("id"): dwlink})
            allepisodes = allepisodes+1
    #download only that amount of episodes
    if howmuch == 0:
        howmuch = len(dict)
        start = list(dict.keys())[howmuch-1]
    while howmuch > 0:
        try:
            download = dict[str(start)]
            #print(f"Downloading episode number {start}")
            l1.insert(END, f"Downloading episode number {start}")
            start = int(start)+1
            if int(start) < 10:
                start = f"0{start}"
            howmuch = howmuch-1
            qb.download_from_link(download)
        except KeyError:
            diclist = list(dict.values())
            dicnumberlist = list(dict.keys())
            download = diclist[-int(start)]
            #print(f"Downloading episode number {dicnumberlist[-int(start)]}")
            l1.insert(END, f"Downloading episode number {dicnumberlist[-int(start)]}")
            start = int(start)+1
            if int(start) < 10:
                start = f"0{start}"
            howmuch = howmuch-1
            qb.download_from_link(download)
        '''except :
            print(sys.exc_info()[0])
            print(f"This anime consists only of {len(dict)} episodes")
            exit()'''
    del q
    del howmuch
    del start
t1 = Label(window,text = "Anime's name").grid(row= 1, column=1  )
e1=Entry(window,textvariable=name).grid(row=1 , column=2  )
t2 = Label(window,text = "Episode to start at").grid(row= 2, column= 1 )
e2=Entry(window,textvariable=astart).grid(row= 2, column= 2 )
t3 = Label(window,text = "No. of episodes to download").grid(row=3 , column= 1 )
e2=Entry(window,textvariable=ahowmuch).grid(row= 3, column= 2 )
R1 = Radiobutton(window, text="1080p", variable=aq, value="1080p").grid(row=5 , column=2, sticky = N)
R2 = Radiobutton(window, text="720p", variable=aq, value="720p").grid(row=5 , column=2)
R3 = Radiobutton(window, text="480p", variable=aq, value="480p").grid(row=5 , column=2, sticky = S )
l1 = Listbox(window, width = 50)
l1.grid(row=5 , column=1  )
b1 = Button(window, text = "Start download",command=downloader).grid(row=6 , column=1  )
window.mainloop()
