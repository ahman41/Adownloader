def findid(name):
    import requests
    from bs4 import BeautifulSoup
    n=0
    from tkinter import messagebox
    num = 0
    name = name.split(" ")
    while n < len(name):
        try:
            x = x+"-"+name[n]
            n = n+1
        except NameError:
            x = name[n]
            n = n+1
    request = requests.get("https://horriblesubs.info/shows/"+x)
    content = request.content
    soup= BeautifulSoup(content,features="lxml")
    link= soup.find_all('script')
    try:
        x = link[num].get_text()
    except:
        messagebox.showerror("Error happened!", "Couldn't find this anime are you sure of the name ?")
        exit()
    while True:
        if "var hs_showid" in x:
            x = x.split("=")
            return(x)
            break
        else:
            try:
                num = num+1
                x =link[num].get_text()
            except:
                messagebox.showerror("Error happened!", "Couldn't find this anime are you sure of the name ?")
                x = 0
                return x
                break
                
