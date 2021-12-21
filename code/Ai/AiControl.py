#! /usr/bin/env python
# -*- coding:Utf-8 -*-
__author__ = "Michel Tremblay"


import random
from dames.partie import Partie

class AiControl:
    """Une classe pour generer un AI"""

    def __init__(self, partie):
        self.currentdamier = partie
    
    def StartAIGet(self):
        bigHistory = self.GetPossibleSource()
        #bestMove = self.getBestMove()
        return random.choice(bigHistory)

    
    def GetPossibleSource(self):
        couleur = self.currentdamier.couleur_joueur_courant
        possibleSource = []
        doitPrendre = self.currentdamier.joueur_courant_peut_prendre_piece_adverse()
        for key in self.currentdamier.damier.cases.keys():
            try:
                self.currentdamier.valider_position_source(key)
                destpossible = self.currentdamier.damier.lister_deplacements_possibles_a_partir_de_position(key,doitPrendre)
                if destpossible != []:
                    possibleSource.append((key,random.choice(destpossible)))
            except Exception as e:
                message = e.msg
        return possibleSource

    


    
   



               
        

        


