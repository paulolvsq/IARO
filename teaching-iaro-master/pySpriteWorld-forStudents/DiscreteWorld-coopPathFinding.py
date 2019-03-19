# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
from gameclass import Game,check_init_game_done
from spritebuilder import SpriteBuilder
from players import Player
from sprite import MovingSprite
from ontology import Ontology
from itertools import chain
import pygame
import glo
import time 

import random 
import numpy as np
import sys


def posValide(pos,wallStates,mapSize = 20):
    row,col = pos
    return (pos not in wallStates) and row>=0 and row<mapSize and col>=0 and col<mapSize
        

def calculLongueurs(listeIters):
    #print(listeIters)
    listeLenParcours = [len(l) for l in listeIters]
    maxLen = max(listeLenParcours)
    return listeLenParcours,maxLen
    
def initPath(posPlayers,players,goalStates,wallStates): 
    listeIters = []
    playerGoal = [goalStates[i] for i in range(len(players))]
    for i in range(len(posPlayers)):
        listeIters.append(astar([posPlayers[i]],[playerGoal[i]],wallStates))    
    listeLenParcours,maxLen  = calculLongueurs(listeIters)
    return { "listeIters" : listeIters, "playerGoal" : playerGoal, "listeLenParcours" : listeLenParcours, "maxLen" : maxLen}
    
def detection(posPlayers,j,next_pos):    
    posAutresJoueurs = []
    for iter in range(len(posPlayers)):
        if iter != j:
            posAutresJoueurs.append(posPlayers[iter])
    return next_pos in posAutresJoueurs

def strategieBasique1(numIter,numPlayer,listeIters,wallStates):
    #strategie à implementer 
    """
    retourne la liste des tuples des positions du debut a la fin seulement pour le joueur en cours
    position du joueur collisionné = listeIters[numPlayer][numIter]
    calcul du nouveau parcours en considerant le nouveau mur auquel on a ajoute la position de la collision
    remplacement de la fin du parcours par le nouveau chemin calcule precedemment
    """
    if numIter == len(listeIters[numPlayer]) -1:
        return listeIters[numPlayer][:numIter] + [listeIters[numPlayer][numIter-1]] + [listeIters[numPlayer][-1]]
    wallStatesCopy = wallStates.copy()
    for i in range(len(listeIters)):
        if i != numPlayer:
            tmp = numIter
            if i > numPlayer:
                tmp-=1
            if len(listeIters[i]) <= tmp:
                 wallStatesCopy.append(listeIters[i][-1])
            if len(listeIters[i]) > tmp:                
                wallStatesCopy.append(listeIters[i][tmp])
    newChemin = astar([listeIters[numPlayer][max(0, numIter-1)]], [listeIters[numPlayer][-1]], wallStatesCopy)
    """
    if not len(newChemin):
        """"""
        si on a aucune des 4 cases disponibles
        on va regarder tous les joueurs qui bloquent, les forcer a reculer d'une case
        on se freeze une iteration et on garde la suite du path initial pour tenter de continuer dessus une fois le sandwich déconstruit
        attention il faut gérer le cas ou les autres joueurs étaient arrivés (ajout d'iterations de la fin de leur parcours jusqu'à numIter - 1 avec des pos identiques à leur actuelle)
        """"""
        
        for i in range(len(listeIters)):
            if i != numPlayer:
                tmp = numIter
                if i > numPlayer:
                    tmp-=1
                if len(listeIters[i]) < tmp:
                     """"""
                     verifier s'il est dans une des 4 cases autour de nous
                     on note ses deux dernieres positions
                     on ajoute des iterations dans sa liste d'iterations jusqu'à ce qu'il en ait tmp - 1 puis ses deux dernieres positions
                     """"""
                     if(verif4cases(listeIters[numPlayer][numIter], listeIters[i][-1])):
                         deuxDerniers = [listeIters[i][-2]] + [listeIters[i][-1]]
                         while len(listeIters[i]) < tmp-1:
                             listeIters[i].append(listeIters[i][-1])
                         listeIters[i]+=deuxDerniers
                             
                else:     
                    break
                    """"""
                    verifier s'il est dans une des 4 cases autour de nous
                    on ajoute au milieu de sa liste sa position precedente puis sa position
                    """"""
        return listeIters[numPlayer][:numIter+1] + [listeIters[numPlayer][numIter]]+ listeIters[numPlayer][numIter+1:]
        
    """
                    
    newL = listeIters[numPlayer][:numIter]
    if(random.random() > 0.1*(numPlayer+1)):
        newL+= [listeIters[numPlayer][max(0, numIter-1)]]
    newL += newChemin
    return newL    

