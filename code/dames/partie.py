#! /usr/bin/env python
# -*- coding:Utf-8 -*-
__author__ = "Jean-Francis Roy"
from dames.damier import Damier
from dames.exceptions import PositionSourceInvalide, PositionCibleInvalide, ProblemeChargement, ProblemeSauvegarde


class Partie:
    def __init__(self):
        """
        Méthode d'initialisation d'une partie. On initialise 4 membres:
        - damier: contient le damier de la partie, celui-ci contenant le dictionnaire de pièces.
        - couleur_joueur_courant: le joueur à qui c'est le tour de jouer.
        - doit_prendre: un booléen représentant si le joueur actif doit absoluement effectuer une prise de pièce.
        - position_source_forcee: Une position avec laquelle le joueur actif doit absoluement jouer. Le seul moment
          où cette position est utilisée est après une prise: si le joueur peut encore prendre d'autres pièces adverses,
          il doit absolument le faire. Ce membre contient None si aucune position n'est forcée.
        """
        self.damier = Damier()
        self.couleur_joueur_courant = "blanc"
        self.doit_prendre = False
        self.position_source_forcee = None
        self.historique = "" #Permet de récupérer l,historique des coups joués.

    def valider_position_source(self, position_source):
        """
        Vérifie la validité de la position source, notamment:
        - Est-ce que la position contient une pièce?
        - Est-ce que cette pièce est de la bonne couleur?
        - Si le joueur doit absolument faire une prise, est-ce que la pièce choisie en la la possibilité?
        - Si le joueur doit absoluement continuer son mouvement avec une prise supplémentaire, a-t-il choisi la
          bonne pièce?

        ATTENTION: Utilisez self.couleur_joueur_courant, self.doit_prendre et self.position_source_forcee pour
                   connaître les informations nécessaires.
        ATTENTION: Bien que cette méthode valide plusieurs choses, les méthodes programmées dans le damier vous
                   simplifieront la tâche!

        :param position_source: La position source à valider.
        :return: Cette méthode ne retourne rien.
        :raise PositionSourceInvalide: Exception lancée si la position source est invalide.
        """
        if self.doit_prendre:
            if len(self.damier.lister_deplacements_possibles_a_partir_de_position(position_source, True)) == 0:
                raise PositionSourceInvalide("Position source invalide:\ncette pièce ne peut\npas faire de prise.")

            if self.position_source_forcee is not None:
                if not (self.position_source_forcee == position_source):
                    raise PositionSourceInvalide("Position source invalide:\nvous devez faire\nune prise avec la pièce " +
                                                 "en ({},{}).".format(self.position_source_forcee[0],
                                                                      self.position_source_forcee[1]))

        piece_source = self.damier.get_piece(position_source)
        if piece_source is None:
            raise PositionSourceInvalide("Position source invalide:\naucune pièce à\ncet endroit.")

        if not piece_source.couleur == self.couleur_joueur_courant:
            raise PositionSourceInvalide("Position source invalide:\npièce de mauvaise\ncouleur.")

    def valider_position_cible(self, position_source, position_cible):
        """
        Vérifie la validité la position cible est valide, en fonction de la position source.
        ATTENTION: Vous avez déjà programmé la méthode nécessaire dans le damier!

        :return: Cette méthode ne retourne rien.
        :raise PositionCibleInvalide: Exception lancée si la position cible est invalide.
        """
        if position_cible not in self.damier.lister_deplacements_possibles_a_partir_de_position(position_source,
                                                                                                self.doit_prendre):
            raise PositionCibleInvalide("Position cible invalide.")

    def passer_au_joueur_suivant(self):
        """
        Cette méthode permet de passer au joueur suivant.
        """
        if self.couleur_joueur_courant == "blanc":
            self.couleur_joueur_courant = "noir"
        else:
            self.couleur_joueur_courant = "blanc"

    def joueur_courant_peut_prendre_piece_adverse(self):
        """
        Vérifie si le joueur courant peut prendre une pièce adverse.

        :return: True si le joueur courant peut faire une prise, False autrement.
        """
        return self.damier.joueur_peut_prendre_une_piece_adverse(self.couleur_joueur_courant)

    def sauvegarder(self, nom_fichier,historique):
        """
        Sauvegarde une partie dans un fichier. Le fichier condiendra:
        - Une ligne indiquant la couleur du joueur courant.
        - Une ligne contenant True ou False, si le joueur courant doit absolument effectuer une prise à son tour.
        - Une ligne contenant None si self.position_source_forcee est à None, et la position ligne,colonne autrement.
        - Le reste des lignes correspondent au damier. Voir la méthode convertir_en_chaine du damier pour le format.

        :param nom_fichier: Le nom du fichier où sauvegarder.
        :type nom_fichier: string.
        :param historique : Contient la liste des coups joués.
        """
        try:
            with open(nom_fichier, "w") as f:
                f.write("{}\n".format(self.couleur_joueur_courant))
                f.write("{}\n".format(self.doit_prendre))
                if self.position_source_forcee is not None:
                    f.write("{},{}\n".format(self.position_source_forcee[0], self.position_source_forcee[1]))
                else:
                    f.write("None\n")
                f.writelines(self.damier.convertir_en_chaine())
                if historique!="": #Controle si le joueur veut sauvegarder l'historique
                    f.write("#\n") # début de la section de l'historique
                    f.write("{}\n".format(historique))
        except:
            raise ProblemeSauvegarde("Problème lors de la sauvegarde.")

    def charger(self, nom_fichier):
        """
        Charge une partie dans à partir d'un fichier. Le fichier a le même format que la méthode de sauvegarde.

        :param nom_fichier: Le nom du fichier à charger.
        :type nom_fichier: string.
        """
        avecHistorique = False
        try:
            with open(nom_fichier) as f:
                self.couleur_joueur_courant = f.readline().rstrip("\n")
                doit_prendre_string = f.readline().rstrip("\n")
                if doit_prendre_string == "True":
                    self.doit_prendre = True
                else:
                    self.doit_prendre = False

                position_string = f.readline().rstrip("\n")
                if position_string == "None":
                    self.position_source_forcee = None
                else:
                    ligne_string, colonne_string = position_string.split(",")
                    self.position_source_forcee = (int(ligne_string), int(colonne_string))
                chaine = ""
                while 1:
                    ligne=f.readline().rstrip("\n")#Lecture de la ligne suivante du fichier
                    if ligne=='':
                        break
                    elif ligne=="#": # Début de la section historique
                        reste=f.read() # Lire la fin du ficher qui contient l'historique
                        self.historique = reste
                        avecHistorique = True
                        break
                    elif ligne!="": #Détection de la non fin du fichier
                        chaine= chaine + ligne + "\n"
                    else:
                        break
            self.damier.charger_dune_chaine(chaine)
            return avecHistorique
        except:
            raise ProblemeChargement("Problème lors du chargement.")

    def nouvelle_partie(self):
        """
        Démarre une nouvelle partie en réinitialisant les attributs à leur valeur par défaut.
        """
        self.couleur_joueur_courant = "blanc"
        self.doit_prendre = False
        self.position_source_forcee = None
        self.damier.initialiser_damier_par_default()
