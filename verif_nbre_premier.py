def est_premier(n: int) -> bool:
    """on va retourner True si le nombre est premier, False sinon, en appliquant d'abord
    l'élimination des cas de base puis ensuite on teste tout les diviseurs potentiels jusqu'à n
    en suivant la règle du 6k + 1 / 6k -1 pour tout les nbre à partir de 5 car
    tt nbre premier > 3 est de cette forme."""

    if n <= 1: #0, 1 et les nbre négatifs ne sont pas premiers
        return False

    if n <= 3: #cas de base : 2 et 3 sont premiers
        return True

    if n % 2 == 0  or n % 3 == 0: #on va éliminer tous les multiples de 2 ou 3
        return False

    #on va tester les diviseurs potentiels jusqu'à n
    #à partir de 5, on va uniquement tester les nombres qui ont une forme de 6k + 1 / 6k -1
    #car tout nombre premier > 3 est forcément de cette forme.
    i = 5
    while i * i <= n: # on va s'arrêter à la racine carré de n
        if n % i == 0 or n% (i+2) == 0: # si n est divisible par i ou i+2 ce n'est pas un nbre premier
            return False

        i += 6 # on avance de 6 (pour tester les prochains 6k + 1 / 6k -1)
    return True # si aucun diviseur est trouvé, on retourne true car n est premier

print(est_premier(2)) # 2 rest premier
print(est_premier(7)) # 7 est premier
print(est_premier(4)) #4 est pas premier
print(est_premier(10000000000)) # pas premier

# tout entier peut s'écrire sous la forme : n = 6k +r avec r appartient à {0,1,2,3,4,5}
#car 6 est multiple de 2 et 3 donc on peut regrouper par bloc de 6 qui permet de repérer les multiples
# de 2 ou 3 facilement.

#EN GROS : tout nombre premier supérieur à 3 est forcément de la forme 6+k -1 ou 6k+1

#EXEMPLE POUR N = 97
# on sait que c pas pair ni multiple de 3
# on teste 5 (6x1 -1), 7(6x1+1), 11 (6x2-1)















