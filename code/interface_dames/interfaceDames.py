#! /usr/bin/env python
# -*- coding:Utf-8 -*-

import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os
from dames.partie import Partie
import Ai.AiControl as Ai
from dames.exceptions import *
from dames.exceptions import PositionSourceInvalide, PositionCibleInvalide, ProblemeChargement, ProblemeSauvegarde


class InterfaceDamier(tk.Frame):
    """
    Classe permettant l'affichage d'un damier. À modifier!
    @author: Bryan Oakley, Camille Besse, Jean-Francis Roy
    """

    def __init__(self, parent, taille_case,damier):
        """taille_case est la taille d'un côté d'une case en pixels."""
        # Definition du damier : # de cases
        self.n_lignes = 8
        self.n_colonnes = 8

        # Definition du damier : taille des cases (en pixels)
        self.taille_case = taille_case

        # Definition du damier : couleur de cases
        self.couleur1 = "white"
        self.couleur2 = "gray"

        # Pièces sur le damier
        self.damier = damier

        # Calcul de la taille du dessin
        canvas_width = self.n_colonnes * self.taille_case
        canvas_height = self.n_lignes * self.taille_case

        # Initialisation de la fenêtre parent contenant le canvas
        tk.Frame.__init__(self, parent)
        
        
        # Initialisation du canvas
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0, width=canvas_width, height=canvas_height,
                               background="white")

        # On place le canvas et le plateau (self) à l'aide de "grid".
        self.canvas.grid(padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W) #redim la fenetre 
        self.grid(padx=4, pady=4, sticky=tk.N + tk.S + tk.E + tk.W) # redim le plateau

        # Fait en sorte que le redimensionnement de la fenêtre redimensionne le damier
        self.canvas.bind("<Configure>", self.actualiser)
        
    

    def ajouter_piece(self, position, piece):
        """
        Ajoute une pièce sur le damier.
        """

        tempfont = ('Helvetica', self.taille_case//2)
        #piece_unicode = caracteres_unicode_pieces[nom_piece[0:2]]

        # On "dessine" la pièce
        ligne, colonne = position
        nom_piece = piece.nom
        self.canvas.create_text(ligne, colonne, text=piece, tags=(nom_piece, "piece"), font=tempfont)
        
        # On place la pièce dans le canvas (appel de placer_piece)
        self.placer_piece((ligne, colonne), nom_piece)


    def placer_piece(self, position, nom_piece):
        """
        Place une pièce à la position donnée (ligne, colonne).
        """
        #tk.messagebox.showinfo("wow",self.canvas.itemcget(nom_piece, 'text')) 
        ligne, colonne = position

        # Placer les pieces au centre des cases.
        x = (colonne * self.taille_case) + int(self.taille_case / 2)
        y = (ligne * self.taille_case) + int(self.taille_case / 2)

        # On change la taille de la police d'écriture selon la taille actuelle des cases.
        tempfont = ('Helvetica', self.taille_case//2)
        self.canvas.itemconfigure(nom_piece, font=tempfont)
        self.canvas.coords(nom_piece, x, y)
    
    def selectCase(self, position, color):
        """
        Selection de la case (afficher d'une manière graphique la case selectionné)
        """
        x1 = position[0] * self.taille_case
        x2 = x1+self.taille_case
        y1 = position[1]*self.taille_case
        y2 = y1+self.taille_case
        if color == "yellow":
            self.canvas.delete("selected")
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="selected")
        # on met les pièces au dessus de la selection de case
        self.canvas.tag_raise("piece")

    def ActualiserPieces(self,Create,new):
        """ On redessine les pieces"""
        if new:
            self.damier.initialiser_damier_par_default()
        if Create:
            self.canvas.delete("piece")
            for position, piece in self.damier.cases.items():
                self.ajouter_piece(position, piece)
        else:
            for position, piece in self.damier.cases.items():
                self.placer_piece(position, piece.nom)

        # On mets les pieces au dessus des cases
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("case")    

    def actualiser(self, event):
        """
        Redessine le damier lorsque la fenetre est redimensionnée.
        """
        
        # Calcul de la nouvelle taille du damier
        x_size = int((event.width - 1) / self.n_colonnes)
        y_size = int((event.height - 1) / self.n_lignes)
        self.taille_case = min(x_size, y_size)

        # On efface les cases
        self.canvas.delete("case")
        # On efface la case selected si il y en a une
        self.canvas.delete("selected")
        

        # On les redessine
        color = self.couleur2
        for row in range(self.n_lignes):
            #Alternance des couleurs
            if color == self.couleur2:
                color = self.couleur1
            else:
                color = self.couleur2

            for col in range(self.n_colonnes):
                x1 = col * self.taille_case
                y1 = row * self.taille_case
                x2 = x1 + self.taille_case
                y2 = y1 + self.taille_case
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="case")

                #Alternance des couleurs
                if color == self.couleur2:
                    color = self.couleur1
                else:
                    color = self.couleur2
        self.ActualiserPieces(False,False)



