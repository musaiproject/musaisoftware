
import pandas as pd
from random import choice, randint
from gestion_temps_frequence import conversion_temps_frequence
from variation_structure import transposition_gamme


def creation_structure_melodique_globale(emotion_structure, emotion_notes, fondamentale = None, tempo = None, i = 0):

    if(i > 99):
        print("limite de piste atteinte")
        exit()
    else:
        fondamentale = randint(0,11)
        tempo = 0
        if(type(emotion_notes['tempo']) == int):
            tempo = emotion_notes['tempo']
        elif(type(emotion_notes['tempo']) == str):
            if(type(tempo) == int):
                tempo = tempo
            else:
                print("TagError : ValueError/creation_notes/creation_structure_melodique_globale/1-25.26")
                exit()
        else:
            try:
                tempo = randint(emotion_notes['tempo'][0],emotion_notes['tempo'][1])
            except ValueError:
                print("Un erreur est survenue, probablement parce que emotion_melodie['tempo'] n'a pas le bon format")
                print("TagError : ValueError/creation_notes/creation_structure_melodique_globale/1-30.17")
                exit()
        stuctures_melodiques_crees = []
        structures_melodiques = []
        liste_finale = []
        voix_suivante = pd.Series([], dtype = object)
        for struct in emotion_structure['struct_globale']:
            print(struct)
            if not (struct[0] in stuctures_melodiques_crees):
                structures_melodiques.append(generer_structure_melodique(emotion_structure['structures'], struct[0], emotion_notes))
                liste_finale.extend(conversion_temps_frequence(structures_melodiques[struct[0]], emotion_notes, fondamentale, tempo))
            else:
                liste_finale.extend(
                    conversion_temps_frequence(
                        variations_structure_melodique(structures_melodiques[struct[0]], emotion_structure['structures'], emotion_notes, struct[0], struct[1]), emotion_notes, fondamentale, tempo))
        if(not emotion_structure['autre_voix'].empty):
            voix_suivante = creation_structure_melodique_globale(emotion_structure['autre_voix'], emotion_notes['autre_voix'], fondamentale = fondamentale, tempo = tempo, i = i + 1)
        structure_finale = pd.Series([liste_finale, emotion_structure['instrument'], voix_suivante, emotion_structure['volume'],18],
                                    index = ['liste_finale','instrument','autre_voix','volume','caste'])
    return structure_finale



def generer_structure_melodique(structures, indice_struct, emotion_notes):
    structure_melodique_norm = []
    duree_temps_fort = emotion_notes['duree_temps_fort']
    taille_gamme = len(emotion_notes['liste_gammes'])
    note = -1
    note_precedante = -1
    compte_temps = 0
    temps_fort = False
    note_suivante = None
    for mesure in structures[indice_struct]:
        for rythme in mesure:
            compte_temps += rythme
            temps_fort = int(compte_temps/duree_temps_fort)==compte_temps/duree_temps_fort
            tonique_actuelle = taille_gamme*(note_precedante//taille_gamme)
            if(note_suivante == None):
                note, note_suivante = generer_note(emotion_notes, indice_struct, note_precedante, tonique_actuelle, temps_fort)
            else:
                note = note_suivante
                note_suivante = None
            structure_melodique_norm.append([note,rythme])
            note_precedante = note
    return structure_melodique_norm



def generer_note(emotion_notes, indice_struct, note_precedante, tonique_actuelle, temps_fort):
    note = -1
    note_suivante = None
    position = 0
    if(temps_fort):
        if(note_precedante == -1):
            try:
                note = choice(emotion_notes['premiere_note'])
            except ValueError:
                print("Une erreur est survenue, probablement parce que le format de emotion_melodie['premiere_note'] est incorrect")
                print("TagError : ValueError/creation_notes/generer_note/1-140.21")
                exit()
        elif(note_precedante >= 0):
            note = tonique_actuelle + choice(choice(emotion_notes['accords'][indice_struct]))
    else:
        position = randint(0,2)
        try:
            orn_type = choice(emotion_notes['ornementations'][indice_struct])[position][0]
            note = tonique_actuelle + choice(choice(emotion_notes['ornementations'][indice_struct])[position][1:])
            value = orn_type + str(note) + str(tonique_actuelle)
            if(position > 3):
                print(value)
        except ValueError:
            print("Une erreur est survenue, probablement parce que le format de emotion_melodie['accords'] ou emotion_melodie['ornementations'] est incorrect")
            print("TagError : ValueError/creation_notes/generer_note/1-190.16")
            exit()
    return note, note_suivante
        


def variations_structure_melodique(structure_melodique, structure_rythmique, emotion_notes, indice_struct, variation):
    if(variation == 'i'):
        return structure_melodique
    elif(variation == 'r'):
        return generer_structure_melodique(structure_rythmique, indice_struct, emotion_notes)
    elif(variation[:2] == 'rt'):
        try:
            decalage = int(variation[2:])
        except ValueError:
            print("Un élement 'rt' de 'struct_globale' n'a probablement pas le bon format")
            print("TagError : ValueError/creation_notes/variations_structure_melodique/8-20.27")
        return transposition_gamme(structure_melodique, decalage)
    else:
        print("Un élement de 'struct_globale' n'a probablement pas le bon format, ou est manquant")
        print("TagError : ValueError/creation_notes/variations_structure_melodique/8-25.28")