def verif4cases(pos1, pos2):
    row, col = pos1
    return pos2 in [(row+1, col), (row, col+1),(row-1, col),(row, col-1)]

def pasDeGestion(numIter,numPlayer,listeIters):
    print("Collision en pos : ",listeIters[numPlayer][numIter])
    return listeIters[numPlayer]
    
def strategieCollision(numIter,numPlayer,listeIters,wallStates):
    #ici on appelle la stratégie choisie
    #les strategies renvoient la nouvelle liste de coups du joueur
    
    pasDeGestion(numIter,numPlayer,listeIters)
    return strategieBasique1(numIter,numPlayer,listeIters, wallStates)
                       
def verification_objet(pos,playerGoal,goalStates,numPlayer,posPlayers,score,accObjets,players,wallStates,minPos = 1,maxPos = 19):
    row,col = pos
    nbPlayers = len(players)
    if (row,col) == playerGoal[numPlayer]:
        accObjets.append(players[numPlayer].ramasse(game.layers))
        game.mainiteration()
        #print ("Objet trouvé par le joueur ", j)
        goalStates.remove((row,col)) # on enlève ce goalState de la liste
        score[numPlayer]+=1

        if len(goalStates) == 0:
            for a in range(nbPlayers):                        
                x = random.randint(minPos,maxPos)
                y = random.randint(minPos,maxPos)
                while (x,y) in wallStates or (x,y) in goalStates or (x,y) in posPlayers:
                    x = random.randint(minPos,maxPos)
                    y = random.randint(minPos,maxPos)
                accObjets[a].set_rowcol(x,y)
                goalStates.append((x,y)) # on ajoute ce nouveau goalState
                game.layers['ramassable'].add(accObjets[a])
                game.mainiteration()  
            accObjets = []
        return True
    return False

def astar(initState, goalState, wallStates):
    if initState == goalState:
        return goalState
    
    posDepart = { "pos" : initState[0], "score": 0}
    explored = [[posDepart.get("pos"), 0, abs(initState[0][0] - goalState[0][0]) + abs(initState[0][1] - goalState[0][1]), None]]
    reserve = []
    while(True):
        #print(len(explored),"\n")
        nbCasesValides = 0
        for i in [(0,1),(0,-1),(1,0),(-1,0)]:        
            next_row = posDepart.get("pos")[0]+i[0]
            next_col = posDepart.get("pos")[1]+i[1]
            nouvellePos = (next_row,next_col)
            if posValide(nouvellePos,wallStates):
                nbCasesValides  +=1
            if posValide(nouvellePos,wallStates) and (nouvellePos not in [explored[i][0] for i in range(len(explored))]):
                if nouvellePos in goalState:
                    listeCoups = []
                    listeCoups.append(nouvellePos)     
                    for truc in explored:
                        if truc[0] == posDepart.get("pos"):
                            a = truc
                            break                    
                    while a[3]:     
                        listeCoups.append(a[0])
                        nouvellePos = a[3] 
                        for truc in explored:
                            if truc[0] == nouvellePos:
                                a = truc
                                break 
                    listeCoups.append(initState[0])
                    ltmp = []
                    for ii in range(len(listeCoups),0,-1):
                        ltmp.append(listeCoups[ii-1])
                    return ltmp
                if not (next_row,next_col) in reserve:
                    esti = posDepart.get("score") + abs(next_row - goalState[0][0]) + abs(next_col - goalState[0][1])
                    tmp = [nouvellePos,posDepart.get("score")+1,esti,posDepart.get("pos")]
                    explored.append(tmp)
                    reserve.append(tmp)  
        if not nbCasesValides:
            return []
        minR = 99999999999999
        tmpTrucTruc = None
        for i in reserve:
            if i[2] < minR:
                minR = i[2]
                posDepart = { "pos" : i[0], "score" : i[1] }
                tmpTrucTruc = i 
        try:
            reserve.remove(tmpTrucTruc)
        except:
            return []
    
