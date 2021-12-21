#! /usr/bin/env python
# -*- coding:Utf-8 -*-
__author__ = "Jean-Francis Roy"


class PositionSourceInvalide(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)

class PositionCibleInvalide(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)


class ProblemeChargement(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)


class ProblemeSauvegarde(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)