class JeuDeDames:
    def __init__(self):
        # On a besoin d'une fenêtre.
        self.fenetre = tk.Tk()
        self.fenetre.title("Jeux de dames de Michel Tremblay et Jean-Francois Paty")
        self.historiqueCharge = []
        self.partieCharge = []
        self.currentSelectedPosition = []      
       
        self.MenuJeu(self.fenetre) #définition des menus pour le jeu
        self.AI = True # Variable pour le controle du jeu contre l'ordinateur
        
        
        # On a besoin d'une partie.
        self.partie = Partie()
        self.aicontrol = Ai.AiControl(self.partie)
        # On a besoin d'un damier, qu'on placera dans notre fenêtre...
        self.interface_damier = InterfaceDamier(self.fenetre, 64,self.partie.damier)
        self.interface_damier.grid()

        
        self.interface_droite = tk.LabelFrame(self.fenetre, borderwidth=1,relief=RAISED)
        self.interface_droite 
        #Joueur
        self.joueur = tk.LabelFrame(self.interface_droite, borderwidth=1,relief=SUNKEN)
        self.afich_joueur = tk.Label(self.joueur,text="Joueur à jouer:" , width=20)
        self.etiq_joueur = tk.Label(self.joueur,text=self.partie.couleur_joueur_courant, width=20)
       
        self.afich_joueur.grid()
        self.etiq_joueur.grid()
        self.joueur.grid(row=0,column=0,padx=5,pady=5,sticky="n")
        # Pointage
        self.pointage = tk.LabelFrame(self.interface_droite, borderwidth=1,relief=SUNKEN,text="Pointage")
        self.nomBlanc = tk.Label(self.pointage,text="Blanc: ", width=10)
        self.nomNoir = tk.Label(self.pointage,text="Noir: ",width=10)
        self.pointBlanc = tk.Label(self.pointage,text="0", width=9)
        self.pointNoir = tk.Label(self.pointage,text="0",width=9)
        self.nomBlanc.grid(row=0,column=0)
        self.nomNoir.grid(row=1,column=0)
        self.pointBlanc.grid(row=0,column=1)
        self.pointNoir.grid(row=1,column=1)
        self.pointage.grid(row=1,column=0,padx=5,pady=20)
        # Message
        self.messageframe = tk.LabelFrame(self.interface_droite, borderwidth=1,relief=SUNKEN,text="Message")
        self.message = tk.Label(self.messageframe,text="",width=25,height = 5)
        self.messageframe.grid(padx=5,pady=15)
        self.message.grid()
        # Historique
        self.historiqueframe = tk.LabelFrame(self.interface_droite, borderwidth=1,relief=SUNKEN,text="Historique")
        self.historique = tk.Text(self.historiqueframe,width=20,height=13,)
        self.historiqueframe.grid(sticky="s",padx=5,pady=15)
        self.historique.grid()
        self.scrollbar = tk.Scrollbar(self.historiqueframe,command=self.historique.yview)
        self.scrollbar.grid(row=0,column=1,sticky='nse')
        self.historique['yscrollcommand'] = self.scrollbar.set
        self.etiquettetest = tk.Label(self.interface_droite,text="")
        self.etiquettetest.grid()
        self.interface_droite.grid(row=0,column=1,sticky="ne", padx=5, pady=5)
        self.fenetre.bind("<Button-1>",self.click)

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.fenetre.grid_columnconfigure(0, weight=1)
        self.fenetre.grid_rowconfigure(0, weight=1)

        # Truc pour le redimensionnement automatique des éléments du plateau.
        self.interface_damier.grid_columnconfigure(0, weight=1)
        self.interface_damier.grid_rowconfigure(0, weight=1)


        # Boucle principale.
        self.fenetre.mainloop()

    def getDamierSize(self):
        """
        Le damier est carré donc on veut juste avoir la plus petite grosseur du damier pour connaitre sa grosseur
        """
        damierwidth = self.interface_damier.winfo_width()
        damierheight = self.interface_damier.winfo_height()
        if damierwidth>damierheight:
            return damierheight-12
        else:
            return damierwidth-12

    def getClickPosition(self, size, event):
        """
        On trouve dans quel case exactement on click (Coordonnée x,y)
        """
        x =   event.x // (size/8)
        y =   event.y // (size/8)
        return (int(x), int(y))

    def VerificationSelectionValide(self, position):
        """ vérification de la selection """ 
        #position est inversé dans ce code par rapport à la partie
        self.message["text"] = ""
        positionInverse = (position[1],position[0])
        pieceChoisie = self.partie.damier.get_piece(positionInverse)
        try:
            self.partie.valider_position_source(positionInverse)
            self.interface_damier.selectCase(position, "yellow")
            listePosition = self.partie.damier.lister_deplacements_possibles_a_partir_de_position(positionInverse,self.partie.joueur_courant_peut_prendre_piece_adverse())
            for positionPossible in listePosition:
                positionPossible = (positionPossible[1],positionPossible[0])
                self.interface_damier.selectCase(positionPossible,"green")
            return True
        except Exception as e:
            self.message["text"] = e.msg
            return False
        

    def click(self, event):
        """
        Au click (donc selection d'une piece) on trouve avec le click qu'elle case on a clicker et on "HighLight" cette case
        """
        self.GestionduJeux(event)

    def GestionduJeux(self, event):
        """ Gestion du jeu principal """
        try:
            if event.widget.widgetName == "canvas":
                damierSize = self.getDamierSize()
                damierPosition = self.getClickPosition(damierSize,event)
                Continue = True
                if damierPosition[0] < 8 and damierPosition[1] < 8:
                    if self.currentSelectedPosition != []:
                        lastclick = self.currentSelectedPosition
                        destInverse = (damierPosition[1],damierPosition[0])
                        sourceInverse = (lastclick[1],lastclick[0])
                        doitPrendre = self.partie.joueur_courant_peut_prendre_piece_adverse()
                        currentPossibilities = self.partie.damier.lister_deplacements_possibles_a_partir_de_position(sourceInverse,doitPrendre)
                        if destInverse in currentPossibilities:
                            self.partie.damier.deplacer(sourceInverse,destInverse)
                            self.Affiche_histo(sourceInverse, destInverse)
                            self.CalculPointage()
                            self.interface_damier.ActualiserPieces(True,False)
                            self.interface_damier.canvas.delete("selected")
                            self.interface_damier.canvas.delete("positionPossible")
                            self.currentSelectedPosition = []
                            maintenantdoitPrendre = self.partie.damier.position_peut_prendre_une_piece_adverse(destInverse)
                            if not maintenantdoitPrendre or not doitPrendre:
                                self.partie.passer_au_joueur_suivant()
                            
                                self.etiq_joueur["text"] = self.ShowCurrentPlayer()
                            Continue = False
                    #HighLight la case
                    if Continue:
                        if self.VerificationSelectionValide(damierPosition):
                            self.currentSelectedPosition = damierPosition
                            self.etiquettetest["text"] = "({},{},{})".format(event.x,event.y,damierPosition)
            if self.partie.couleur_joueur_courant == 'noir' and self.AI:
                self.aiPlay()
        except:
            if not self.VerifGagnant():
                tk.messagebox.showwarning("NULLE","La partie est nulle\nDémarrez une nouvelle partie")
    
    def aiPlay(self):
        doitPrendre = self.partie.joueur_courant_peut_prendre_piece_adverse()
        if not doitPrendre:
            self.aiCurrentPlay()
        while doitPrendre:
            doitPrendre = self.aiCurrentPlay()
        self.partie.passer_au_joueur_suivant()
        self.etiq_joueur["text"] = self.ShowCurrentPlayer()

    def aiCurrentPlay(self):
        bestMove = self.Aiset()
        source = bestMove[0]
        sourceInverse = (source[1],source[0])
        destination = bestMove[1]
        destinationInverse = (destination[1],destination[0])
        self.partie.damier.deplacer(source,destination)
        self.Affiche_histo(source, destination)
        doitPrendre = self.partie.damier.position_peut_prendre_une_piece_adverse(destination)
        self.CalculPointage()
        self.interface_damier.ActualiserPieces(True,False)
        return doitPrendre
    
    def Affiche_histo(self,source,destination):
        """Affiche L'historique des coups dans la fenetre"""
        chaine=self.etiq_joueur["text"] + str(source)+ " " + str(destination) + "\n"
        self.historique.insert(END, chaine)
        

    def MenuJeu(self, fenetre):
        """ Déclaration du menu du jeu """
        mainmenu = tk.Menu(fenetre)  ## Barre de menu 
        menuPartie = tk.Menu(mainmenu)  ## Menu fils menuExample 
        menuPartie.add_command(label="Nouvelle Partie", command=self.NouveauJeu)
        menuPartie.add_command(label="Nouvelle Partie vs AI", command=self.NouveauJeuAi)
        menuPartie.add_command(label="Charger une Partie", command=self.ChargerJeu)
        menuPartie.add_command(label="Charger une Partie avec historique", command=self.ChargerJeuHistorique)
        menuPartie.add_command(label="Sauvegarder une partie", command=self.SauveJeu)
        menuPartie.add_command(label="Sauvegarder une partie avec historique", command=self.SauveJeuHistorique)
        menuPartie.add_command(label="Quitter", command=fenetre.destroy) 
  
        menuHelp = tk.Menu(mainmenu) ## Menu Fils 
        menuHelp.add_command(label="A propos", command=self.aPropos) 
  
        mainmenu.add_cascade(label = "Partie", menu=menuPartie) 
        mainmenu.add_cascade(label = "Aide", menu=menuHelp)
        fenetre.config(menu = mainmenu)
        
    def aPropos(self):
        """ Afiche la boite de dialogue sur la version du jeu """ 
        tk.messagebox.showinfo("A propos", "                     Version 1.0\n                     Conçu par\nJean-Francois Paty et Michel Tremblay")
    

    def ShowCurrentPlayer(self):
        """ Affiche le joueur courant dans le cadre de la fenetre """
        self.etiq_joueur["text"] = self.partie.couleur_joueur_courant
        pass
    

    def VerifGagnant(self):
        """ Vérification si il y a un gagnant """
        
        if self.pointBlanc["text"] == '12':
            tk.messagebox.showinfo("Gagnant!!","Le joueur Blanc est Gagnant de la partie")
            self.message["text"] = "Partie gagné\npar le joueur\nBLANC"
            return True
        elif self.pointNoir["text"] == '12':
            tk.messagebox.showinfo("Gagnant!!","Le joueur Noir est Gagnant de la partie")
            self.message["text"] = "Partie gagné\npar le joueur\nNOIR"
            return True


    def CalculPointage(self):
        """ Calcul et affichage du pointage """
        
        noir = 12
        blanc = 12
        for piece in self.partie.damier.cases.values():
            if str(piece) == "x" or str(piece) == "X":
                blanc = blanc - 1
            elif str(piece) == "o" or str(piece) == "O":
                noir = noir - 1
        self.pointBlanc["text"] = str(blanc)
        self.pointNoir["text"] = str(noir)

    def Aiset(self):
        bestMove = self.aicontrol.StartAIGet()
        return bestMove
        
    def deplacerPiece(self,source,destination):
        self.interface_damier.damier.deplacer(source,destination)
        

    def NouveauJeu(self):
        """ Démarre une nouvelle partie """
        #Partie.nouvelle_partie
        self.historique.delete(1.0,END)
        self.interface_damier.ActualiserPieces(True,True)
        self.partie.historique = ""
        self.CalculPointage()
        self.ShowCurrentPlayer()
        self.AI = False

    def NouveauJeuAi(self):
        """ Nouvelle partie contre l'ordinateur """
        #Partie.nouvelle_partie
        self.historique.delete(1.0,END)
        self.interface_damier.ActualiserPieces(True,True)
        self.partie.historique = ""
        self.CalculPointage()
        self.ShowCurrentPlayer()
        self.AI = True
                
    def ChargerJeu(self):
        """ Charge une partie sans historique """
        self.partie.historique = ""
        fileName = filedialog.askopenfile(filetypes=[("Save Games", "*.sav")])
        try:
            if fileName!=None:
            
                self.historique.delete(1.0,END)
                avecHistorique = self.partie.charger(fileName.name)
                if avecHistorique:
                    if not self.QuestionChargementErreur("Il y a un historique dans le fichier\nVoulez vous le charger quand même\nsans l'historique?"):
                        raise ProblemeChargement("Chargement non complété\nIl contient un historique")
                    else:
                        self.ContinueChargement()
                else:
                    self.ContinueChargement()
           
            else:
                self.message["text"] ="Chargement réussi"
        except ProblemeChargement as e:
            self.message["text"] =e.msg

    def ChargerJeuHistorique(self):
        """ Charge une partie avec historique """
        self.partie.historique = ""
        fileName = filedialog.askopenfile(filetypes=[("Save Games", "*.sav")])
        try:
            if fileName!=None:
                self.historique.delete(1.0,END)
                avecHistorique = self.partie.charger(fileName.name)
                if not avecHistorique:
                    if not self.QuestionChargementErreur("Il n'y a pas d'historique dans le fichier\nVoulez vous le charger quand même?"):
                        raise ProblemeChargement("Chargement non complété\nIl contient aucun historique")    
                    else:
                        self.ContinueChargement()
                else:
                    self.ContinueChargement(True)
            else:
                self.message["text"] ="Chargement réussi"
        except ProblemeChargement as e:
                self.message["text"] =e.msg
    
    def ContinueChargement(self,historique = False):
        """Continue avec le chargement du jeux avec ou sans historique"""
        try:
            self.interface_damier.ActualiserPieces(True,False)
            if historique:
                self.historique.insert(END, self.partie.historique)
            self.CalculPointage()
        except ProblemeChargement as e:
            self.message["text"] =e.msg
        else:
            self.message["text"] ="Chargement réussi"
                     
    def QuestionChargementErreur(self,message):
        """Question à l'usager pour savoir si il veut charger le fichier quand même"""
        result = tk.messagebox.askquestion("Chargement", message, icon='warning')
        if result == "yes":
            return True
        else:
            return False
                    
    def SauveJeu(self):
        """ Sauvegarde une partie dans un ficher """
        self.file_opt = options = {}
        options['defaultextension'] = '.sav'
        options['filetypes'] = [("Save Games", "*.sav")]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'mySave.sav'
        options['title'] = 'Sauvegarder votre Jeux de Dames'
        filename=filedialog.asksaveasfile(mode='w', **self.file_opt)
        if filename!=None:
            try:
                self.partie.sauvegarder(filename.name,"")
            except ProblemeSauvegarde as e:
                self.message["text"] = e.msg
            else:
                self.message["text"] ="Sauvegarde réussie"
                
    def SauveJeuHistorique(self):
        """ Sauvegarde une partie dans un fichier avec l'historique"""
        self.file_opt = options = {}
        options['defaultextension'] = '.sav'
        options['filetypes'] = [("Save Games", "*.sav")]
        options['initialdir'] = 'C:\\'
        options['initialfile'] = 'mySave.sav'
        options['title'] = 'Sauvegarder votre Jeux de Dames'
        filename=filedialog.asksaveasfile(mode='w', **self.file_opt)
        if filename!=None:
            try:
                self.partie.sauvegarder(filename.name,self.historique.get(1.0, END))
            except ProblemeSauvegarde as e:
                self.message["text"] = e.msg
            else:
                self.message["text"] ="Sauvegarde réussie"
   
        
        
        
