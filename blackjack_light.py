from random import random
from kandinsky import *
from ion import keydown

VAL = (2,3,4,5,6,7,8,9,10,'V','D','R','A')
FIG = ((16,56,124,254,511,254,124,56,16),(56,56,56,471,511,471,16,56,511),
(16,56,124,254,511,511,443,56,511),(198,495,511,511,511,254,124,56,16))
R,N,B,V,L = (255,0,0), 3*(0,), 3*(255,), (80,130,50), (0,255,0)
COUL = (R,N,N,R)

NUM_KEYS = (48,42,43,44,36,37,38,30,31,32)

jeu = sorted(list(range(len(VAL)*len(COUL))), key = lambda x:random())

def get_VAL(c): return VAL[c%len(VAL)]

# def name(c): return str(get_VAL(c)) + " de " + ("Trefle", "Coeur", "Carreau", "Pique")[c//len(VAL)]

def advance():
  while not keydown(4): pass
  while keydown(4): pass

def get_num():
  fill_rect(190,140,10,18,B)
  num = ''
  while True:
    for k in NUM_KEYS:
      if keydown(k): 
        num += str(NUM_KEYS.index(k))
        draw_num(num)
        while keydown(k): pass
      elif keydown(17): 
        num = num[:-1]
        draw_num(num)
        while keydown(17): pass
      elif keydown(52):
        while keydown(52): pass
        if num: return int(num)

def draw_num(num): 
  fill_rect(190,140,250,18,V)
  full_str(190,140,txt=num if num else " ",bc=B)
  

def get_option(*nums):
  while True:
    for n in nums:
      if keydown(NUM_KEYS[n]): 
        while keydown(NUM_KEYS[n]): pass
        return n



def get_pseudo(): # Player.n
  pseudo = input("Entrez le pseudo du joueur "+str(Player.n)+" : ")
  if len(pseudo)>7: pseudo = pseudo[:7]

  return pseudo

class Player:
  n = 1
  def __init__(self,is_dealer,nj=None):
    self.is_dealer = is_dealer
    self.active_cards = []
    self.solde = 100
    if is_dealer: self.solde *= nj
    self.mise = 0
    self.points = 0
    self.pseudo = "Dealer" if is_dealer else get_pseudo()
    Player.n += 1
  


  def get_mise(self):
      active_pseudo(self.pseudo)
      full_str(120,20,txt="Veuillez rentrer")
      full_str(120,38,txt="votre mise.")
      full_str(120,120,txt="SOLDE : "+str(self.solde))
      full_str(120,140,txt="MISE : ")
      self.mise = get_num()
      while not 0<self.mise<=self.solde:
        if self.mise == 0: t_erreur(("Vous ne pouvez pas","miser 0 points."))
        else: t_erreur(("Vous n'avez pas","assez de points."))
        self.mise = get_num()


  def deal(self):
    for _ in range(2): self.add_card()


  def add_card(self):
    c = jeu.pop(0)
    self.active_cards.append(c)
    jeu.append(c)


  def do_round(self):
    active_pseudo(self.pseudo)

    j = sorted(map(get_VAL,self.active_cards), key=VAL.index)
    self.points = 0
    for card in j:
      if card in range(1,11): self.points += card
      elif card in VAL[9:12]: self.points += 10
      else:
        self.points += 1
        if self.points < 12: self.points += 10

    if not self.is_dealer:

      v = round(214-(14*len(self.active_cards)))
      for i, c in enumerate(self.active_cards):
        carte(v+i*28,160,c)
      s = str(self.points)
      draw_string(s,320-len(s)*10,204)
    
    else: 
      fill_rect(0,111,300,111,V)
      v = round(214-(14*len(self.active_cards)))
      for i, c in enumerate(self.active_cards):
        carte(v+i*28,17,c)
      
      s = str(self.points)
      draw_string(s,320-len(s)*10,204)
      advance()
    if self.points>21:
      bandeau(self.pseudo+" BUSTED",R)
      self.points = -1
      advance()
  
    elif self.points==21: 
      if len(self.active_cards)==2: 
        bandeau(self.pseudo+" BLACKJACK",L)
      advance()
    
    else:
      ajout = self.is_dealer and self.points<17
      if not self.is_dealer:
        full_str(120,110,txt="STAND <0>")
        full_str(120,130,txt="HIT <1>")
        ajout = get_option(0,1)
      if ajout:
        self.add_card()
        if self.is_dealer: 
          advance()
        self.do_round()
    fill_rect(108,85,250,222,V)


  def reset(self):
    self.mise = 0
    self.points = 0
    self.active_cards.clear()

