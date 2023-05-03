import pandas as pd

# derniere_voix sert à initialiser les Series. C'est également ce qui indique la fin d'une des voix dans les 'emotion_struct'
derniere_voix = pd.Series([], dtype = object) # attention, cette definition sera peut-être opsolete dans des versions futurs de python

struct_globale = [[0,'i'],[1,'i'],[0,'i'],[2,'i'],[0,'rt+2'],[1,'rt+2'],[0,'r'],[2,'r']]
option_rythme_voix2 = ['-acc','-lyr2','-lyr2','-lyr1']
sadness_structure_voix2 = pd.Series([struct_globale, 2, option_rythme_voix2, None, derniere_voix, 80], 
                        index=['struct_globale','taille_des_structures','option_rythme','instrument','autre_voix','volume'])
option_rythme_voix1 = ['-lyr1','-lyr2','-lyr2','-lyr1'] 

sadness_structure = pd.Series([struct_globale, 2, option_rythme_voix1, None, sadness_structure_voix2, 100], 
                    index=['struct_globale','taille_des_structures','option_rythme','instrument','autre_voix','volume'])

# debut et fin font référence au début ou la fin d'une structure mélodique
etiquette = ['debut-lyr1', 'fin-lyr1', 'debut-lyr2', 'fin-lyr2', 'debut-acc', 'fin-acc'] # ce ne sont pas forcement les etiquettes définitives, on peut rajouter des choses
# Les étiquettes définitives peuvent être typiquement : mesure de début de structure, de fin de structure, mais aussi mesures spéciales (par exemple de début ou de fin de morceau)
# pour les premières et dernières structures d'un morceau par exemple
sadness_rythme = pd.Series([[[8,8,8,8],[8,8,8,4,4],[4,4,4,4,8,4,4],[8,4,4,8,4,4]], 
                            [[8,4,4,2,2,4,8],[8,8,16],[4,4,4,4,8,8]], 
                            [[12,4,12,4],[16,16]], 
                            [[16,16],[12,4,12,4],[16,8,8]], 
                            [[8,8,8,8],[16,16],[8,8,16]], 
                            [[16,16],[8,8,16]]], index=etiquette)



# struct_globale est une suite qui donne la composition de la structure globale.
# Cette suite contient un chiffre indiquant si la strcuture est basé sur la première (0), deuxième (1), ect... structure rythmique du morceau
# La structure correspondant au chiffre i est précisement la structure stocké dans structures[i]
# le str à coté du chiffre donne une indication sur la variation à réaliser sur la structure rythmique considérée : 
# structures qui se répètent rythmiquement mais sans lien mélodiquement ('r')
# des structures qui se répètent rythmiquement et qui transposent mélodiquement ('rt') 
# et des structures qui se repetent à l'identique ('i')
# on peut inventer d'autres types d'infos au besoin. Ces infos sont communes à la generation rythmique et mélodique

# 'taille_des_structures' est un int qui indique de combien de mesure sont composés les structures

# 'structures_rythmes','structures_notes' sont des listes vides au départ
# gobalement, il n'est même pas nécessaire de les mettre dans la series emotion_struct
# après passage dans l'algorithme, on y stock une liste de liste. Chaque liste contient une structure de 'taille_de_structure' mesures
# pour chaque numéros dans struct_globale, on construit par tirage au hasard une strucutre dans 'structures_rythmiques'

# 'intrument' définit le type d'instrument qui devra jouer les instructions. Cette information sera transmise au générateur de son
# L'info est peut-être inutile (le timbre est défini indépendement en fonction d'autres paramètres)

# autre_voix peut être utilisée si on veut ajouter une voix (acompagnement ou contre chant). Il faut alors définir une nouvelle structure globale, du même format
# On peut ajouter par casscade de cette manière des voix supplémentaires à l'infini (limite fixé à 99 pour l'instant)
# La dernière voix doit nécessairement être une serie vide (qu'on peut définir par derniere_voix = pd.Series([], dtpye = list) )

# Volume est un entier entre 1 et 100. Il définit le volume des pistes les unes par rapport aux autres
# ce n'est pas très important car on peut redefinir ce volume plus tard au moment du mixage des voix, mais ça peut servir justement à ce moment là pour avoir l'info de ce qui est important






# creation melodie : 

# fondamentale : permet de définir la tonalitée (ça pourrait être un parametre aléatoire)

