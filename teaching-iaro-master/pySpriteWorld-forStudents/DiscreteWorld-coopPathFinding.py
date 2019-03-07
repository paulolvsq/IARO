# -*- coding: utf-8 -*-

# Nicolas, 2015-11-18

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
        



def astar(initState, goalState, wallStates):
    if initState == goalState:
        return goalState
    posDepart = { "pos" : initState[0], "score": 0}
    explored = [[posDepart.get("pos"), 0, abs(initState[0][0] - goalState[0][0]) + abs(initState[0][1] - goalState[0][1]), None]]
    reserve = []
    while(True):
        #print(len(explored),"\n")
        for i in [(0,1),(0,-1),(1,0),(-1,0)]:        
            next_row = posDepart.get("pos")[0]+i[0]
            next_col = posDepart.get("pos")[1]+i[1]
            nouvellePos = (next_row,next_col)
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
            print(tmpTrucTruc, reserve,len(explored),posDepart,initState,goalState)
            sys.exit(1)
    
def choixSimple(posSuiv,posPlayers,wallStates,numPlayer,goal):
    coupsLegaux = []
    posBloquee = []
    for i in [(0,1),(0,-1),(1,0),(-1,0)]:
        next_pos = (posSuiv[0]+i[0],posSuiv[1]+i[1])
        if posValide(next_pos,wallStates):
            if next_pos in posPlayers:
                posBloquee.append(next_pos)
            else:
                coupsLegaux.append(next_pos)
    coupsLegauxScore = [abs(i[0] - goal[0]) + abs(i[1] - goal[1]) for i in coupsLegaux]
    if coupsLegaux == []:
        return posSuiv
    return coupsLegaux[coupsLegauxScore.index(min(coupsLegauxScore))]

    
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
    game.fps = 8 # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player
    
