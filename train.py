game.joueur1 = ab_train 
game.joueur2 = ab
"""on a une variable globale qui s'appelle params 
on affiche le vecteur de paramètres du genre [1,1,1...]"""

def train(eps = 1.0, decay = 0.999, n = 10, epoch = 1000):
    pars = ab_train.params
    for i in range (epoch):
        for j in range (len(pars)):
            v = joueN(n)[0] #fait jouer n fois le joueur 1 contre 2, chacun leur tour et on renvoie une liste avec les score comme on avait fait 
                #par défaut on a mis 10 ça va aller vite mais c'est peu fiable 
                #indicateur de la qualité du joueur mais joue sur la chance 
            x = random.rand()
            if x < 0.5:
                m = -eps
            else:
                m = eps
                pars[j] += m
                v2 = joueN(n)[0]
            if v1 > v2:
                pars[j] -= m
                print(str(pars))
                print(str(v2))
        eps *= decay
    ab.params = deepcopy(pars)
    train(e, decay, n, epoch)