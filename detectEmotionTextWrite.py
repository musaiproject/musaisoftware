# Fait afficher un écran pour rentrer du texte. 

import pygame
import sys
import Final_2
import creation_structure
import creation_notes
import detectEmotionTextRoberta

def jouer_musique(emotion, x, y):
    structure_morceau = creation_structure.creation_structure_rythmique_globale(emotion['emotion_structure'], emotion['emotion_rythme'])
    structure_finale = creation_notes.creation_structure_melodique_globale(structure_morceau, emotion['emotion_notes'])
    print(structure_finale['liste_finale'])
    Final_2.create_sound_generator(x,y,structure_finale['liste_finale'])




def WriteText():
    pygame.init()
    clock = pygame.time.Clock()
    # it will display on screen
    SIZE_LENGTH = 1200
    SIZE_HEIGHT = 250
    screen = pygame.display.set_mode([SIZE_LENGTH, SIZE_HEIGHT]) 
    # basic font for user typed
    base_font = pygame.font.Font(None, 32)
    pygame.display.set_caption('musai')
    icon = pygame.image.load('Musai_MiniLogo.png')
    pygame.display.set_icon(icon)

    # create rectangle
    input_rect = pygame.Rect(20, SIZE_HEIGHT/4, 100, 32)
    waiting_rect = pygame.Rect(400, 200, 1000, 32)
    # color_active stores color(lightskyblue3) which
    # gets active when input box is clicked by user
    color_active = pygame.Color(210,210,210)
    color_passive = pygame.Color(0,0,0)
    jauneMusai = pygame.Color(255,242,40) # La couleur choisie est le même jaune que celui du logo
    color = color_passive
    active = False

    user_text = ""
    emotion1, emotion2 = "", ""

    file = open("registered_messages.txt",'a')
  
    while True:
        for event in pygame.event.get():
        # if user types QUIT then the screen will close
            if event.type == pygame.QUIT:
                file.close()
                pygame.quit()
                sys.exit()
  
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
  
            if event.type == pygame.KEYDOWN:
            # Check for backspace
                if event.key == pygame.K_BACKSPACE:
                # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
                elif event.key == pygame.K_RETURN:
                    screen.blit(base_font.render("stop pressing keys and listen to the music please", True, jauneMusai),(2*SIZE_LENGTH/5, 2*SIZE_HEIGHT/3))
                    pygame.display.flip()
                    # main part
                    emotion_str = detectEmotionTextRoberta.DetectEmotion(user_text)
                    emotion_str2 = Final_2.associer_emotion(emotion_str)
                    print(emotion_str)
                    x,y,emotion = Final_2.get_emotion_coordinates(emotion_str2)
                    print(x)
                    print(y)
                    print(emotion)
                    jouer_musique(emotion, x, y)
                    file.write('message  :  ' + user_text + '\nemotion  :  ' + emotion1 + ', ' + emotion2 + '\n\n')
                    pygame.event.clear()
                    user_text = ""
                else:
                    if input_rect.w < 1160: user_text += event.unicode

        # it will set background color of screen
        screen.fill((255, 255, 255))
  
        if active:
            color = color_active
        else:
            color = color_passive
        pygame.draw.rect(screen, color, input_rect)
        text_surface = base_font.render(user_text, True, (0, 0, 0))
        # render at position stated in arguments
        screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
     
        # set width of textfield so that text cannot get
        # outside of user's text input
        input_rect.w = max(100, text_surface.get_width()+10)
      
        # display.flip() will update only a portion of the
        # screen to updated, not full area
        pygame.display.flip()
      
        # clock.tick(60) means that for every second at most
        # 60 frames should be passed.
        clock.tick(60)