def main():

    #for arg in sys.argv:
    #iterations = 50 # default
    #if len(sys.argv) == 2:
    #    iterations = int(sys.argv[1])
    #print ("Iterations: ")
    #print (iterations)

    init('pathfindingWorld_MultiPlayer1')
    
    
    

    
    #-------------------------------
    # Initialisation
    #-------------------------------
       
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    score = [0]*nbPlayers
    
    
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    
    # on localise tous les objets ramassables
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
        
    # on localise tous les murs
    wallStates = [w.get_rowcol() for w in game.layers['obstacle']]
    #print ("Wall states:", wallStates)
    
    #-------------------------------
    # Placement aleatoire des fioles 
    #-------------------------------
    
    
    # on donne a chaque joueur une fiole a ramasser
    # en essayant de faire correspondre les couleurs pour que ce soit plus simple à suivre
    
    
    #-------------------------------
    # Boucle principale de déplacements 
    #-------------------------------
    
    """
    #version opportuniste classique demandée sans gestion de collision
    
    posPlayers = initStates
    print(posPlayers)
    listeIters = []
    for i in range(len(posPlayers)):
        print(posPlayers[i],goalStates[i])
        listeIters.append(astar([posPlayers[i]],[goalStates[i]],wallStates))
    #print(listeIters) 
    listeLenParcours = [len(l) for l in listeIters]
    maxLen = max(listeLenParcours)
    
    for i in range(maxLen):
        for j in range(nbPlayers): # on fait bouger chaque joueur séquentiellement
            if i >= listeLenParcours[j]:
                continue
            row,col = listeIters[j][i]    
            players[j].set_rowcol(row,col)               
            game.mainiteration()
            
            
            # si on a  trouvé un objet on le ramasse
            if (row,col) in goalStates:
                o = players[j].ramasse(game.layers)
                game.mainiteration()
                print ("Objet trouvé par le joueur ", j)
                goalStates.remove((row,col)) # on enlève ce goalState de la liste
                score[j]+=1
                
        
                # et on remet un même objet à un autre endroit
                x = random.randint(1,19)
                y = random.randint(1,19)
                while (x,y) in wallStates:
                    x = random.randint(1,19)
                    y = random.randint(1,19)
                o.set_rowcol(x,y)
                goalStates.append((x,y)) # on ajoute ce nouveau goalState
                game.layers['ramassable'].add(o)
                game.mainiteration()                
                
                break  
    
    print ("scores:", score)
    pygame.quit()
    """
    accObjets = []
    #version infinie et alternative avec gestion de collision
    
    posPlayers = initStates  
    while 1:
        #print ("Init states:", initStates)
        #print ("Goal states:", goalStates)
    
        #print(posPlayers)
        listeIters = []
        playerGoal = [goalStates[i] for i in range(len(players))]
        for i in range(len(posPlayers)):
            #print(posPlayers[i],goalStates[i])
            listeIters.append(astar([posPlayers[i]],[playerGoal[i]],wallStates))
        #print(listeIters) 
        listeLenParcours = [len(l) for l in listeIters]
        maxLen = max(listeLenParcours)
        flagList = [0]*len(players)
        i = 0
        while i < maxLen:
            #print(i,maxLen,[len(l) for l in listeIters])
            for j in range(nbPlayers): # on fait bouger chaque joueur séquentiellement
                print(posPlayers)
                bloqueurFini = False
                if i >= listeLenParcours[j]:
                    continue                
                row,col = listeIters[j][i]
                next_pos = (row, col)
                posAutresJoueurs = []
                for iter in range(nbPlayers):
                    if iter != j:
                        posAutresJoueurs.append(posPlayers[iter])
                
                #print(posAutresJoueurs,next_pos)
                if next_pos in posAutresJoueurs:
                    print(i,"collision",j,flagList,posPlayers)
                    if not flagList[j]:                       
                        trouverBloqueur = [a == next_pos for a in posPlayers] 
                        print(trouverBloqueur)                            
                        flagList = [flagList[a] + (int) (trouverBloqueur[a]) for a in range(nbPlayers)]
                        if listeLenParcours[flagList.index(max(flagList))] < i:
                            bloqueurFini = True
                            print("esquive")
                        else:
                            listeIters[j] = listeIters[j][:max(i-1,0)] + [listeIters[j][max(i-1,0)]] + listeIters[j][max(i-1,0):]
                            row,col = listeIters[j][i]
                    else:
                        listeIters[j] = listeIters[j][:max(i-1,0)] + [choixSimple(next_pos,posPlayers,wallStates,j,playerGoal[j]), listeIters[j][max(i-1,0)]] + listeIters[j][max(i-1,0):]
                        print(listeIters[j][i:i+3])
                        listeLenParcours[j]+= 1
                        #row,col = choixSimple(posPlayers,wallStates,j,playerGoal[j])
                    listeLenParcours[j]+= 1 - int(bloqueurFini)
                    maxLen = max(listeLenParcours)
                
                
                flagList[j] = int(bloqueurFini)
                players[j].set_rowcol(row,col) 
                #print ("pos ", j," : ", row,col)
                posPlayers[j] = (row,col)
                game.mainiteration()
                
                
                # si on a  trouvé un objet on le ramasse
                if (row,col) == playerGoal[j]:
                    accObjets.append(players[j].ramasse(game.layers))
                    game.mainiteration()
                    #print ("Objet trouvé par le joueur ", j)
                    goalStates.remove((row,col)) # on enlève ce goalState de la liste
                    score[j]+=1
                    
                    if len(goalStates) == 0:
                        for a in range(nbPlayers):                        
                            x = random.randint(2,7)
                            y = random.randint(2,7)
                            while (x,y) in wallStates or (x,y) in goalStates or (x,y) in posPlayers:
                                x = random.randint(2,7)
                                y = random.randint(2,7)
                            accObjets[a].set_rowcol(x,y)
                            goalStates.append((x,y)) # on ajoute ce nouveau goalState
                            game.layers['ramassable'].add(accObjets[a])
                            game.mainiteration()                
                        
                        break  
            i+=1
        #print ("scores:", score)
    pygame.quit()   
    """
    
    version infinie et alternative
    posPlayers = initStates   
    
    while 1:
        #print(posPlayers)
        listeIters = []
        playerGoal = [goalStates[i] for i in range(len(players))]
        for i in range(len(posPlayers)):
            #print(posPlayers[i],goalStates[i])
            listeIters.append(astar([posPlayers[i]],[playerGoal[i]],wallStates))
        #print(listeIters) 
        listeLenParcours = [len(l) for l in listeIters]
        maxLen = max(listeLenParcours)
        
        for i in range(maxLen):
            for j in range(nbPlayers): # on fait bouger chaque joueur séquentiellement
                if i >= listeLenParcours[j]:
                    continue
                row,col = listeIters[j][i]    
                players[j].set_rowcol(row,col) 
                posPlayers[j] = (row,col)
                game.mainiteration()
                
                
                # si on a  trouvé un objet on le ramasse
                if (row,col) == playerGoal[j]:
                    o = players[j].ramasse(game.layers)
                    game.mainiteration()
                    #print ("Objet trouvé par le joueur ", j)
                    goalStates.remove((row,col)) # on enlève ce goalState de la liste
                    score[j]+=1
                    
            
                    # et on remet un même objet à un autre endroit
                    x = random.randint(1,19)
                    y = random.randint(1,19)
                    while (x,y) in wallStates:
                        x = random.randint(1,19)
                        y = random.randint(1,19)
                    o.set_rowcol(x,y)
                    goalStates.append((x,y)) # on ajoute ce nouveau goalState
                    game.layers['ramassable'].add(o)
                    game.mainiteration()                
                    
                    break  
                      
        #print ("scores:", score)
    pygame.quit()       
    
    """
    


if __name__ == '__main__':
    main()
    