def gnop(txt,bc): full_str(108,111,212,111,txt,bc=bc)

def bandeau(txt,bc): full_str(108,86,212,50,txt,bc=bc)

def carte(x,y,carte):
  coul = COUL[carte//13]
  full_str(x,y,25,45,str(VAL[carte%13]),N,B)
  for c in range(9):
    for l in range(9):
        if FIG[carte//13][l] >> c & 1: 
          set_pixel(x+2+c, y+2+l, coul)
          set_pixel(x+14+c, y+34+l, coul)

def dos(x,y):
  fill_rect(x,y,25,45,B)
  fill_rect(x+1,y+1,24,44,3*(80,))



def t_erreur(t):
  fill_rect(190,140,200,18,V)
  for i,text in enumerate(t):
    full_str(120,180+i*18,txt=text,fc=R)

# def fr1(x,y,w,h,color): fill_rect(x,y,w,h,color)

def full_str(x,y,w=None,h=18,txt='',fc=N,bc=V):
  if not type(txt)==str: txt=str(txt)
  if w==None: w = len(txt)*10
  if h<18: h=18
  # fr1(*[round(e) for e in (x,y,w,h)],color=bc)
  fill_rect(round(x),round(y),round(w),round(h),bc)
  draw_string(txt,round((2*x+w-len(txt)*10)/2),round(y+h/2-9),fc,bc)

def classement(lp):
  fill_rect(0,0,107,200,V)
  for i,p in enumerate(sorted(lp, key=lambda e: e.solde, reverse=True)):
    c0, c1 = V, L
    if not p.solde>0:
      fill_rect(0,i*48,107,42,R)
      c0, c1 = R, N
    draw_string(str(i+1)+"."+p.pseudo,4,4+i*48,N,c0)
    draw_string(str(p.solde),24,i*48+22,c1,c0)
  fill_rect(108,0,250,222,V)

def active_pseudo(pseudo): 
  full_str(0,202,107,20,pseudo)
  fill_rect(108,111,300,222,V)

def show_dealers_cards(cards):
  carte(186,17,cards[0])
  dos(214,17)





def manche(lp, dealer):
  valid_participants = [p for p in lp if p.solde]
  non_dealer = [p for p in valid_participants if not p.is_dealer]
  for p in non_dealer: p.get_mise()
  fill_rect(108,0,250,111,V)
  for p in valid_participants : p.deal()
  show_dealers_cards(dealer.active_cards)

  for p in valid_participants: p.do_round()


  fill_rect(108,0,250,222,V)
  full_str(108,0,106,28,txt="PERDANTS",bc=R)
  full_str(214,0,106,28,txt="GAGNANTS",bc=L)
  full_str(108,201,212,20,"SCORE A BATTRE : "+str(dealer.points))
  fill_rect(107,28,250,1,N)
  fill_rect(107,201,250,1,N)
  fill_rect(214,0,1,201,N)
  pos = [0,0]
  for p in non_dealer:
    c = int(p.points>dealer.points) # 0 / 1
    m = 2*c-1 # -1 / 1
    x = 110 + c*106
    y = 33 + pos[c]*57
    for i,t in enumerate(("- "+p.pseudo,"SCORE : "+str(p.points),"("+str(p.mise*m)+")")):
      draw_string(t,x,y+i*18,N,V)

    pos[c] += 1
    p.solde += p.mise*m
    dealer.solde -= p.mise*m
  advance()    

  for p in valid_participants: p.reset()
  classement(lp)






def run():
  fill_rect(0,0,320,222,V)
  full_str(0,93,320,txt="Entrez le nombre de joueurs :")
  full_str(0,111,320,txt="1 - 2 - 3")
  N_JOUEURS = get_option(1,2,3)
  lp = [Player(is_dealer=0) for _ in range(N_JOUEURS)] + [Player(is_dealer=True,nj=N_JOUEURS)]
 
  fill_rect(0,0,320,222,V) 
  classement(lp)
  fill_rect(107,0,1,222,N)
  fill_rect(0,201,107,1,N)
  for _ in range(5):
    if any([p.solde for p in lp if not p.is_dealer]) and lp[-1].solde>0: manche(lp,lp[-1])


run()