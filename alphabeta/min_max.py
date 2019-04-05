#!/usr/bin/env python
#-*- coding: utf-8 -*-

jeu = None
depth = 1

def debut(jeu, profondeur):
    # parcours horizon 1 (les 6 coups du joueurs courant)
    # renvoie le coup avec l evaluation la plus haute
    listeCoups
    valMax = -10000
    coupMax = NULL
    for c in listeCoups:
        saveJeu = copie(jeu)
        saveJeu.joueCoup(c)
        val = MINMAX(saveJeu, profondeur-1, jeu[1])
        if val > valMax:
            valMax = val
            coupMax = c
    return coupMax

def MINMAX(jeu, profondeur,  joueur):

    if finJeu(jeu):
        if gagnant==joueur:
            return 100000
        elif gagnant==adversaire
            return -100000
        else:
            return -100

    if profondeur==0:
        return evaluation(jeu)
    listeCoups

    if(jeu[1]==joueur%2+1):
        #min
        minVal = 10000
        for c in listeCoups:
            saveJeu = copie(jeu)
            saveJeu.joueCoup(c)
            val = MINMAX(saveJeu, profondeur-1, joueur)
            if val < minVal:
                minVal = val
        return minVal
    else:
        #max
        maxVal = -10000
        for c in listeCoups:
            saveJeu = copie(jeu)
            saveJeu.joueCoup(c)
            val = MINMAX(saveJeu, profondeur-1, joueur)
            if val > maxVal:
                maxVal = val
        return maxVal

def evaluation(jeu):
    #renvoie la somme des Lambda(i)*F(i)