def initPath2(posPlayers,players,goalStates,wallStates): 
    listeIters = []
    playerGoal = [goalStates[i] for i in range(len(players))]
    wallStatesCopy = wallStates.copy()
    for i in range(len(posPlayers)):
        chemin = astar([posPlayers[i]],[playerGoal[i]],wallStatesCopy)
        if(len(chemin) > 0):
            listeIters.append(chemin)
        else:
            print("chemin par defaut joueur ", i)
            listeIters.append(astar([posPlayers[i]],[playerGoal[i]],wallStates))
        wallStatesCopy += listeIters[-1]
    listeLenParcours,maxLen  = calculLongueurs(listeIters)
    return { "listeIters" : listeIters, "playerGoal" : playerGoal, "listeLenParcours" : listeLenParcours, "maxLen" : maxLen}

def initPath3(posPlayers,players,goalStates,wallStates): 
    listeIters = []
    playerGoal = [goalStates[i] for i in range(len(players))]
    for i in range(len(posPlayers)):
        listeIters.append(astar([posPlayers[i]],[playerGoal[i]],wallStates))    
    """
    on en choisit un au hasard
    on le met dans la liste 1
    pour chaque autre astar
    on regarde s'i y a au moins une case en commun avec ceux de la liste 1
    sinon on l'ajoute a la liste 1
    si oui on cree la liste i+1
    etc on va dans i+2 i+3 jusqu'a ce qu'ils soient tous dans une liste
    une fois que tout ça est fait
    ceux de la liste 1 on les touche pas 
    ceux de la liste 2 et plus on les freeze pendant n iterations avec n = longueu max dans liste 1 etc
    etc...
    """
    L0 = []
    L0.append([0])
    for i in range(1, len(listeIters)): #pour chaque autre astar
        for j in listeIters[i]: #pour chaque case de ce astar
            for l in range(len(L0)): #pour chaque sous liste de L0
                for k in L0[0]: # pour chaque astar deja dans la classe 0
                    if j in listeIters[k]: #on verifie si l'iteration est deja dans un des astar de la classe courante
                        continue;
                    
                    
                
    listeLenParcours,maxLen  = calculLongueurs(listeIters)
    return { "listeIters" : listeIters, "playerGoal" : playerGoal, "listeLenParcours" : listeLenParcours, "maxLen" : maxLen}
    
# ---- ---- ---- ---- ---- ----
# ---- Main                ----
# ---- ---- ---- ---- ---- ----

game = Game()

def init(_boardname=None):
    global player,game
    # pathfindingWorld_MultiPlayer4
    name = _boardname if _boardname is not None else 'pathfindingWorld_MultiPlayer1'
    game = Game('Cartes/' + name + '.json', SpriteBuilder)
    game.O = Ontology(True, 'SpriteSheet-32x32/tiny_spritesheet_ontology.csv')
    game.populate_sprite_names(game.O)
    game.fps = 15# frames per second

    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player

def main():
    init('pathfindingWorld_MultiPlayer1')
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    score = [0]*nbPlayers  
    
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]

    #version infinie et alternative avec gestion de collision
    accObjets = []  
    while 1:
        posPlayers = initStates
        dicoTmp = initPath2(initStates,players,goalStates,wallStates)
        listeIters = dicoTmp["listeIters"]
        playerGoal = dicoTmp["playerGoal"]
        listeLenParcours = dicoTmp["listeLenParcours"]  
        maxLen = dicoTmp["maxLen"]
        i = 0
        while i < maxLen:
            # print(i,maxLen,[len(l) for l in listeIters])
            for j in range(nbPlayers): # on fait bouger chaque joueur séquentiellement
                if i >= listeLenParcours[j]:
                    continue  #si un joueur a fini on le fait pas bouger              
                row,col = listeIters[j][i]
                next_pos = (row, col)                
                #print(posAutresJoueurs,next_pos)
                if detection(posPlayers,j,next_pos):
                    listeIters[j] = strategieCollision(i,j,listeIters,wallStates)
                    listeLenParcours,maxLen  = calculLongueurs(listeIters)
                    row,col = listeIters[j][i]          
                players[j].set_rowcol(row,col) 
                posPlayers[j] = (row,col)
                game.mainiteration()
                
                
                # si on a  trouvé un objet on le ramasse
                a = verification_objet((row,col),playerGoal,goalStates,j,posPlayers,score,accObjets,players,wallStates,1,19)
                #if a:
                #    break  
            i+=1
        print(maxLen)
        #print ("scores:", score)
    pygame.quit()   

if __name__ == '__main__':
    main()

    
    

           
 
