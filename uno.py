from tkinter import *
import random

#fonction MELANGER
def melanger(lst):
    """Mélanger les éléments d'une liste"""
    for inc in range(1,300):#300 fois
        i = random.randint(1,len(lst)-1)
        lst.append(lst.pop(i))

#fonction COULEUR
def couleur(carte):
    """Renvoie la variable 'color', couleur de la carte"""
    if 1 <= carte <= 25:
        crtcouleur = 'Rouge'
    elif 26 <= carte <= 50:
        crtcouleur = 'Bleu'
    elif 51 <= carte <= 75:
        crtcouleur = 'Vert'
    elif 76 <= carte <= 100:
        crtcouleur = 'Jaune'
    elif 101 <= carte <= 108:
        crtcouleur = ''
    return crtcouleur  #on retrouve les caractéristiques de la carte selon son code(de 1 à 108)

#fonction NUMERO
def numero(carte):
    """
    Donne le numero de la carte (ou son utilité pour les cartes spéciales)
    """

    liste = ['Rouge','Bleu','Vert','Jaune','']
    nbrindice = [0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12]
    #on retrouve les caractéristiques de la carte selon son code(de 1 à 108)
    if 101 <= carte <= 104:
       numero = '+4'
    elif 105 <= carte <= 108:   
        numero = 'Joker'
    elif 10 <= nbrindice[carte-(25*(liste.index(couleur(carte))))-1] <= 12:
        if nbrindice[carte-25*(liste.index(couleur(carte)))-1] == 10:
            numero = '+2'
        elif nbrindice[carte-25*(liste.index(couleur(carte)))-1] == 11:
            numero = '<=>'
        elif nbrindice[carte-25*(liste.index(couleur(carte)))-1] == 12:
            numero = 'Ø'
    elif 0 <= nbrindice[carte-(25*(liste.index(couleur(carte))))-1] <= 9:
        numero = nbrindice[carte-(25*(liste.index(couleur(carte))))-1]
    numero = str(numero)
    return numero

#fonction PIOCHE
def piochelst(lst,lst2):
    """Déplace un élément d'une liste à une autre"""
    lst2.append(lst.pop())

#fonction PIOCHE VIDE
def piochevide(lst,lst2):
    """La pile devient la pioche(on transfere les cartes)"""
    last = lst2.pop(0)
    melanger(lst2)
    for i in range(0,len(lst2)):
        lst.append(lst2[i])
    lst2 = []
    lst2.append(last)

#fonction ORDRE PIOCHER
def piocher(lst,lst2,lst3,n):
    """Execute la fonction pioche n fois"""
    for i in range(1,n+1):
        if len(lst)==0:
            piochevide(lst,lst3)
        piochelst(lst,lst2)

#fonction REGLE DU JEU (verification) 
def verification(lst,crtcouleur,crtnombre):
    """Vérifie si la carte est jouable"""
    i=0
    verif = False
    while i <= len(lst)-1 and verif == False:
        carte = lst[i]
        if numero(carte) == 'Joker' or numero(carte) == '+4':
            verif = True
        elif crtcouleur == couleur(carte):
            verif = True
        elif crtnombre == numero(carte):
            verif = True
        i+=1
    return verif

#fonction CARTES A PIOCHER
def jouepioche(lst,crtcouleur,crtnombre):
    """Renvoie le nombre de cartes à piocher au début du tour"""
    addcart = 0
    if crtnombre == "+4":
        addcart+=4
    elif crtnombre == "+2":
        addcart+=2
    if verification(lst,crtcouleur,crtnombre) == False:
        addcart+=1
    return addcart

#fonction SENS + PROCHAIN JOUEUR
def senstour(noms,indice,sens,symbole):
    """
        Renvoie l'indice du prochain joueur et le sens
    """
    #on vérifira que l'indice reste dans l'intervalle des joueurs définis
    if symbole == '<=>':
        if sens == -1:
            sens = 1
        elif sens == 1:
            sens = -1
    elif symbole =='Ø':
        indice+=sens
    if indice < 0:
        indice = len(noms)-1
    elif indice > len(noms)-1:
        indice = 0
    indice+=sens
    if indice < 0:
        indice = len(noms)-1
    elif indice > len(noms)-1:
        indice = 0
    return indice,sens

