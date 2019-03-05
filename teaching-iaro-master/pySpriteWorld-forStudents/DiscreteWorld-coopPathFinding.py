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

import random 
import numpy as np
import sys

def astar(initState, goalState, wallStates):
    
    posDepart = { "pos" : initState[0], "score": 0}
    explored = [[posDepart.get("pos"), 0, abs(initState[0][0] - goalState[0][0]) + abs(initState[0][1] - goalState[0][1]), None]]
    reserve = []
    while(True):
        #print(explored,"\n")
        #time.sleep(0.5)
        for i in [(0,1),(0,-1),(1,0),(-1,0)]:        
            next_row = posDepart.get("pos")[0]+i[0]
            next_col = posDepart.get("pos")[1]+i[1]
            nouvellePos = (next_row,next_col)
            if (nouvellePos not in wallStates) and (nouvellePos not in [explored[i][0] for i in range(len(explored))]) and next_row>=0 and next_row<20 and next_col>=0 and next_col<20 :
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
        reserve.remove(tmpTrucTruc)
            
    



    
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
    game.fps = 15  # frames per second
    game.mainiteration()
    game.mask.allow_overlaping_players = True
    #player = game.player
    
def main():

    #for arg in sys.argv:
    iterations = 50 # default
    if len(sys.argv) == 2:
        iterations = int(sys.argv[1])
    print ("Iterations: ")
    print (iterations)

    init()
    
    
    

    
    #-------------------------------
    # Initialisation
    #-------------------------------
       
    players = [o for o in game.layers['joueur']]
    nbPlayers = len(players)
    score = [0]*nbPlayers
    
    
    # on localise tous les états initiaux (loc du joueur)
    initStates = [o.get_rowcol() for o in game.layers['joueur']]
    print ("Init states:", initStates)
    
    
    # on localise tous les objets ramassables
    goalStates = [o.get_rowcol() for o in game.layers['ramassable']]
    print ("Goal states:", goalStates)
        
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
     
    
    #version infinie et alternative avec gestion de collision
    
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
                
                #gestion de la collision
                listePosBloquees = []
                for a in range(nbPlayers):
                    if listeLenParcours[a] > i:
                        
                
                players[j].set_rowcol(row,col)               
                game.mainiteration()
                posPlayers[j] = (row,col)
                
                
                # si on a  trouvé un objet on le ramasse
                if (row,col) == playerGoal[j]:
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
                game.mainiteration()
                posPlayers[j] = (row,col)
                
                
                # si on a  trouvé un objet on le ramasse
                if (row,col) == playerGoal[j]:
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

if __name__ == '__main__':
    main()
    


