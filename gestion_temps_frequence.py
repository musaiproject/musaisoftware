# ID 7
import numpy as np


Do = [32.70,65.41,130.81,261.63,523.25,1046.50,2093.00,4186.01,8372.02,16744.04]
Do_d = [34.65,69.30,138.59,277.18,554.37,1108.73,2217.46,4434.92,8869.84,17739.68]
Re = [36.71,73.42,146.83,293.66,587.33,1174.66,2349.32,4698.64,9397.28,18794.56]
Re_d = [38.89,77.78,155.56,311.13,622.25,1244.51,2489.02,4978.03,9956.06,19912.12]
Mi = [41.20,82.41,164.81,329.63,659.26,1318.51,2637.02,5274.04,10548.08,21096.16]
Fa = [43.65,87.31,174.61,349.23,698.46,1396.91,2793.83,5587.65,11175.30,22350.60]
Fa_d = [46.25,92.50,185.00,369.99,739.99,1479.98,2959.96,5919.91,11839.82,23679.64]
Sol = [49.00,98.00,196.00,392.00,783.99,1567.98,3135.96,6271.93,12543.86,25087.72]
Sol_d = [51.91,103.83,207.65,415.30,830.61,1661.22,3322.44,6644.88,13289.76,26579.52]
La = [55.00,110.00,220.00,440.00,880.00,1760.00,3520.00,7040.00,14080.00,28160.00]
La_d = [58.27,116.54,233.08,466.16,932.33,1864.66,3729.31,7458.62,14917.24,29834.48]
Si = [61.74,123.47,246.94,493.88,987.77,1975.53,3951.07,7902.13,15804.26,31608.52]


Notes = np.array([Do, Do_d, Re, Re_d, Mi, Fa, Fa_d, Sol, Sol_d, La, La_d, Si])


def generer_frequence(note, liste_gamme, longueur_gamme, fondamentale, hauteur_moyenne, Notes):
    ind_note = liste_gamme[note % longueur_gamme] + fondamentale
    hauteur = hauteur_moyenne + (note//longueur_gamme)
    try:
        freq = Notes[ind_note % 12][hauteur + ind_note//12]
    except IndexError:
        print("Une erreur à eu lieu, parce que la hauteur des notes a dépassé la hauteur max. ou min.")
        print("La hauteur va être automoatiquement corrigée, mais certaines notes pourraient ne pas correspondre à ce que vous vouliez")
        print("TagError : IndexError/gestion_temps_frequence/generer_frequence/7-50.20")
        if(hauteur + ind_note//12 > 9):
            hauteur = 9
        elif(hauteur + ind_note//12 < 0):
            hauteur = 0
        else:
            print("L'erreur n'a pas pu être corrigée")
            print("TagError : InternalError/gestion_temps_frequence/generer_frequence/7-55.21")
            exit()
        freq = Notes[ind_note % 12][hauteur]
    return freq


def duree_rythme(rythme, tempo):
    return (rythme/8)*60000/tempo


def conversion_temps_frequence(structure_melodique_norm, emotion_notes, fondamentale, tempo):
    part_liste_finale = []
    liste_gamme = emotion_notes['liste_gammes']
    longueur_gamme = len(liste_gamme)
    hauteur_moyenne = emotion_notes['hauteur_moyenne']
    for note_rythme in structure_melodique_norm:
        freq = generer_frequence(note_rythme[0], liste_gamme, longueur_gamme, fondamentale, hauteur_moyenne, Notes)
        duree = duree_rythme(note_rythme[1], tempo)
        part_liste_finale.append([int(freq),int(duree)])
    return part_liste_finale







#     liste = [[0,4],[1,4],[2,4],[0,4],[0,4],[1,4],[2,4],[0,4],[2,4],[3,4],[4,8],[5,4],[6,4],[7,8],[7,4],[8,4],[9,4],[7,4],[-7,4],[-6,4],[-5,4],[-7,4]]
