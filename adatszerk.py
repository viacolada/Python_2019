import turtle
import datetime
import math
class Ora:
    def __init__(self):
        self.nap=None
        self.kezdo=None
        self.veg=None
        self.neve=None
        self.epulete=None
        self.emelete=None
        
def ora_epulete(adatok):
    epulet=adatok[4]
    epulet=epulet[:2]# mert legfeljebb 3 betűs lehet az épület neve
    epulet_betu=""
    for x in epulet:
        if x=='V':
            epulet_betu=epulet_betu+epulet[1:3]
        elif x.isalpha():
            epulet_betu=epulet_betu+x
    return epulet_betu

def ora_emelete(tanora):
    emelet=tanora[4]
    emelet=emelet[1:]
    emelet_szam=""
    for y in emelet:
        if y=='V':
            emelet_szam=emelet[2:]
        if y.isdigit():
            emelet_szam=emelet_szam+y
            emelet_szam=emelet_szam[0]
    return emelet_szam
        
def beolvas(fajlnev, nap):
    adatok=[]
    osszesora=[]
    f = open(fajlnev, "rt")
    for x in f:
        adatok=x.split(', ')
        ora=Ora()
        ora.nap=adatok[0]
        ora.kezdo=adatok[1]
        ora.veg=adatok[2]
        ora.neve=adatok[3]
        ora.epulete=ora_epulete(adatok)
        ora.emelete=ora_emelete(adatok)
        if ora.nap==nap:
            osszesora.append(ora)
    return osszesora
#*****************************************************
class Epulet:
    def __init__(self):
        self.neve=None
        self.vegpont=None
        self.x=None
        self.y=None
        self.vegpontok=[]
        self.csomopontok=[]

def terkep():
    f = open("epuletek.txt", "rt")
    epulet=[]
    epuletek=[]
    for x in f:
        epulet=x.split("\t")
        ep=Epulet()
        ep.neve=epulet[0]
        ep.vegpont=epulet[1]
        ep.x=int(epulet[2])
        ep.y=int(epulet[3])
        ep.vegpontok=epulet[4].split(", ")
        ep.csomopontok=epulet[5].split(', ')
        epuletek.append(ep)
    return epuletek
#**************************************************
def melyik_nap(nap):
    nap=nap-1
    if nap==0:
        return 'hetfo'
    elif nap==1:
        return 'kedd'
    elif nap==2:
        return 'szerda'
    elif nap==3:
        return 'csutortok'
    elif nap==4:
        return 'pentek'
#**************************************************

def kiindulas(x,y):
    f=open('BME_terkep.png')
    screen = turtle.Screen()
    screen.setup(1414,490)
    screen.bgpic('BME_terkep.png')
    screen.update()
    turtle.color("cyan")
    turtle.pensize(4)
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()

def beallit(terem):
    print(terem)
    kiindulas(melyik_koordinata(terem)[0], melyik_koordinata(terem)[1])

def oda (terem): #betű alapján megtalálja a helyet
    print('hova?',terem)
    for tp in range(0, len(terkep())):
        if terkep()[tp].neve==terem:
            turtle.speed(1)
            turtle.goto(terkep()[tp].x, terkep()[tp].y)
def melyik_epulet(x,y):
    for tp in range (0, len(terkep())):
        if x==terkep()[tp].x:
            if y==terkep()[tp].y:
                return terkep()[tp].neve
            
def melyik_koordinata(neve):
    koord=[]
    for tp in range (0, len(terkep())):
        if neve==terkep()[tp].neve:
            koord=terkep()[tp].x,terkep()[tp].y
    return list(koord)

def vektor_hossza(startpont, celpont):
    #print(startpont, celpont)
    startx=startpont[0]
    starty=startpont[1]
    celx=celpont[0]
    cely=celpont[1]
    tavolsag=math.sqrt(((celx-startx)**2) + ((cely-starty)**2))
    return tavolsag

def navigal(termek): #megkapja a kiválasztott nap óráinak listáját
    kiindulas = termek[0]#az első óra alapján beállítja a teknőc kiindulási pontját és visszatér az első óra épületének betűjével
    beallit(termek[0])
    for tm in range(0, len(termek)-1): #minden aznapi terem esetében
        kozelit(termek[tm], termek[tm+1]) #majd meghívja azt a függvényt, ami ezt a helyet közelíti a célhoz
                #print(kiindulas) #ez meg csak random check

def kozelit (kiindulo, celja):
    print ('--currenct step:',kiindulo,'to:',celja)
    ott_van=False 
    vegpontok=[]
    for tp in range (0, len(terkep())):
        if kiindulo == terkep()[tp].neve:
            vegpontok = terkep()[tp].vegpontok #rögzíti egy listában azokat a kiindulóponthoz tartozó pontokat, amelyek CSAK végpontot jelölnek (magyarul azoknak az épületeknek a nevét, amikbe egyenes út vezet onnan és nem halad belőle tovább)
    for v in range(0, len(vegpontok)):
        if celja == vegpontok[v]: #ha a cél egyezik ezek közül valamelyikkel, akkor megvagyunk
            ott_van=True
            oda(vegpontok[v]) #és odavezéreljük a legrövidebb úton abba a pontba a teknőcöt
    if vektor(celja, kiindulo) == celja:
        oda(celja)
        ott_van=True
    if not ott_van: #ha nem, akkor meg meghívjuk azt a függvényt, ami megkeresi nekünk a legrövidebbet
        oda(vektor(celja, kiindulo))
        kozelit(vektor(celja, kiindulo),celja)
        
def vektor(celja, kiindulo): #csak azt a a két pontot nézzük, ahol közlekedni kell
    csomopontok=[] #ez fogja tartalmazni azoknak a pontoknak a nevét, amikből indul elágazás máshova és kapcsolatban áll a kiindulási ponttal
    celjaxy=melyik_koordinata(celja) #az épület neve alapján megkeresi a cél épület koordinátáit 
    startxy=melyik_koordinata(kiindulo) # a kiindulási pont koordinátája
     #ez pedig a csomópontok közül annak a pontnak a koordinátája, ami a legközelebb visz a célhoz azon a szakaszon
    for tp in range (0, len(terkep())):
        if kiindulo == terkep()[tp].neve: #ha a kiindulási pont neve megegyezik a térképen valamelyik nevével
            csomopontok = terkep()[tp].csomopontok #rögzítjük azokat a pontokat, amikbe közvetlenül vezet út belőlük
    for csp in range(0, len(csomopontok)):
        for tp in range (0, len (terkep())):
            if csomopontok[csp]==terkep()[tp].neve: #a csomópontokat egyenként megkeressük a térkép adatai között
                reszxy=melyik_koordinata(terkep()[tp].neve) #és a hozzájuk tartozó koordinátát is külön rögzítjük
                if vektor_hossza(startxy, celjaxy) > vektor_hossza(reszxy, celjaxy): #ennek a koordinátának a távolságát összehasonlítjuk a kiindulási pont távolságával és ha kisebb, 
                    startxy=reszxy
    return melyik_epulet(startxy[0],startxy[1])
            
def main():
    nap=int(input("Melyik nap orarendjet szeretned kivalasztani? 1=hetfo, 2=kedd, 3=szerda, 4=csutortok, 5=pentek"))
    termek = []
    for x in range(0, len(beolvas("orarend.txt",melyik_nap(nap)))):
        termek.append(beolvas("orarend.txt",melyik_nap(nap))[x].epulete) #ezek az aznapi termek
    navigal(termek)
    
main()
        
