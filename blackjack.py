from random import random
from kandinsky import *
from ion import keydown

VAL = (2,3,4,5,6,7,8,9,10,'V','D','R','A')
R,N,B,V,L = (255,0,0),3*(0,),3*(255,),(80,130,50),(0,255,0)
NUM_KEYS = (48,42,43,44,36,37,38,30,31,32)
jeu = sorted(list(range(52)), key = lambda x:random())

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
      elif keydown(4):
        while keydown(4): pass
        if num: return int(num)
        else: return 0

def draw_num(num): 
  fill_rect(190,140,250,18,V)
  full_str(190,140,txt=num if num else " ",bc=B)
  
def get_option(*nums):
  while True:
    for n in nums:
      if keydown(NUM_KEYS[n]): 
        while keydown(NUM_KEYS[n]): pass
        return n

class Player:
  n = 1
  def __init__(self,is_dealer,nj=None):
    self.is_dealer = is_dealer
    self.active_cards = []
    self.solde = 100
    if is_dealer: 
      self.solde *= nj
      self.pseudo = "Dealer"
    else:
      self.pseudo = input("Entrez le pseudo du joueur "+str(Player.n)+" : ")
      if len(self.pseudo)>7: self.pseudo = self.pseudo[:7]
      Player.n += 1
    self.mise, self.points = 0, 0
    
  def active_pseudo(self):
    full_str(0,202,107,20,self.pseudo)
    fill_rect(108,111,300,222,V)

  def afficher_cartes(self,y):
    for i, c in enumerate(self.active_cards): carte(round(214-(14*len(self.active_cards)))+i*28,y,c)
    s = str(self.points)
    draw_string(s,320-len(s)*10,204)

  def add_card(self):
    c = jeu.pop(0)
    self.active_cards.append(c)
    jeu.append(c)

  def do_round(self):
    self.active_pseudo()
    while not len(self.active_cards)>1: self.add_card()
    j = sorted([VAL[c%len(VAL)] for c in self.active_cards], key=VAL.index)
    self.points = 0
    for card in j:
      if card in range(1,11): self.points += card
      elif card in VAL[9:12]: self.points += 10
      else:
        self.points += 1
        if self.points < 12: self.points += 10
    if self.is_dealer:
      fill_rect(108,0,300,222,V)
      self.afficher_cartes(17)
      advance()
    else: self.afficher_cartes(160)
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
        if self.is_dealer: advance()
        self.do_round()
    fill_rect(108,85,250,222,V)

def bandeau(txt,bc): full_str(108,86,212,50,txt,bc=bc)

def carte(x,y,carte):
  coul = (R,N,N,R)[carte//13]
  full_str(x,y,25,45,str(VAL[carte%13]),N,B)
  for c in range(9):
    for l in range(9):
        if ((16,56,124,254,511,254,124,56,16),(56,56,56,471,511,471,16,56,511),
(16,56,124,254,511,511,443,56,511),(198,495,511,511,511,254,124,56,16))[carte//13][l] >> c & 1: 
          set_pixel(x+2+c, y+2+l, coul)
          set_pixel(x+14+c, y+34+l, coul)

def t_erreur(t):
  fill_rect(190,140,200,18,V)
  for i,text in enumerate(t):
    full_str(120,180+i*18,txt=text,fc=R)

def full_str(x,y,w=None,h=18,txt='',fc=N,bc=V):
  if w==None: w = len(txt)*10
  if h<18: h=18
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

def run():
  fill_rect(0,0,320,222,V)
  full_str(0,93,320,txt="Entrez le nombre de joueurs :")
  full_str(0,111,320,txt="1 - 2 - 3")
  N_JOUEURS = get_option(1,2,3)
  dealer = Player(is_dealer=1,nj=N_JOUEURS)
  players = [Player(is_dealer=0) for _ in range(N_JOUEURS)]
  lp = players + [dealer]
  fill_rect(0,0,320,222,V) 
  classement(lp)
  fill_rect(107,0,1,222,N)
  fill_rect(0,201,107,1,N)
  while any([p.solde for p in players]) and dealer.solde>0: 
    valid_participants = [p for p in lp if p.solde]
    valid_players = valid_participants[:-1]
    for p in valid_players:
      p.active_pseudo()
      full_str(120,20,txt="Veuillez rentrer")
      full_str(120,38,txt="votre mise.")
      full_str(120,120,txt="SOLDE : "+str(p.solde))
      full_str(120,140,txt="MISE : ")
      p.mise = get_num()
      while not 0<p.mise<=p.solde:
        if p.mise == 0: t_erreur(("Vous ne pouvez pas","miser 0 points."))
        else: t_erreur(("Vous n'avez pas","assez de points."))
        p.mise = get_num()
    fill_rect(108,0,250,111,V)
    dealer.add_card()
    carte(186,17,dealer.active_cards[0])
    fill_rect(214,17,25,45,B)
    fill_rect(215,18,24,44,3*(80,))
    for p in valid_participants: p.do_round()
    fill_rect(108,0,250,222,V)
    full_str(108,0,106,28,txt="PERDANTS",bc=R)
    full_str(214,0,106,28,txt="GAGNANTS",bc=L)
    full_str(108,201,212,20,"SCORE A BATTRE : "+str(dealer.points))
    def h(y): fill_rect(107,y,250,1,N)
    h(28)
    h(201)
    fill_rect(214,0,1,201,N)
    pos = [0,0]
    for p in valid_players:
      c = int(p.points>dealer.points)
      m = 2*c-1
      for i,t in enumerate(("- "+p.pseudo,"SCORE : "+str(p.points),"("+str(p.mise*m)+")")):
        draw_string(t,110+c*106,(33+pos[c]*57)+i*18,N,V)
      pos[c] += 1
      p.solde += p.mise*m
      dealer.solde -= p.mise*m
    advance()    
    for p in valid_participants:
      p.mise,p.points = 0,0
      p.active_cards.clear()
    classement(lp)

run()