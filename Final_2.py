import numpy as np
import math
from pyo import *
import random
from generation_melodie import pride, fear, sadness, annoyance, neutral, funny
# fonction qui renvoie dans quel quadrant se situe l'emotion 

def pos_quadrant(x,y) :
    if x > 0 and y > 0:
        return 1
    elif x < 0 and y > 0:
        return 2
    elif x < 0 and y < 0:
        return 3
    elif x > 0 and y < 0:
        return 4
    else:
        return 0 
    
def midi_to_hz(midi_notes):
    """
    Convertit une liste de notes MIDI en fréquences en Hz.
    """
    frequencies = []
    for midi_note in midi_notes:
        frequency = 440 * math.pow(2, (midi_note - 69) / 12)
        frequencies.append(frequency)
    return frequencies

def get_emotion_coordinates(emotion):
    if emotion == 'funny':
        return (0.4, 0.8,funny)
    elif emotion == 'pride':
        return (0.5, 0.5,pride)
    elif emotion == 'fear':
        return (-0.8, 0.2,fear)
    elif emotion == 'sadness':
        return (-0.7, -0.5,sadness)
    elif emotion == 'annoyance':
        return (-0.8, 0.9,annoyance)
    elif emotion == 'neutral':
        return (0, 0,neutral)
    else:
        return (0, 0,neutral)
    


def associer_emotion(emotion):
    emotions_cibles = {
        'admiration': 'pride',
        'amusement': 'funny',
        'anger': 'annoyance',
        'annoyance': 'annoyance',
        'approval': 'joy',
        'caring': 'joy',
        'confusion': 'neutral',
        'curiosity': 'joy',
        'desire': 'joy',
        'disappointment': 'sadness',
        'disapproval': 'annoyance',
        'disgust': 'annoyance',
        'embarrassment': 'sadness',
        'excitement': 'joy',
        'fear': 'fear',
        'gratitude': 'joy',
        'grief': 'joy',
        'joy': 'joy',
        'love': 'pride',
        'nervousness': 'fear',
        'optimism': 'pride',
        'pride': 'pride',
        'realization': 'neutral',
        'relief': 'joy',
        'remorse': 'sadness',
        'sadness': 'sadness',
        'surprise': 'neutral',
        'neutral': 'neutral'
    }
    return emotions_cibles.get(emotion)



