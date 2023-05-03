# ID 4

# imports
import pandas as pd
import random



def creation_structure_rythmique_globale(emotion_structure, emotion_rythme, i = 0):
    option = emotion_structure['option_rythme']
    if(i > 99):
        print("Le nombre maximale de piste possible a été atteint, ou le parametre d'option en entrée a mal été défini")
        print("TagError : InternalError/creation_structure/creation_structure_globale/4-40.9")
    else:
        size = emotion_structure['taille_des_structures']
        structures_crees = []
        structures_rythme = []
        voix_suivante = pd.Series([], dtype = object)
        for struct in emotion_structure['struct_globale']:
            if not (struct[0] in structures_crees):
                structures_rythme.append(creation_structure_rythmique(emotion_rythme, size = size, option = option[i])) # On ajoute la structure rytmique correspondante
                structures_crees.append(struct[0])
        if(not emotion_structure['autre_voix'].empty):
            if(i >= len(option)):
                print("Il y a des voix en trop, ou alors il manque des arguments dans 'option'")
                print("TagError : InternalError/creation_structure/creation_structure_globale/4-60.8")
            else:
                voix_suivante = creation_structure_rythmique_globale(emotion_structure['autre_voix'], emotion_rythme, i = i+1)

        structure_morceau = pd.Series([emotion_structure['struct_globale'], structures_rythme, emotion_structure['instrument'], voix_suivante, emotion_structure['volume']],
                                  index = ['struct_globale','structures','instrument','autre_voix','volume'])
    return structure_morceau



def creation_structure_rythmique(emotion, size = 4, option = '44'):
    new_structure = []
    try:
        for compte_mesure in range(size):
            if(compte_mesure == 0):
                etiquette = 'debut' + option
            elif(compte_mesure == size-1):
                etiquette = 'fin' + option
            else:
                print("TagError : InternalError/creation_structure/new_emotion_structure/2-80.7")
                exit()
            new_structure.append(random.sample(emotion[etiquette], 1)[0])
    except KeyError:
        print("Erreur, typiquement causé par un choix de taille de structure trop grand, sans fournir d'etiquette intermediaire")
        print("TagError : KeyError/creation_structure/new_emotion_structure/2-85.6")
        exit()

    return new_structure



