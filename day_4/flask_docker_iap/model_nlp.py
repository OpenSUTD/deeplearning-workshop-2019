import numpy as np
import keras
import pickle
import re
from nltk.corpus import stopwords
from keras import preprocessing

class sentiment_classifier(object):
    def __init__(self, model_file="cnn.h5"):
        self.model = keras.models.load_model(model_file)
        self.model._make_predict_function()
        self.classes = ["negative", "positive"]
        with open('tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)
        
    def predict(self, input_data):
        input_sequence = self.preprocess(input_data)
        preds = self.model.predict(input_sequence)
        pred = preds.argmax(axis=-1)
        output = self.classes[pred[0]]
        return output

    from nltk.corpus import stopwords
    def clean_text(text, remove_stopwords=True):
        output = ""
        text = str(text).replace("\n", "")
        text = re.sub(r'[^\w\s]','',text).lower()
        if remove_stopwords:
            text = text.split(" ")
            for word in text:
                if word not in stopwords.words("english"):
                    output = output + " " + word
        else:
            output = text
        return str(output.strip()).replace("  ", " ")

    def preprocess(self, input_data, MAX_SEQUENCE_LENGTH=30):
        input_string = self.clean_text(input_data)
        input_token = self.tokenizer.texts_to_sequences([input_string])
        processed_input = preprocessing.sequence.pad_sequences(input_token, padding='pre', maxlen=(MAX_SEQUENCE_LENGTH-5))
        processed_input = preprocessing.sequence.pad_sequences(processed_input, padding='post', maxlen=(MAX_SEQUENCE_LENGTH))
        return processed_input