depth = 1
alpha = -1000000
beta = 1000000

def joueCoup(jeu):
    c = decision(jeu, depth, jeu[1])
    game.joueCoup(jeu, c)

def decision(jeu, profondeur, joueur):
    listeCoups = game.getCoupsValides(jeu)
    maxVal = -100000000
    coupStock = None
    for c in listeCoups:
        saveJeu = game.getCopieJeu(jeu)
        game.joueCoup(saveJeu, c)
        val = estimation(saveJeu, profondeur-1, joueur, alpha, beta)
        if val > maxVal:
            maxVal = val
            coupStock = c
    return coupStock
        
def estimation(jeu, profondeur, joueur, a, b):
    
    if game.finJeu(jeu):
        if game.getGagnant(jeu) == joueur:
            return 10000
        elif game.getGagnant(jeu) == (joueur %2 + 1):
            return -10000
        else:
            return -100
            
    if profondeur == 0:
        return evaluation(jeu, joueur)
    
    if (jeu[1] == joueur):
        maxVal = -10000000
        for c in game.getCoupsValides(jeu):
            saveJeu = game.getCopieJeu(jeu)
            game.joueCoup(saveJeu, c)
            maxVal = max(maxVal, estimation(saveJeu, profondeur-1, joueur, a, b))
            a = max(a, maxVal)
            if b <= a:
                break
        return maxVal
    else:
        minVal = 10000000
        for c in game.getCoupsValides(jeu):
            saveJeu = game.getCopieJeu(jeu)
            game.joueCoup(saveJeu, c)
            minVal = min(minVal, estimation(saveJeu, profondeur-1, joueur, a, b))
            b = min(b, minVal)
            if b <= a:
                break
        return maxVal
        
def evaluation(jeu, joueur):
    return 1*(jeu[4][joueur-1] - jeu[4][joueur%2])
        
    