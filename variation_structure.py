


def transposition_gamme(structure_melodique, decalage):
    nouv_structure_melodique = []
    for note_rythme in structure_melodique:
        nouv_structure_melodique.append([note_rythme[0]+decalage, note_rythme[1]])
    return nouv_structure_melodique