# gammes : array de listes qui contienent les gammes possibles
# une gamme est définie par l'ecart entre chaque notes
# les gammes majeurs, mineurs, et mineur avec sensible altérées sont déjà définies plus haut
# CORRECTIF : Pour l'instant, gammes ne contient qu'une gamme donc ce n'est pas un array
# On pourra ajouter des gammes plus tard si necessaire
# Attention : les notes de liste_gamme sont indiquées par rapport à la gamme chromatique, mais les autres notes
# indiquées dans d'autres paramètres sont indiquées par rapport à la liste_gamme choisie
# Quelque gammes déjà définies : 
liste_gamme_majeur = [0,2,4,5,7,9,11]
liste_gamme_mineur = [0,2,3,5,7,8,10]
liste_gamme_minSensibleAlter = [0,2,3,5,7,8,11]
liste_gamme_pynthatoniqueMin = [0,3,5,7,11]
liste_gamme_pynthatoniqueMaj = [0,4,5,7,11]
liste_gamme_jazz1 = [0,3,4,5,7,10,11]
liste_gamme_chromatique = [0,1,2,3,4,5,6,7,8,9,10,11]


# duree_temps_fort : c'est la durée entre chaque temps fort
# typiquement en 4/4, ça sera la blanche ou la ronde (et défois la noire)
# Et en 3/4, ça pourra être la blanche pointée
# Je n'ai rien prévu pour qu'elle puisse être irrégulière pour l'instant
# Irrégulière = comme en 8/8 parfois ou on a des découpages 3,3,2

# premiere note : définit les premieres notes possibles dans la gamme choisie pour commencer le morceau ou pour le 
# reprendre après certains évenements (un silence ou une "double barre" par exemple)
# On prendra typiquement 0 et 4 (tonique et dominante) : 
premiere_note_classique = [0]
premiere_note_classique2 = [0,4]

# accords : Contient une liste de liste d'accord. 
# Il y a une liste pour chaque structures du morceau (pour chaque élements de strucutres) la liste des accords
# Il y a un accord pour chaque élements de durée duree_temps_fort de la structure
# Les notes indiquées sont les notes dans la gamme choisie (à chager -> définir les accords dans la gamme pythatonique perméterait d'avoir des accords plus généraux)
# (On n'est alors même plus obligé de définir la gamme du morceau, on peut juste définir l'accord rajouter un indice de transposition)
# Quelque accords classique si votre liste_gamme est liste_gamme_majeur ou une des liste_gamme_mineur :
acc_parfait = [0,2,4]
acc_parfait1rev = [-3,0,2]
acc_final = [0,0,0,7]
acc_septieme3 = [-1,1,3]
acc_septieme4 = [-1,1,3,5]
acc_dominante3 = [-3,-1,1,4] # remarque : l'ordre des notes de l'accord peut avoir du sens
acc_dominante4 = [-1,1,2,4]
acc_mediante = [2,4,6]
acc_seconde = [-2,0,1,3,5]


# ornementation : contient pour chaque elements de duree duree_temps_fort dans le morceau l'accord correspondant
# comme pour accords, on doit avoir len(ornementations) == duree_morceau//duree_temps_fort
# Une ornementation contient trois listes correspondant à la note post dernier accord, pre accord suivant, et aux autres
# Si il n'y a qu'une seule note de passage, c'est la pre accord suivant qui est jouée, ensuite, la post accord, et enfin les autres
# les orn_type indiquent si une note de passage est choisie dans l'absolu ('abs'), 
# ou par décalage par rapport à la note d'avant('avn') ou d'aprés('apr')
# c'est une chaine de caractère toujours située à la position 0 d'une liste de décalage d'ornememantation
# ! 'apr' ne peut être utilisé que dans la 3e liste d'une ornementation, et ne peut pas être utilisé sur le dernier temps fort d'une struct
# # note 1 : je rajoute 'ars' (avant répété sur la suivante) qui permet de choisir en fonction de la note d'avant et de faire varier la note d'après avec le même écart
# ça peut être trés utile pour les marches harmoniques en seconde ou en tierce
# ! ne peut pas être utilisé sur le dernier temps fort
# De plus, si 'ars' est utilisé au millieux de l'orn, alors il prend le pas sur le pre temps fort (sauf si il n'y a que une ou deux notes de passage)
# note 2 : On rajoute 'red' (random entre-deux) dont l'écart indiqué correspond à l'écart entre la note précedante et la note située deux coups
# plus loin, la note entre les deux sera tirée au hasard entre leur deux valeur; (je ne suis pas sur qu'il sera très util celui-la)
# liste d'ornementation utilisables
# (remarque pour la suite : plutôt que d'utiliser ce système, il vaudrait mieux fournir des listes d'enchainements possibles
# au programme, éventuellement dépendants des conditions. Il faut ensuite fixer un critère, éventuellement l'aléatoire, qui définit quel
# enchainement l'ordi choisit parmi ceux qui sont possibles dans un cas donné dans le morceau)
orn_conjoint = [['avn',-1,1],['avn',-1,1],['avn',1,-1]]
orn_conjoint_melodique = [['ars',-1,1],['ars',-1,1],['ars',-1,1]] # Le meilleur pour les mouvements conjoints
orn_retard_conjoint_appogiature = [['avn',0],['avn',-1,1],['apr',-1,1]] # vérifier si les appoggiatures marchent
orn_retard_conjoint = [['avn',0],['avn',-1,1],['avn',-1,1]]
orn_conjoint_appoggiature = [['avn',-1,1],['ars',-1,1],['apr',-1,1]] # Celui là est probablement pas mal
orn_quasiConjoint_appoggiature = [['avn',-2,-1,1,2],['avn',-1,-1,1,1,0],['apr',1,-1]]