#fonction VICTOIRE
def victoire(lst):
    """
        Teste si le joueur a gagné
    """
    if len(lst) == 0:
        res = True
    else:
        res = False
    return res

#fonction affichage carte TKINTER
def carteTK(canvas,couleur,symbole,x,y,xdim,ydim):
    """
    Affichage de carte dans l'interface tkinter
    """
    lstcolor = ['Rouge','Bleu','Vert','Jaune','']
    colortk = ['#DF0101','#0404B4','#298A08','#F8D10A','#000000']
    itk = lstcolor.index(couleur)
    tkcolor = colortk[itk]  #détermine la couleur, transition vers le code couleur HTML
    rect = canvas.create_rectangle(x-xdim,y-ydim,x+xdim,y+ydim, fill = tkcolor,outline='#FFFFFF',activeoutline='#00FFFF',width=3) #création de la carte
    coord = canvas.coords(rect)
    canvas.create_text(x,y,text = symbole,fill='#FFFFFF',font=('Segoe UI Black','18'))  #imprime le symbole de la carte
    return coord #on renvoie les coordonnées pour pouvoir les réutiliser dans la fonction jouer TK

#fonction affichage main TKINTER
def mainTK(fen,lst):
    """
    Affichage de la main dans l'interface tkinter grâce à la fonction carteTK
    """
    x = -50
    y = 80
    cadreM=Frame(fen,width=780,height=160) #écran d'affichage de la main
    lstcadre.append(cadreM) #on garde en mémoire l'écran pour faciliter les manipulations
    cadreM.grid(row=2,column=0,columnspan=2)
    canvasmain=Canvas(cadreM,bg='#2E2E2E',width=780,height=160,scrollregion=(0,0,10+len(lst)*110,160))
    fondmain.append(canvasmain)
    for i in range(0,len(lst)):
            x += 110
            coords = carteTK(canvasmain,couleur(lst[i]),numero(lst[i]),x,y,50,70)
            lstcoords.append(coords)
    hbar=Scrollbar(cadreM,orient=HORIZONTAL,bg='#2E2E2E') #la barre de défilement pour l'affichage complet de la main
    lstscroll.append(hbar)
    hbar.pack(side=BOTTOM,fill=X)
    hbar.config(command=canvasmain.xview)
    canvasmain.config(width=780,height=160)
    canvasmain.config(xscrollcommand=hbar.set)
    canvasmain.pack(side=LEFT,expand=True,fill=BOTH)

#fonction sidebar joueur TKINTER
def sidebar(fen,lst,lst2,i,sens):
    """
    Affichage des prochains joueurs à jouer ainsi que leur nbr de cartes dans la main
    """
    cadreS=Frame(fen,width = 220,height=525)#écran d'affichage de la sidebar
    lstcadre.append(cadreS)
    cadreS.grid(row=0,column=2,rowspan=3)
    canvas=Canvas(cadreS,bg ='#A4A4A4',width=220,height=525)
    canvas.pack()
    x = 95
    y = 60
    c = 0
    lstsidebar = []
    ind     = i + sens
    canvas.create_text(x+15,y-40,text='Joueurs suivants',fill='#FFFFFF',font=('Segoe UI Light','22'))
    if ind == len(lst): 
        ind = 0
    elif ind < 0:
        ind = len(lst)-1
    while c != len(lst)-1:
        lstsidebar.append(lst[ind])#crée une nouvelle liste indépendante pour l'affichage des prochains joueurs
        c+=1
        ind += sens
        if ind == len(lst):
            ind = 0
        elif ind < 0:
            ind = len(lst)-1
    for nom in lstsidebar:
        canvas.create_text(x-80,y,anchor='w',text = nom,fill='#FFFFFF',font=('Segoe UI Light','16'),justify='left')
        canvas.create_rectangle(x+80,y-10,x+100,y+10,fill = 'red',outline='#FFFFFF')
        canvas.create_text(x+90,y-1,text = len(lst2[lst.index(nom)]),fill='#FFFFFF',font=('Segoe UI Light','14'))# on affiche
        y += 50