def create_sound_generator (x,y,A) :

    s = Server(nchnls=0,audio='embedded').boot()
    #variables
    freq1 = [200,301]
    quad = pos_quadrant(x,y)
    #choix d'un generateur de son 
    #gestion pattern
    t=[duration[1] for duration in A]
    f=[frequences[0] for frequences in A]
    env = LinTable([(0,0),(100,1),(500,.5),(8192,0)])
   
    pits=f
    durs = t
    time_seq = [(i / .125)/1000 for i in durs]
    # trigger sequence base on duration sequence
    #seq = Seq(time=.125, seq=time_seq, poly=4).play()
    # get pitch and duration from lists (.mix(1) to avoid duplication)
    seq = Seq(time=.125, seq=time_seq, poly=4).play()
    freq1 = Iter(seq.mix(1), choice=pits)
    dur = Iter(seq.mix(1), choice=durs)
    amp = TrigEnv(seq, table=env, dur=dur, mul=.9)


    if quad == 1 : # choix JP saw / HAPPY ; JOYOUS ; INTERESTED , FEELING SUPERIOR 
           
        #paramètres x : [0,1] ; y : [0,1]
        
        #######enveloppe######
        #env = Adsr(attack=y/100, decay=y, sustain=y*10, release=y*10, dur=2, mul=0.8)

        # generation de son 
        
        lfo4 = Sine(float(np.exp(2*x))).range(0.5, 0.6)
        gen = SuperSaw(freq=freq1, detune=lfo4, bal = 0.8, mul=amp)

        ######fx#########

        #harm
        if x > 0.5 :
            gen = Harmonizer(gen, transpo=5, feedback = x-0.2, winsize=0.1)
        else :
            gen = Harmonizer(gen, transpo=-12, feedback = x, winsize=1)
            
        #reverb

        gen = WGVerb(gen, feedback=[x-.1,x+.1], cutoff=8000, bal=.35, mul=.3)
        

        #filtrage
        freq=Sig(y*10000)
        gen = ButLP(gen, freq)


    elif quad == 2 : # choix CrossFm ANGRY , ANNOYED , DISTRESSED 

         #y =[0 : 1] ; x =[0;-1]

        #####enveloppe######
        #env = Adsr(attack=0.1, decay=.2, sustain=.5, release=.1, dur=2, mul=.5)

        #####generation de son#####
        lfo = Sine(0.2).range(0, 1)
        [X,Y]= ChenLee(pitch=0.4, chaos=lfo, stereo = True)
        gen = CrossFM(carrier=freq1, ratio=[1.5, 1.49], ind1=X, ind2=Y, mul=amp)
        #####fx########
        
        if -x>0.2 :
            gen = Harmonizer(gen, transpo=9, feedback = -x-0.2, winsize=0.1)
        elif -x > 0.5:
             gen = Harmonizer(gen, transpo=-7, feedback = -x-0.2, winsize=0.1)
        
        
        gen = WGVerb(gen, feedback=[0.8,0.8], cutoff=8000, bal=.35, mul=1)
        gen = Disto(gen,drive = -x-.25)

    
    elif quad == 3 : # choix Blits SAD, GLOOMY, BORED, DROPY, 
         
        #[x,y]--> [0,-1]
        #  
        #######enveloppe######
        #env = Adsr(attack=0.8, decay=.2, sustain=.5, release=.9, dur=1, mul=.5)

        #####generation de son#######
        a=Phasor(freq=-x*500)
        lf2 = Sin(a, mul =30,add=20)
        gen = Blit(freq=freq1, harms=lf2, mul=amp)

        #######FX########
        gen = WGVerb(gen, feedback=[0.85,0.84], bal=1, mul=1)
        gen = SmoothDelay(gen,-x,-x,-x/10)
        #gen = Harmonizer(gen, transpo=8, feedback = -x-0.2, winsize=0.3)

        #filtrage
        #freq = Sig(1000/(-y*2))
        #gen = ButLP(gen, freq)

    elif quad == 4  : # choix Sine wave ATTENTIVE, CONFIDENT, HOPEFULL 
        ######enveloppe########
        #env = Adsr(attack=0.1, decay=.2, sustain=.5, release=.1, dur=2, mul=.5)
        lf1 = Sine(freq=[0.1, 0.15], mul=100, add=25)
        lf2 = Sine(freq=[0.18, 0.13], mul=0.4, add=1.5)
        lf3 = Sine(freq=[0.07, 0.09], mul=5, add=6)
        ####generation de son#####
        gen = Sine(freq=freq1, mul=amp)
       
       #######fx##########
        gen = WGVerb(gen, feedback=[.6,.7], cutoff=8000, bal=.65, mul=.7)

        gen = Phaser(gen, freq=lf1, spread=lf2, q=lf3, num=8, mul=0.5).out()
        
    


    else : #choix sin pure
        
        ######enveloppe########
        #env = Adsr(attack=.01, decay=.2, sustain=.5, release=.1, dur=2, mul=.5)

        ####genration de son#####
        gen = Sine(freq=freq1, mul=amp)
        #######fx##########
        gen = WGVerb(gen, feedback=[.7,0.8], cutoff=8000, bal=.35, mul=.3)

    gen.out()

    gen.out()
    s.start()
    time.sleep(30)
    s.stop()
    
    
#if __name__=="__main__":
#	A = [[440,500],[220,500]]
#	create_sound_generator(0.5,0.5,A)
#	print("Default input device: %i" % pa_get_default_input())
#	print("Default output device: %i" % pa_get_default_output())
#	print("Audio host APIS:")
#	pa_list_host_apis()
#	pa_list_devices()