orn_accord_parfait = [['abs',0,2,4],['abs',0,2,4],['abs',0,2,4]]
orn_accord_septieme = [['abs',1,3,4,6],['abs',1,3,4,6],['abs',1,3,4,6]]

orn_random = [['avn',-4,-3,-2,-1,0,1,2,3,4,5,6],['avn',-4,-3,-2,-1,0,1,2,3,4,5,6],['avn',-4,-3,-2,-1,0,1,2,3,4,5,6]]
orn_conjoint_randomLim_echapee = [['avn',-1,1],['abs',0,2,3,4],['abs',5]]
orn_conjoint_echapee_montant = [['avn',-1,1],['avn',1],['avn',1,2]]
orn_conjoint_echapee_descendant = [['avn',-1,1,1],['avn',-1],['avn',-1,-2]]

orn_avantFinal = [['avn',-1,1],['abs',-1,1,2,4],['apr',-1,2]]
orn_final = [['avn',-1,1],['abs',-3,0,4],['abs',0]]
orn_retard_ascendant1 = [['avn',0],['avn',0,1,1,1],['avn',0,1,1,2]]
orn_retard_ascendant2 = [['avn',0],['avn',0,1,1,1],['apr',-1,1]]

orn_conjoint_ton = [['ars',-2,2],['ars',-2,2],['ars',-2,2]] # Pour la gamme par demi-ton

# tempo : c'est une liste de deux élements qui correspondent à des tempos à la noire
# Le tempo est choisit au hasard entre les deux élements
# On peut aussi entrer un int, dans ce cas le tempo à la noire est égal au int
# quelque tempos classiques : 
largo = [48,60]
adagio = [56,72]
andante = [76,90]
allegro = [100,120]
presto = [140,160]


accords2 = [[acc_parfait,acc_parfait,acc_mediante,acc_mediante],[acc_septieme3,acc_mediante,acc_septieme4,acc_dominante4],[acc_parfait,acc_septieme4,acc_dominante4,acc_final]]
ornementations2 = [[orn_retard_ascendant2,orn_retard_ascendant1,orn_conjoint_echapee_montant,orn_conjoint_echapee_montant],[orn_conjoint_melodique,orn_conjoint_melodique,orn_conjoint_echapee_descendant,orn_conjoint_echapee_descendant],[orn_retard_conjoint_appogiature,orn_conjoint_melodique,orn_avantFinal,orn_final]]

accords = [[acc_parfait,acc_dominante3],[acc_parfait,acc_dominante3],[acc_dominante4,acc_final]]
ornementations = [[orn_conjoint_melodique,orn_conjoint_melodique],[orn_conjoint_melodique,orn_conjoint_melodique],[orn_conjoint_melodique,orn_final]]

sadness_notes_voix2 = pd.Series([liste_gamme_mineur, 32, premiere_note_classique, 3, accords, ornementations, largo, derniere_voix], 
                        index=['liste_gammes','duree_temps_fort','premiere_note','hauteur_moyenne','accords','ornementations','tempo','autre_voix'])

sadness_notes = pd.Series([liste_gamme_mineur, 32, premiere_note_classique, 4, accords, ornementations, adagio, sadness_notes_voix2], 
                        index=['liste_gammes','duree_temps_fort','premiere_note','hauteur_moyenne','accords','ornementations','tempo','autre_voix'])


description = "Il s'agit d'une architecture de morceau évoquant la tristesse"


sadness = pd.Series([sadness_structure, sadness_rythme, sadness_notes, description],
                    index = ['emotion_structure', 'emotion_rythme', 'emotion_notes', 'description'])
                    
                    

                    
                    


