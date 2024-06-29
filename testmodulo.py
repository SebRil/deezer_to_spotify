days = [0,1,2,3,4,5,6,7,8,9] # non utilisée (il s'agit des index des températures)
temperatures = [12,19,5,3,5,16,20,21,10,8]

best_range = []
temporary_range = []
for i, temp in enumerate(temperatures) :
    if i > 0 :
        # Calcul de la différence avec le jour d'avant
        temp_difference = abs(temp - temperatures[i-1])
        # Si différence <= 5, on commence ou on continue à construire la range
        if temp_difference <= 5 :
            temporary_range.append(i)
        # Si différence > 5, on finit la range en cours (si elle existe) et on la compare à la meilleure potentiellement calculée
        else :
            if temporary_range :
                temporary_range.insert(0, temporary_range[0] - 1) # ajout du jour de départ
                # Si la range en cours est meilleure que la best_range, on remplace cette dernière
                if len(temporary_range) > len(best_range) :#gérer ici les égalités
                    best_range = temporary_range
                temporary_range = [] #reset

print(best_range)