#fonction carte actuelle TKINTER (écran principal)
def affTK(fen,couleur,symbole,nom):
    """
    Affichage de l'écran principal contenant la carte actuelle, les message à l'utilisateur,etc...
    """
    cadreC=Frame(fen,width=780,height=340)#écran principal
    lstcadre.append(cadreC)
    cadreC.grid(row=0,column=0,rowspan=2,columnspan=2)
    canvas = Canvas(cadreC,bg='#FFFFFF',width=780,height=340)
    fondcarte.append(canvas)
    canvas.pack()
    canvas.create_text(15,40,anchor = "w",text ='Tour de',fill='#2E2E2E',font=('Segoe UI Light','19'))
    canvas.create_text(105,40,anchor = 'w',text = nom,fill='#DF0101',font=('Segoe UI Light','19'))
    carteTK(canvas,couleur,symbole,390,170,100,140) #carte active
#fonction choix carte TKINTER
def jouerTK(event):
    """
    Fonction a executé lorsque le joueur doit jouer
    """
    global color
    global symbol
    global mains
    global i
    global sens
    lstcadre[2].focus_set()
    decalagex,decalagey=lstscroll[0].get() #décalage du à la barre de défilement
    decalagex=decalagex*(10+len(mains[i])*110)
    coordx=decalagex+event.x #coordonnée du clic de l'utilisateur
    coordy=event.y
    valider = 0
    crt = 0
    while crt <= len(mains[i])-1:
        if (lstcoords[crt][0]<=coordx<=lstcoords[crt][2])and(lstcoords[crt][1]<=coordy<=lstcoords[crt][3]): # on teste si le clic est inclu dans une des cartes
            test = []
            test.append(mains[i][crt])
            if verification(test,color,symbol):#on teste ensuite si la carte est jouable
                carte = mains[i][crt]
                valider = 1
                while len(lstcoords)!=0:#on pense à réinitialiser la liste de coordonnées des cartes
                    lstcoords.pop(0)
                break
            elif verification(test,color,symbol)==False:
                break
        else:
            crt+=1
    if valider ==1:
        pile.append(carte)
        mains[i].remove(carte) #la carte choisie passe en active
        symbol=numero(carte)
        color = couleur(carte)
        carteTK(fondcarte[0],color,symbol,390,170,100,140)
        mainTK(fenetre[0],mains[i])
        if victoire(mains[i]):
            lstcadre[0].destroy()
            cadreC = Frame(fenetre[0],width = 780,height = 340)
            cadreC.grid(row=0,column=0,rowspan=2,columnspan=2)
            canvas = Canvas(cadreC,bg='#FFFFFF',width=780,height=340)
            canvas.pack()
            canvas.create_text(200,170,anchor = "w",text =players[i]+" a gagné!",fill='#000000',font=('Segoe UI Light','40'))# le joueur i a gagné
        elif 101 <= carte <= 108:
            rctrouge = fondcarte[0].create_rectangle(500,80,620,110,fill='red',outline='#FFFFFF',activeoutline='#00FFFF',width=2)
            rctbleu = fondcarte[0].create_rectangle(500,120,620,150,fill='blue',outline='#FFFFFF',activeoutline='#00FFFF',width=2)
            rctvert = fondcarte[0].create_rectangle(500,160,620,190,fill='green',outline='#FFFFFF',activeoutline='#00FFFF',width=2)
            rctjaune = fondcarte[0].create_rectangle(500,200,620,230,fill='yellow',outline='#FFFFFF',activeoutline='#00FFFF',width=2)
            fondcarte[0].bind('<Button-1>',jokercouleur)#choix de la nouvelle carte si joker ou +4
        else:
            color = couleur(carte)
            i,sens=senstour(players,i,sens,symbol)
            suivant = Button(lstcadre[0],text='Suivant',relief='flat',font=('Segoe UI Light','12'),bg='#FFFFFF',command=changement)#tour suivant
            lstbutton.append(suivant)
            suivant.place(x=720,y=300)
            #coordcouleur = [[500,80,620,110],[500,120,620,150],[500,160,620,190],[500,200,620,230]]
    if valider == 0:
        fondmain[0].bind('<Button-1>',jouerTK)# si le clic n'a pas abouti

