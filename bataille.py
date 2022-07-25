from random import random
from ion import keydown, KEY_OK
from time import sleep
from kandinsky import fill_rect, draw_string, set_pixel

R,N,B,V = (255,0,0), 3*(0,), 3*(255,), (80,130,50)
FIG = [[16,56,124,254,511,254,124,56,16],[56,56,56,471,511,471,16,56,511],
[16,56,124,254,511,511,443,56,511],[198,495,511,511,511,254,124,56,16]]
VAL = (2,3,4,5,6,7,8,9,10,'V','D','R','A')
COUL = [R,N,N,R]

def separeDeck(monDeck):
    moitierListe = len(monDeck)//2
    return [monDeck[:moitierListe], monDeck[moitierListe:]]

def valeur(c): return c%13

def milieu(l,t): return (l - 10*len(t)) // 2

def draw_noir_vert(txt,x,y): draw_string(txt,x,y,N,V)

def h(y): fill_rect(0,y,106,1,N)

def dos(x,y):
    fill_rect(x,y,25,45,3*(80,))
    fill_rect(x,y,25,1,B)
    fill_rect(x,y,1,45,B)

def carte(x, y, f, t, coul):
    fill_rect(x, y, 25, 45, B)
    for c in range(9):
        for l in range(9):
            if f[l] >> c & 1:
                set_pixel(x+2+c, y+2+l, coul)
                set_pixel(x+14+c, y+34+l, coul)
    draw_string(t,x+milieu(25,t),y+14,N,B) 

def manche(n_manche):
    txt = "MANCHE "+str(n_manche)
    draw_noir_vert(txt,milieu(106,txt),1)

def cartes_restantes(cr0,cr1):
    fill_rect(71,57,10,18,V)
    fill_rect(71,148,10,18,V)
    draw_noir_vert("×"+str(cr0),51,57)
    draw_noir_vert("×"+str(cr1),51,148)

l_decks = separeDeck(sorted(list(range(52)), key=lambda x:random()))
noms = ("CPU",input("Entrez votre pseudo ici : "))
compteurTour = 1
fill_rect(0,0,320,222,V)
draw_string("VS",43,102,R,V)
draw_noir_vert(noms[1],milieu(106,noms[1]),203)
fill_rect(106,0,1,320,N)
for hv in range(20,203,182): h(hv)
for dv1 in range(43,135,91): dos(26,dv1)
for dv2 in range(5,173,167): dos(290,dv2)

while all(l_decks) and compteurTour<300:

    manche(compteurTour)
    cartes_restantes(len(l_decks[0]),len(l_decks[1]))
    while not keydown(KEY_OK):
        pass
    sleep(.05)
    l_cartes = []
    
    for i in range(2):
        c = l_decks[i][0]
        l_cartes.append(c)
        carte(191,33+111*i,FIG[c//13], str(VAL[c%13]), COUL[c//13])
        l_decks[i].pop(0)

    draw_string(' '*20,110,102,N,V)

    txt_gagnant = "Gagnant : "
    if valeur(l_cartes[0])==valeur(l_cartes[1]):
        txt_gagnant = "Bataille !"
    else:
        gn = max((0,1), key=lambda x: valeur(l_cartes[x]))
        l_decks[gn] += l_cartes
        txt_gagnant += noms[gn]

    draw_string(txt_gagnant,106+milieu(213,txt_gagnant),102,N,V)
    compteurTour += 1

fill_rect(0,0,320,222,V)
t = noms[max((0,1), key=lambda x: len(l_decks[x]))]+" a gagne !!!"
draw_string(t,milieu(320,t),102,N,V)
