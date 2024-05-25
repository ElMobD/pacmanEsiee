import random
import tkinter as tk
from tkinter import font  as tkfont
import numpy as np
 

##########################################################################
#
#   Partie I : variables du jeu  -  placez votre code dans cette section
#
#########################################################################
 
# Plan du labyrinthe

# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

# transforme une liste de liste Python en TBL numpy équivalent à un tableau 2D en C
def CreateArray(L):
   T = np.array(L,dtype=np.int32)
   T = T.transpose()  ## ainsi, on peut écrire TBL[x][y]
   return T

TBL = CreateArray([
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,0,1,1,2,2,1,1,0,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,1,2,2,2,2,1,0,0,0,0,0,0,1],
        [1,0,1,0,1,1,0,1,1,1,1,1,1,0,1,1,0,1,0,1],
        [1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,0,1,0,1,1,1,1,1,1,0,1,0,1,1,0,1],
        [1,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1] ])
# attention, on utilise TBL[x][y] 
        
HAUTEUR = TBL.shape [1]      
LARGEUR = TBL.shape [0]  

# placements des pacgums et des fantomes

def PlacementsGUM():  # placements des pacgums
   GUM = np.zeros(TBL.shape,dtype=np.int32)
   
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 0):
            GUM[x][y] = 1

   GUM[1][1] = 2
   GUM[LARGEUR-2][1] = 2
   GUM[1][HAUTEUR-2] = 2
   GUM[LARGEUR-2][HAUTEUR-2] = 2


   return GUM
            
GUM = PlacementsGUM()   
   

      

PacManPos = [5,5]