#fonction choix couleur joker TKINTER
def jokercouleur(event):
    """
    Choix de la couleur dans le cas d'un joker ou d'un +4
    """
    global color
    global i
    global sens
    global symbol
    fondcarte[0].focus_set()
    coordcouleur = [[500,80,620,110],[500,120,620,150],[500,160,620,190],[500,200,620,230]]
    lstcouleur = ['Rouge','Bleu','Vert','Jaune']
    coordx=event.x
    coordy=event.y
    clr=0
    valider = 0
    while clr <= 3:
        if (coordcouleur[clr][0]<=coordx<=coordcouleur[clr][2])and(coordcouleur[clr][1]<=coordy<=coordcouleur[clr][3]):#comme pour le choix de la carte,on teste si le clic est valide
            color = lstcouleur[clr]
            carteTK(fondcarte[0],color,symbol,390,170,100,140)
            valider = 1
            break
        else:
            clr+=1
    if valider == 1:
        i,sens=senstour(players,i,sens,symbol)
        suivant = Button(lstcadre[0],text='Suivant',relief='flat',font=('Segoe UI Light','12'),bg='#FFFFFF',command=changement)# tour suivant
        lstbutton.append(suivant)
        suivant.place(x=720,y=300)
    
#fonction LANCER TKINTER
def lancer():
    """
    Déroulement d'un tour
    """

    global uno #parfois difficile d'importer des variables existantes dans tkinter donc on utilise global
    global i
    global sens
    global mains
    global pioche
    global pile
    global color
    global symbol
    while len(lstchangement)!=0:
        lstchangement[0].destroy()
        lstchangement.pop(0)
    fond.destroy()#on pense à réinitialiser à chaque tour tous les widgets TKINTER
    if uno == 0:
        choixcouleur = ['Rouge','Bleu','Vert','Jaune','']
        addcart=jouepioche(mains[i],color,symbol) #affichage de l'écran
        affTK(root,color,symbol,players[i])
        sidebar(root,players,mains,i,sens)
        if addcart > 0:
            piocher(pioche,mains[i],pile,addcart)
            msgpioche = "Vous avez pioché " +str(addcart) +" carte(s)." #message si l'utilisateur a pioché ce tour ci.
            labelpioche = Label(lstcadre[0],text=msgpioche,bg='#FFFFFF',font=('Segoe UI Light','16'))
            labelpioche.place(x=5,y=310)
        mainTK(root,mains[i])
        if verification(mains[i],color,symbol)==False:
            labeljouer = Label(lstcadre[0],bg='#FFFFFF',text="Vous ne pouvez pas jouer.",font=('Segoe UI Light','16')) #message si le joueur ne peut pas jouer.
            labeljouer.place(x=255,y=310)
            i+=sens
            if i < 0:
                i = len(players)-1
            elif i > len(players)-1:
                i = 0
            suivant = Button(lstcadre[0],text='Suivant',relief='flat',font=('Segoe UI Light','12'),bg='#FFFFFF',command = changement)#tour suivant
            lstbutton.append(suivant)
            suivant.place(x=720,y=300)
        elif verification(mains[i],color,symbol):
            fondmain[0].bind('<Button-1>',jouerTK)#choix de la carte
    
