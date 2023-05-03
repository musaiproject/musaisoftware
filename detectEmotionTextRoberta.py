from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline


tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")
model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")
emotion = pipeline('text-classification', model = 'arpanghoshal/EmoRoBERTa')

#Renvoie des émotions correspondant à Text en entrée
def DetectEmotion(Text):
    emotion_labels = emotion(Text)
    return emotion_labels[0]['label']