Ghosts  = []
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "pink", (0,0)])
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "orange", (0,0)])
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "cyan", (0,0)])
Ghosts.append(  [LARGEUR//2, HAUTEUR // 2 ,  "red", (0,0)])         

#### Code ajouté

gameOver = False
pacManScore = 0
CDD = np.zeros(TBL.shape, dtype=np.int32) # carte des distances
CDDG = np.zeros(TBL.shape, dtype=np.int32) # carte des distances des fantômes
GHOST = np.zeros(TBL.shape, dtype=np.int32) # carte des positions des fantomes
grandeValeur = 1000
nbrCases = LARGEUR * HAUTEUR
directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
chase_mode = False
chase_time = 0

### CARTE DES DISTANCES
def distance():
    global CDD, grandeValeur, nbrCases

    for x in range(LARGEUR):
        for y in range(HAUTEUR):

            if TBL[x][y] == 1:
                CDD[x][y] = grandeValeur
            elif GUM[x][y] == 1 or GUM[x][y] == 2:
                CDD[x][y] = 0
            else:
                CDD[x][y] = nbrCases

    return CDD
### CARTE DES DISTANCES


### CARTE DES DISTANCES DES FANTÔMES
def distanceGhosts():
    global CDDG, GHOST

    GHOST = np.zeros(TBL.shape, dtype=np.int32)
    for G in Ghosts:
        GHOST[G[0]][G[1]] = 1

    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if GHOST[x][y] == 1:
                CDDG[x][y] = 0     
            elif TBL[x][y] == 1 or TBL[x][y] == 2:
                CDDG[x][y] = grandeValeur
            else:
                CDDG[x][y] = nbrCases
    return CDDG
### CARTE DES DISTANCES DES FANTÔMES

def updateDistance():
    global CDD, directions, grandeValeur, nbrCases

    isUpdated = True

    while isUpdated:
        isUpdated = False
        for x in range(1, LARGEUR-1):
            for y in range(1, HAUTEUR-1):
                if CDD[x][y] != grandeValeur:
                    neighbours = []
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < LARGEUR and 0 <= ny < HAUTEUR:
                            neighbours.append((nx, ny))

                    neighboursValue = []

                    for nx, ny in neighbours:
                        neighboursValue.append(CDD[nx][ny])

                    minValue = min(neighboursValue)

                    if CDD[x][y] > minValue + 1:
                        CDD[x][y] = minValue + 1
                        isUpdated = True
                        
                    #SetInfo1(x, y, CDD[x][y])

def updateDistanceGhosts():
    global CDDG, directions, grandeValeur
    isUpdated = True
    while isUpdated:
        isUpdated = False
        for x in range(1, LARGEUR-1):
            for y in range(1, HAUTEUR-1):
                if TBL[x][y] == 0:
                    neighbours = []
                    for dx, dy in directions:
                        nx = x + dx
                        ny = y + dy
                        if 0 <= nx < LARGEUR and 0 <= ny < HAUTEUR:
                            neighbours.append((nx, ny))

                    neighboursValue = []

                    for nx, ny in neighbours:
                        neighboursValue.append(CDDG[nx][ny])

                    minValue = min(neighboursValue)

                    if CDDG[x][y] > minValue + 1:
                        CDDG[x][y] = minValue + 1
                        isUpdated = True

                    SetInfo2(x, y, CDDG[x][y])

CDD = distance()
CDDG = distanceGhosts()


##############################################################################
#
#  Debug : ne pas toucher (affichage des valeurs autours dans les cases

LTBL = 100
TBL1 = [["" for i in range(LTBL)] for j in range(LTBL)]
TBL2 = [["" for i in range(LTBL)] for j in range(LTBL)]


# info peut etre une valeur / un string vide / un string...
def SetInfo1(x,y,info):
   info = str(info)
   if x < 0 : return
   if y < 0 : return
   if x >= LTBL : return
   if y >= LTBL : return
   TBL1[x][y] = info
   
def SetInfo2(x,y,info):
   info = str(info)
   if x < 0 : return
   if y < 0 : return
   if x >= LTBL : return
   if y >= LTBL : return
   TBL2[x][y] = info
   


##############################################################################
#
#   Partie II :  AFFICHAGE -- NE PAS MODIFIER  jusqu'à la prochaine section
#
##############################################################################

 

ZOOM = 40   # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels

screeenWidth = (LARGEUR+1) * ZOOM  
screenHeight = (HAUTEUR+2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth)+"x"+str(screenHeight))   # taille de la fenetre
Window.title("ESIEE - PACMAN")

# gestion de la pause

PAUSE_FLAG = False 

def keydown(e):
   global PAUSE_FLAG
   if e.char == ' ' : 
      PAUSE_FLAG = not PAUSE_FLAG 
 
Window.bind("<KeyPress>", keydown)
 

# création de la frame principale stockant plusieurs pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)


# gestion des différentes pages

ListePages  = {}
PageActive = 0

def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame

def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()
    
    
def WindowAnim():
    PlayOneTurn()
    Window.after(333,WindowAnim)

Window.after(100,WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas( Frame1, width = screeenWidth, height = screenHeight )
canvas.place(x=0,y=0)
canvas.configure(background='black')
 
 
#  FNT AFFICHAGE


def To(coord):
   return coord * ZOOM + ZOOM 
   
# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [ 5,10,15,10,5]


def Affiche(PacmanColor,message):
   global anim_bouche
   
   def CreateCircle(x,y,r,coul):
      canvas.create_oval(x-r,y-r,x+r,y+r, fill=coul, width  = 0)
   
   canvas.delete("all")
      
      
   # murs
   
   for x in range(LARGEUR-1):
      for y in range(HAUTEUR):
         if ( TBL[x][y] == 1 and TBL[x+1][y] == 1 ):
            xx = To(x)
            xxx = To(x+1)
            yy = To(y)
            canvas.create_line(xx,yy,xxx,yy,width = EPAISS,fill="blue")

   for x in range(LARGEUR):
      for y in range(HAUTEUR-1):
         if ( TBL[x][y] == 1 and TBL[x][y+1] == 1 ):
            xx = To(x) 
            yy = To(y)
            yyy = To(y+1)
            canvas.create_line(xx,yy,xx,yyy,width = EPAISS,fill="blue")
            
   # pacgum
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         if ( GUM[x][y] == 1):
            xx = To(x) 
            yy = To(y)
            e = 5
            canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="orange")
         elif ( GUM[x][y] == 2):
            xx = To(x) 
            yy = To(y)
            e = 6
            canvas.create_oval(xx-e,yy-e,xx+e,yy+e,fill="green")
            
   #extra info
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x) 
         yy = To(y) - 11
         txt = TBL1[x][y]
         canvas.create_text(xx,yy, text = txt, fill ="white", font=("Purisa", 8)) 
         
   #extra info 2
   for x in range(LARGEUR):
      for y in range(HAUTEUR):
         xx = To(x) + 10
         yy = To(y) 
         txt = TBL2[x][y]
         canvas.create_text(xx,yy, text = txt, fill ="yellow", font=("Purisa", 8)) 
         
  
   # dessine pacman
   xx = To(PacManPos[0]) 
   yy = To(PacManPos[1])
   e = 20
   anim_bouche = (anim_bouche+1)%len(animPacman)
   ouv_bouche = animPacman[anim_bouche] 
   tour = 360 - 2 * ouv_bouche
   canvas.create_oval(xx-e,yy-e, xx+e,yy+e, fill = PacmanColor)
   canvas.create_polygon(xx,yy,xx+e,yy+ouv_bouche,xx+e,yy-ouv_bouche, fill="black")  # bouche
   
  
   #dessine les fantomes
   dec = -3
   for P in Ghosts:
      xx = To(P[0]) 
      yy = To(P[1])
      e = 16
      
      coul = P[2]
      # corps du fantome
      CreateCircle(dec+xx,dec+yy-e+6,e,coul)
      canvas.create_rectangle(dec+xx-e,dec+yy-e,dec+xx+e+1,dec+yy+e, fill=coul, width  = 0)
      
      # oeil gauche
      CreateCircle(dec+xx-7,dec+yy-8,5,"white")
      CreateCircle(dec+xx-7,dec+yy-8,3,"black")
       
      # oeil droit
      CreateCircle(dec+xx+7,dec+yy-8,5,"white")
      CreateCircle(dec+xx+7,dec+yy-8,3,"black")
      
      dec += 3
      
   # texte  
   
   canvas.create_text(screeenWidth // 2, screenHeight- 50 , text = "PAUSE : PRESS SPACE", fill ="yellow", font = PoliceTexte)
   canvas.create_text(screeenWidth // 2, screenHeight- 20 , text = message, fill ="yellow", font = PoliceTexte)
   
 
AfficherPage(0)
            
#########################################################################
#
#  Partie III :   Gestion de partie   -   placez votre code dans cette section
#
#########################################################################
def PacmanEatGum():
    global pacManScore, nbrCases, CDD, chase_mode, chase_time
    if GUM[PacManPos[0]][PacManPos[1]] == 1 or GUM[PacManPos[0]][PacManPos[1]] == 2:  # si la pos du pacman est sur un pacgum
        pacgumEaten = GUM[PacManPos[0]][PacManPos[1]]
        GUM[PacManPos[0]][PacManPos[1]] = 0    # on enleve le pacgum
        CDD[PacManPos[0]][PacManPos[1]] = nbrCases
        if pacgumEaten == 1: pacManScore = pacManScore + 100
        else: 
            pacManScore = pacManScore + 200
            chase_mode = True
            chase_time = 16
    if chase_mode:
        for G in Ghosts:
            if chase_mode and (PacManPos[0] == G[0] and PacManPos[1] == G[1]):
                G[0] = LARGEUR // 2
                G[1] = HAUTEUR // 2
                pacManScore = pacManScore + 2000

    CDD = distance()
       

def Collision():
   global PacManPos, Ghosts, chase_mode
   for g in Ghosts:
      if not chase_mode and (PacManPos[0] == g[0] and PacManPos[1] == g[1]):
         return True
   return False

def PacManPossibleMove():
   L = []
   x,y = PacManPos
   if ( TBL[x  ][y-1] == 0 ): L.append((0,-1))
   if ( TBL[x  ][y+1] == 0 ): L.append((0, 1))
   if ( TBL[x+1][y  ] == 0 ): L.append(( 1,0))
   if ( TBL[x-1][y  ] == 0 ): L.append((-1,0))
   return L
   
def GhostsPossibleMove(x,y):
   L = []
   if ( TBL[x  ][y-1] == 2 or TBL[x][y-1] == 0): L.append((0,-1))
   if ( TBL[x  ][y+1] == 2 or TBL[x][y+1] == 0): L.append((0, 1))
   if ( TBL[x+1][y  ] == 2 or TBL[x+1][y] == 0): L.append(( 1,0))
   if ( TBL[x-1][y  ] == 2 or TBL[x-1][y] == 0): L.append((-1,0))
   return L
   
def IAPacman():
    global PacManPos, Ghosts, CDD, CDDG, nbrCases, chase_mode, chase_time

    #deplacement Pacman vers les pacgums
    L = PacManPossibleMove()
    min_distance = nbrCases
    next_move = None
    for move in L:
        new_x = PacManPos[0] + move[0]
        new_y = PacManPos[1] + move[1]
        if CDD[new_x][new_y] < min_distance:
            min_distance = CDD[new_x][new_y]
            next_move = move

    # si un fantôme est proche
    if CDDG[PacManPos[0]][PacManPos[1]] < 4: 
        next_move = None
        min_distance = CDDG[PacManPos[0]][PacManPos[1]]
        for move in L:
            new_x = PacManPos[0] + move[0]
            new_y = PacManPos[1] + move[1]
            if CDDG[new_x][new_y] > min_distance:
                min_distance = CDDG[new_x][new_y]
                next_move = move

    #print(chase_mode, chase_time)

    # si le mode chasse est activé
    if chase_time and chase_mode > 0: 
        chase_time -= 1
        next_move = None
        min_distance = CDDG[PacManPos[0]][PacManPos[1]]
        for move in L:
            new_x = PacManPos[0] + move[0]
            new_y = PacManPos[1] + move[1]
            if CDDG[new_x][new_y] < min_distance:
                min_distance = CDDG[new_x][new_y]
                next_move = move
    else:
        chase_mode = False

    if next_move: # Faire avancer le Pacman
        PacManPos[0] += next_move[0]
        PacManPos[1] += next_move[1]

    PacmanEatGum()
    updateDistance()
    return Collision()
 
   
def IAGhosts():
   #deplacement Fantome
   for F in Ghosts:
      x, y = F[0], F[1]
      dx, dy = F[3] # direction actuelle
      L = GhostsPossibleMove(x,y)
      # Si le fantôme est dans un couloir, continuer dans la direction actuelle
      if (dx, dy) in L and len(L) == 2:  # Le fantôme peut continuer et il est dans un couloir (2 directions possibles)
            new_dx, new_dy = dx, dy
      else:
            choix = random.randrange(len(L))
            new_dx = L[choix][0]
            new_dy = L[choix][1]
            

      # Mettre à jour la position et la direction
      F[0], F[1] = x + new_dx, y + new_dy
      F[3] = (new_dx, new_dy)
      
      distanceGhosts()
      updateDistanceGhosts()
   return Collision()
  
 

 
#  Boucle principale de votre jeu appelée toutes les 500ms

iteration = 0
def PlayOneTurn():
    global iteration, PAUSE_FLAG, pacManScore, gameOver, chase_mode
    
    if not PAUSE_FLAG and not gameOver: 
        iteration += 1
        if iteration % 2 == 0 :   
            if IAPacman() : gameOver = True
        else:                     
            if IAGhosts() : gameOver = True
    
    if chase_mode: color = "green"
    else : color = "yellow"

    Affiche(PacmanColor = color, message = "Score : "+str(pacManScore))  
    print("")
    print("")
 
###########################################:
#  demarrage de la fenetre - ne pas toucher

Window.mainloop()