#fonction changement de joueur
def changement():
    """
    Ecran de transistion entre deux joueurs
    """
    global i
    global players
    while len(lstcoords)!=0:
        lstcoords.pop(0)
    while len(lstcadre)!=0:
        lstcadre[0].destroy()
        lstcadre.pop(0)
    while len(fondmain)!=0:
        fondmain[0].destroy()
        fondmain.pop(0)
    while len(fondcarte)!=0:
        fondcarte[0].destroy()
        fondcarte.pop(0)
    while len(lstscroll)!=0:
        lstscroll[0].destroy()
        lstscroll.pop(0)
    fond = Canvas(root,width = 1000,height = 528,bg ='#A4A4A4')
    lstchangement.append(fond)
    fond.pack()
    fond.create_text(15,40,anchor = "w",text ='Tour de',fill='#2E2E2E',font=('Segoe UI Light','19'))
    fond.create_text(105,40,anchor = 'w',text = players[i],fill='#DF0101',font=('Segoe UI Light','19'))
    jouer = Button(root,text = 'JOUER',bg ='#A4A4A4',fg='#FFFFFF',font=('Segoe UI Black','15'),width = 0,height = 1,command = lancer,justify='center',relief='flat',activeforeground='#1C1C1C')#premier tour
    lstbutton.append(jouer)
    jouer.place(x=465,y=230)
    
#initialisation tkinter

def nextplayer(event):
    """
    Initialisation de la partie via tkinter
    """
    touche = event.keysym
    if entree.get() in players:
        entree.delete(0,END)
    elif not(entree.get()=='stop'):
        if touche == "Return":
            players.append(entree.get())# on recupère le nom du joueur
            mains.append([])
            entree.delete(0,30)
    elif entree.get() == 'stop':
        entree.destroy()
        fond.delete(titre)
        fond.delete(instruction)
        for j in mains:
            piocher(pioche,j,pile,7)#<--changement nbr de carte
        piocher(pioche,pile,mains[0],1)
        cartespe = ['<=>','Ø','+2','Joker','+4']
        while numero(pile[0]) in cartespe: #si la première carte est une carte spéciale, on change de carte
            auxaux = pile.pop(0)
            pioche.insert(0,auxaux)
            piocher(pioche,pile,mains[0],1)
        global color
        global symbol
        color = couleur(pile[0])#on met en place les paramètres de la première carte
        symbol = numero(pile[0])
        fond.create_text(15,40,anchor = "w",text ='Tour de',fill='#2E2E2E',font=('Segoe UI Light','19'))
        fond.create_text(105,40,anchor = 'w',text = players[i],fill='#DF0101',font=('Segoe UI Light','19'))
        jouer = Button(root,text = 'JOUER',bg ='#A4A4A4',fg='#FFFFFF',font=('Segoe UI Black','15'),width = 0,height = 1,command = lancer,justify='center',relief='flat',activeforeground='#1C1C1C')#premier tour
        lstbutton.append(jouer)
        jouer.place(x=465,y=230)#bouton de lancement de la partie
    return touche

#UNO
root = Tk() #fenetre TKINTER du uno
root.geometry("1000x528+0+0")
lstbutton = []
lstcadre = []
fondmain = []
lstcoords = []
fenetre = [root]
fondcarte = []
lstscroll = []
lstchangement=[]
# les listes qui gardent en mémoire les widgets tkinter
#ci dessous les paramètres de bases
uno = 0
players = []
mains = []
i = 0
sens = 1
pioche = []
pile = []
color = ''
symbol = ''
for j in range (1,109): # on crée toutes les cartes
    pioche.append(j)
melanger(pioche)
#ci dessous la fenetre d'initialisation des joueurs
fond = Canvas(root,width = 1000,height = 528,bg ='#A4A4A4')
"""
txt = fond.create_text(295,315,text="Ajouter un joueur",font =('Arial','16'),fill='#FFFFFF')
"""
titre = fond.create_text(500,200,text="UNO",font=('Segoe UI Black','55','italic'),fill='#FFFFFF')
instruction = fond.create_text(860,500,text='Tapez stop pour commencer',font=('Segoe UI Light','16'),fill='#FFFFFF')
fond.pack()

entree = Entry(root,relief = 'flat',width=15,bg='#848484',bd=3,fg='#FFFFFF',font=('Segoe UI Light','16'),insertbackground='#FFFFFF',selectbackground='#FFFFFF',selectforeground='#A4A4A4',justify='center')
entree.place(x=414,y=275)
entree.insert(0,"Ajouter un joueur")
entree.bind('<Return>',nextplayer)

root.mainloop()#fenetre principale
