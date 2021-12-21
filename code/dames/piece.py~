__author__ = "Jean-Francis Roy"


class Piece:
    """
    Classe modélisant une pièce d'un jeu de dames.
    """

    # Variable statique permettant de numéroter les pièces.
    numero = 0

    def __init__(self, couleur, type_de_piece):
        """
        La méthode spéciale __init__ d'une classe est appelée lorsqu'on instancie un nouvel objet. Elle peut prendre
        des paramètres supplémentaires (ici, "couleur" et "type_de_piece"), qui sont les paramètres nécessaires
        lorsqu'on crée un nouvel objet. Le mot clé "self" permet de stocker des informations dans l'instance de
        l'objet. Chaque instance a son propre espace mémoire et peut donc contenir des valeurs différentes dans ses
        variables membres.

        :param couleur: couleur de la pièce ("blanc", "noir").
        :type couleur: string.
        :param type_de_piece: type de pièce ("pion", "dame").
        :type type_de_piece: string.
        :param numero: numéro de la pièce (facultatif).
        :type numero: int.
        """
        assert couleur in ["blanc", "noir"], "Piece: couleur invalide."
        assert type_de_piece in ["pion", "dame"], "Piece: type invalide."

        self.couleur = couleur
        self.type_de_piece = type_de_piece
        self.numero_unique = Piece.numero
        Piece.numero += 1

        self.nom = "%s%s%d" % ("P" if type_de_piece == "pion" else "D",
                               "B" if couleur == "blamc" else "N",
                               self.numero_unique)

    def est_pion(self):
        """
        Retourne si la pièce est un pion.

        :return: True si la pièce est un pion, False autrement.
        """
        return self.type_de_piece == "pion"

    def est_dame(self):
        """
        Retourne si la pièce est une dame.

        :return: True si la pièce est une dame, False autrement.
        """
        return self.type_de_piece == "dame"

    def est_blanc(self):
        """
        Retourne si la pièce est de couleur blanche.

        :return: True si la pièce est de couleur blanche, False autrement.
        """
        return self.couleur == "blanc"

    def est_noir(self):
        """
        Retourne si la pièce est de couleur noire.

        :return: True si la pièce est de couleur noire, False autrement.
        """
        return self.couleur == "noir"

    def promouvoir(self):
        """
        Cette méthode permet de "promouvoir" une pièce, c'est à dire la transformer en dame.
        """
        self.type_de_piece = "dame"

    def __repr__(self):
        """
        Cette méthode spéciale permet de modifier le comportement d'une instance de la classe Piece pour l'affichage.
        Faire un print(une_piece) affichera un caractère unicode représentant le dessin d'une pièce.
        """
        if self.est_blanc() and self.est_pion():
            return "\u26C0"
        elif self.est_blanc() and self.est_dame():
            return "\u26C1"
        elif self.est_noir() and self.est_pion():
            return "\u26C2"
        else:
            return "\u26C3"
