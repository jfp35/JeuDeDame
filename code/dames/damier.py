#! /usr/bin/env python
# -*- coding:Utf-8 -*-
__author__ = "Jean-Francis Roy"
from dames.piece import Piece
from dames.exceptions import PositionCibleInvalide, PositionSourceInvalide, ProblemeChargement


class Damier:
    """
    Classe représentant le damier d'un jeu de dames.
    """

    def __init__(self):
        """
        Méthode spéciale initialisant un nouveau damier.
        """
        # Dictionnaire de cases. La clé est une position (ligne, colonne), et la valeur une instance de la classe Piece.
        self.cases = {}

        # Appel de la méthode qui initialise un damier par défaut.
        self.initialiser_damier_par_default()

    def get_piece(self, position):
        """
        Récupère une pièce dans le damier.

        :param position: La position où récupérer la pièce.
        :type position: Tuple de coordonnées matricielles (ligne, colonne).
        :return: La pièce à cette position s'il y en a une, None autrement.
        """
        if position not in self.cases.keys():
            return None

        return self.cases[position]

    def position_valide(self, position):
        """
        Vérifie si une position est valide (chaque coordonnée doit être dans les bornes).

        :param position: Un couple (ligne, colonne).
        :type position: tuple de deux éléments
        :return: True si la position est valide, False autrement
        """
        return 0 <= position[0] <= 7 and 0 <= position[1] <= 7

    def lister_deplacements_possibles_a_partir_de_position(self, position, doit_prendre=False):
        """
        Cette méthode retourne une liste de positions qui sont accessibles par une pièce qui est placée sur la
        position reçue en paramètres. Un paramètre "doit_prendre" indique si la liste des positions retournée ne doit
        contenir que les positions résultant de la prise d'une autre pièce.

        Il y a donc au maximum 8 positions retournées:
        - Les 4 diagonales (les positions doivent être valides, et aucune autre pièce ne doit s'y trouver);
        - Les 4 sauts en diagonale (les positions doivent être valide, aucune pièce ne doit s'y trouver, et on doit
        sauter par dessus une pièce adverse.

        N'oubliez pas qu'un pion ne peut qu'avancer (et non reculer), mais peut effectuer une prise dans n'importe
        quelle direction. N'oubliez pas non plus qu'une dame peut avancer et reculer.

        :param position: La position de départ du déplacement.
        :type position: Tuple de deux éléments (ligne, colonne)
        :param doit_prendre: Indique si oui ou non on force la liste de positions à ne contenir que les déplacements
                             résultants de la prise d'une pièce adverse.
        :type doit_prendre: Booléen.
        :return: Une liste de positions où il est possible de se déplacer depuis la position "position".
        """
        piece = self.get_piece(position)
        if piece is None:
            return []

        diagonale_bas_gauche = (position[0] + 1, position[1] - 1)
        diagonale_bas_droite = (position[0] + 1, position[1] + 1)
        diagonale_haut_gauche = (position[0] - 1, position[1] - 1)
        diagonale_haut_droite = (position[0] - 1, position[1] + 1)
        saut_bas_gauche = (position[0] + 2, position[1] - 2)
        saut_bas_droite = (position[0] + 2, position[1] + 2)
        saut_haut_gauche = (position[0] - 2, position[1] - 2)
        saut_haut_droite = (position[0] - 2, position[1] + 2)

        piece_bas_gauche = self.get_piece(diagonale_bas_gauche)
        piece_bas_droite = self.get_piece(diagonale_bas_droite)
        piece_haut_gauche = self.get_piece(diagonale_haut_gauche)
        piece_haut_droite = self.get_piece(diagonale_haut_droite)
        piece_saut_bas_gauche = self.get_piece(saut_bas_gauche)
        piece_saut_bas_droite = self.get_piece(saut_bas_droite)
        piece_saut_haut_gauche = self.get_piece(saut_haut_gauche)
        piece_saut_haut_droite = self.get_piece(saut_haut_droite)

        liste_deplacements = []

        if self.position_valide(diagonale_bas_gauche):
            if piece_bas_gauche is None:
                if not doit_prendre:
                    if piece.est_noir() or piece.est_dame():
                        liste_deplacements.append(diagonale_bas_gauche)
            else:
                if self.position_valide(saut_bas_gauche):
                    if piece_saut_bas_gauche is None and piece_bas_gauche.couleur != piece.couleur:
                        liste_deplacements.append(saut_bas_gauche)

        if self.position_valide(diagonale_bas_droite):
            if piece_bas_droite is None:
                if not doit_prendre:
                    if piece.est_noir() or piece.est_dame():
                        liste_deplacements.append(diagonale_bas_droite)
            else:
                if self.position_valide(saut_bas_droite):
                    if piece_saut_bas_droite is None and piece_bas_droite.couleur != piece.couleur:
                        liste_deplacements.append(saut_bas_droite)

        if self.position_valide(diagonale_haut_gauche):
            if piece_haut_gauche is None:
                if not doit_prendre:
                    if piece.est_blanc() or piece.est_dame():
                        liste_deplacements.append(diagonale_haut_gauche)
            else:
                if self.position_valide(saut_haut_gauche):
                    if piece_saut_haut_gauche is None and piece_haut_gauche.couleur != piece.couleur:
                        liste_deplacements.append(saut_haut_gauche)

        if self.position_valide(diagonale_haut_droite):
            if piece_haut_droite is None:
                if not doit_prendre:
                    if piece.est_blanc() or piece.est_dame():
                        liste_deplacements.append(diagonale_haut_droite)
            else:
                if self.position_valide(saut_haut_droite):
                    if piece_saut_haut_droite is None and piece_haut_droite.couleur != piece.couleur:
                        liste_deplacements.append(saut_haut_droite)

        return liste_deplacements

    def lister_deplacements_possibles_de_couleur(self, couleur, doit_prendre=False):
        """
        Fonction retournant la liste des positions (déplacements) possibles des pièces d'une certaine couleur. Encore
        une fois, un paramètre permet d'indiquer si on ne désire que les positions résultant de la prise d'une pièce
        adverse.

        ATTENTION: ne dupliquez pas de code déjà écrit! Réutilisez les fonctions déjà programmées!

        :param couleur: La couleur ("blanc", "noir") des pièces dont on considère le déplacement.
        :type couleur: string
        :param doit_prendre: Indique si oui ou non on force la liste de positions à ne contenir que les déplacements
                             résultants de la prise d'une pièce adverse.
        :return: Une liste de positions où les pièces de couleur "couleur" peuvent de se déplacer.
        """
        deplacements_possibles = []

        for (position, piece) in self.cases.items():
            if piece.couleur == couleur:
                deplacements_possibles += self.lister_deplacements_possibles_a_partir_de_position(position,
                                                                                                  doit_prendre)

        return deplacements_possibles

    def position_peut_prendre_une_piece_adverse(self, position):
        """
        Vérifie si la pièce à une certaine position peut prendre une pièce adverse.

        :param position: La position source.
        :type position: tuple (ligne, colonne)
        :return: True si la pièce peut faire une prise, False autrement.
        """
        return len(self.lister_deplacements_possibles_a_partir_de_position(position, True)) > 0

    def joueur_peut_prendre_une_piece_adverse(self, couleur_joueur):
        """
        Vérifie si un joueur peut prendre une pièce adverse.

        :param couleur_joueur: La couleur du joueur.
        :type couleur_joueur: string.
        :return: True si le joueur peut faire une prise, False autrement.
        """
        return len(self.lister_deplacements_possibles_de_couleur(couleur_joueur, True)) > 0

    def deplacer(self, position_source, position_cible):
        """
        Effectue un déplacement sur le damier. Si le déplacement est valide, on doit mettre à jour le dictionnaire
        self.cases, en déplaçant la pièce à sa nouvelle position.

        Cette méthode doit également:
        - Promouvoir un pion en dame si celui-ci atteint l'autre extrémité du plateau.
        - Supprimer une pièce adverse qui a été prise lors du déplacement, si c'est le cas.
        - Retourner un message indiquant "ok", "prise" ou "erreur".

        ATTENTION: Si le déplacement est effectué, cette méthode doit retourner "ok" si aucune prise n'a été faite,
                   et "prise" si une pièce a été prise.
        ATTENTION: Ne dupliquez pas de code! Vous avez déjà programmer (ou allez programmer) une méthode permettant
                   de trouver la liste des déplacements valides...

        :param position_source: La position source du déplacement.
        :type position_source: Tuple (ligne, colonne).
        :param position_cible: La position cible du déplacement.
        :type position_cible: Tuple (ligne, colonne).
        :return: True si le déplacement a été effectué avec prise, False autrement.
        :raise PositionSourceInvalide: Exception retournée si la position source est invalide.
        :raise PositionCibleInvalide: Exception retournée si la position cible est invalide.
        """
        piece = self.get_piece(position_source)

        if piece is None:
            raise PositionSourceInvalide("Déplacement invalide: aucune pièce à la position source.")

        deplacements_possibles = self.lister_deplacements_possibles_a_partir_de_position(position_source)
        if not position_cible in deplacements_possibles:
            raise PositionCibleInvalide("Déplacement invalide: position cible erronnée.")

        self.cases[position_cible] = piece
        del self.cases[position_source]

        # Si la pièce est rendue au bout, elle est promue reine!
        if (position_cible[0] == 0 and piece.est_blanc()) or (position_cible[0] == 7 and piece.est_noir()):
            piece.promouvoir()

        # Si le déplacement est une prise, on doit supprimer la pièce prise.
        if abs(position_cible[0] - position_source[0]) == 2:
            position_prise = ((position_cible[0] + position_source[0]) / 2,
                              (position_cible[1] + position_source[1]) / 2)
            del self.cases[position_prise]

            return True

        return False

    def convertir_en_chaine(self):
        """
        Retourne une chaîne de caractères où chaque case est écrite sur une ligne distincte.
        Chaque ligne contient l'information suivante :
        ligne,colonne,couleur,type

        Cette méthode pourrait par la suite être réutilisée pour sauvegarder un damier dans un fichier.

        :return: La chaîne de caractères.
        """
        chaine = ""
        for position, piece in self.cases.items():
            chaine += "{},{},{},{}\n".format(position[0], position[1], piece.couleur, piece.type_de_piece)

        return chaine

    def charger_dune_chaine(self, chaine):
        """
        Remplit le damier à partir d'une chaîne de caractères comportant l'information d'une pièce sur chaque ligne.
        Chaque ligne contient l'information suivante :
        ligne,colonne,couleur,type

        :param chaine: La chaîne de caractères.
        :type chaine: string
        :raise ProblemeChargement: Exception lancée si un problème survient lors du chargement.
        """
        try:
            self.cases.clear()
            for information_piece in chaine.split("\n"):
                if information_piece != "":
                    ligne_string, colonne_string, couleur, type_piece = information_piece.split(",")
                    self.cases[(int(ligne_string), int(colonne_string))] = Piece(couleur, type_piece)
        except:
            raise ProblemeChargement("Problème lors du chargement.")

    def initialiser_damier_par_default(self):
        """
        Initialise un damier de base avec la position initiale des pièces.
        """
        self.cases.clear()
        self.cases[(7, 0)] = Piece("blanc", "pion")
        self.cases[(7, 2)] = Piece("blanc", "pion")
        self.cases[(7, 4)] = Piece("blanc", "pion")
        self.cases[(7, 6)] = Piece("blanc", "pion")
        self.cases[(6, 1)] = Piece("blanc", "pion")
        self.cases[(6, 3)] = Piece("blanc", "pion")
        self.cases[(6, 5)] = Piece("blanc", "pion")
        self.cases[(6, 7)] = Piece("blanc", "pion")
        self.cases[(5, 0)] = Piece("blanc", "pion")
        self.cases[(5, 2)] = Piece("blanc", "pion")
        self.cases[(5, 4)] = Piece("blanc", "pion")
        self.cases[(5, 6)] = Piece("blanc", "pion")
        self.cases[(2, 1)] = Piece("noir", "pion")
        self.cases[(2, 3)] = Piece("noir", "pion")
        self.cases[(2, 5)] = Piece("noir", "pion")
        self.cases[(2, 7)] = Piece("noir", "pion")
        self.cases[(1, 0)] = Piece("noir", "pion")
        self.cases[(1, 2)] = Piece("noir", "pion")
        self.cases[(1, 4)] = Piece("noir", "pion")
        self.cases[(1, 6)] = Piece("noir", "pion")
        self.cases[(0, 1)] = Piece("noir", "pion")
        self.cases[(0, 3)] = Piece("noir", "pion")
        self.cases[(0, 5)] = Piece("noir", "pion")
        self.cases[(0, 7)] = Piece("noir", "pion")

    def __repr__(self):
        """
        Cette méthode spéciale permet de modifier le comportement d'une instance de la classe Damier pour l'affichage.
        Faire un print(un_damier) affichera le damier à l'écran.
        """
        s = " +-0-+-1-+-2-+-3-+-4-+-5-+-6-+-7-+\n"
        for i in range(0, 8):
            s += str(i)+"| "
            for j in range(0, 8):
                if (i, j) in self.cases:
                    s += str(self.cases[(i, j)])+" | "
                else:
                    s += "  | "
            s += "\n +---+---+---+---+---+---+---+---+\n"

        return s
