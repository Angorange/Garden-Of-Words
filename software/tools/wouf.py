#wouf 2018 (py3.6.4)
#http://site2wouf.fr
#Pour créer dico.txt
#Qui contient un lexique basé sur
#ODS7
#En scollant le site : listesdemots.net
#requis :l beautifulsoup4 request html5lib
#(cmd : pip install beautifulsoup4)
#(cmd : pip install request)
#(cmd : pip install html5lib)
 
import requests
from bs4 import BeautifulSoup

filename = "../../data/lexique_fr.txt"
fichier = open(filename, "w")
 
#   Initialisation:
url="https://www.listesdemots.net/touslesmots"
requete = requests.get(str(url+".htm")) #page1
print(requete.url)
page = requete.content
 
soup = BeautifulSoup(page,features="html5lib")
span = soup.find("span", {"class": "mot"})
mots=span.string.strip()
lesmots=mots.split(" ")
for l in lesmots:
    fichier.write(l+"\n")
    print("|",end="")
print()
print("page 1 : OK ("+str(len(lesmots))+")")
totalmot=len(lesmots)

#page 2 à 8998:
for i in range(2,899):
    lurl=url+"page"+str(i)+".htm"
    ok=False
    while not ok:
        try:
            requete = requests.get(lurl,timeout=1)
            ok=True
        except:
            print("Problème de connexion. Je recommence !")
    print(requete.url)
    page = requete.content
    soup = BeautifulSoup(page,features="html5lib")
    span = soup.find("span", {"class": "mot"})
    mots=span.string.strip()
    lesmots=mots.split(" ")
    for l in lesmots:
        fichier.write(l+"\n")
        print("|",end="")
    totalmot+=len(lesmots)
    print()
    print("page "+str(i)+" : OK ("+str(len(lesmots))+"/"+str(totalmot)+")")
    
fichier.close()
#fin du script:
  
 
print("mots :",totalmot)