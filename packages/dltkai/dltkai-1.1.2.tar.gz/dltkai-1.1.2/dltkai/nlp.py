import base64
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import pandas as pd
import spacy
from spacy import displacy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import pickle
import time
import warnings
warnings.filterwarnings("ignore")
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
import numpy as np
import string
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import load_model
import tensorflow as tf
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer

nlp = spacy.load('en_core_web_sm')


def clean_text(text):
    try:
        text = text.translate(string.punctuation)
        text = text.lower().split()
        stops = set(stopwords.words("english"))
        text = [w for w in text if not w in stops and len(w) >= 3]
        text = " ".join(text)
        text = re.sub(r"[^A-Za-z0-9^,!.\/'+-=]", " ", text)
        text = re.sub(r"what's", "what is ", text)
        text = re.sub(r"\'s", " ", text)
        text = re.sub(r"\'ve", " have ", text)
        text = re.sub(r"n't", " not ", text)
        text = re.sub(r"i'm", "i am ", text)
        text = re.sub(r"\'re", " are ", text)
        text = re.sub(r"\'d", " would ", text)
        text = re.sub(r"\'ll", " will ", text)
        text = re.sub(r",", " ", text)
        text = re.sub(r"\.", " ", text)
        text = re.sub(r"!", " ! ", text)
        text = re.sub(r"\/", " ", text)
        text = re.sub(r"\^", " ^ ", text)
        text = re.sub(r"\+", " + ", text)
        text = re.sub(r"\-", " - ", text)
        text = re.sub(r"\=", " = ", text)
        text = re.sub(r"'", " ", text)
        text = re.sub(r"(\d+)(k)", r"\g<1>000", text)
        text = re.sub(r":", " : ", text)
        text = re.sub(r" e g ", " eg ", text)
        text = re.sub(r" b g ", " bg ", text)
        text = re.sub(r" u s ", " american ", text)
        text = re.sub(r"\0s", "0", text)
        text = re.sub(r" 9 11 ", "911", text)
        text = re.sub(r"e - mail", "email", text)
        text = re.sub(r"j k", "jk", text)
        text = re.sub(r"\s{2,}", " ", text)
        return text
    except Exception as e:
        print("Exception generated inside clean_text method in "+os.getcwd()+'/dltkai/nlp.py -',e.args)


class NaturalLanguage:

    def pos_tagger(params):
        try:
            text = params
            doc = nlp(text)
            response = {}
            pos_response = {}
            for token in doc:
                pos_response[token.text] = token.tag_
            response["result"] = pos_response
            response["text"] = text
            return response
        except Exception as e:
            print("Exception generated inside pos_tagger method in "+os.getcwd()+'/dltkai/nlp.py -',e.args)


    def ner_tagger(params):
        try:
            text = params
            doc = nlp(text)
            response = {}
            ner_response = {}
            person_details = []
            org_details = []
            for ent in doc.ents:
                ner_response[str(ent)] = ent.label_
            response["result"] = ner_response
            response["text"] = text
            response["persons"] = person_details
            response["organizations"] = org_details
            return response
        except Exception as e:
            print("Exception generated inside ner_tagger method in "+os.getcwd()+'/dltkai/nlp.py -',e.args)


    def dependency_parser(params):
        try:
            text = params
            doc = nlp(text)
            response = {}
            dependency_response = {}
            for token in doc:
                dependency_response[str(token.text)] = {"dep": token.dep_,
                                                        "headText": token.head.text,
                                                        "headPOS": token.head.pos_,
                                                        "children": [str(child) for child in token.children]
                                                        }
            response["result"] = dependency_response
            response["text"] = text
            return dependency_response
        except Exception as e:
            print("Exception generated inside parser method in "+os.getcwd()+'/dltkai/nlp.py -',e.args)

    def decode_sentiment(score, include_neutral=True):
    # SENTIMENT
        POSITIVE = "POSITIVE"
        NEGATIVE = "NEGATIVE"
        NEUTRAL = "NEUTRAL"
        SENTIMENT_THRESHOLDS = (0.4, 0.7)
        if include_neutral:
            label = NEUTRAL
            if score <= SENTIMENT_THRESHOLDS[0]:
                label = NEGATIVE
            elif score >= SENTIMENT_THRESHOLDS[1]:
                label = POSITIVE

            return label
        else:
            return NEGATIVE if score < 0.5 else POSITIVE


    def toxic_comment_detect(text):
        try:
            maxlen = 50
            embed_dim = 100
            max_words = 20000
            text=clean_text(str(text))
            #print(type(text))
            with open('resources/tokenizer.pickle', 'rb') as handle:
                tokenizer = pickle.load(handle)
            ls=[]
            ls.append(text)
            data = tokenizer.texts_to_sequences(ls)
            #print('tokenized data-',data)
            data = pad_sequences(data, maxlen=maxlen, padding='post')
           # print('padded-seq',data)
            model=load_model('resources/Cyber_bullying-LSTM-multi-class')
            res=NaturalLanguage.sentiment_detect(text)
            comment_state=res['emotion']
            tagged_words=res['text']
            sample='no discernable type'
            #if res['emotion']=='NEGATIVE':
            #    pred=model.predict(data)
            dt={}
            if res['emotion']=='NEGATIVE':
                pred=model.predict(data)
                if np.argmax(pred)==1:
                    sample='racism'
                elif np.argmax(pred)==2:
                    sample='sexism'
            dt['state']=comment_state
            dt['tagged_words']=tagged_words
            dt['toxic_comment_type']=sample
            #else:
            #    print("not detected")
            
            dt['state']=comment_state
            dt['tagged_words']=tagged_words
            dt['cyber_bullying_type']=sample

            return dt

        except Exception as e:
            print("Exception generated inside toxic_comment_detect method in "+os.getcwd()+'/dltkai/nlp.py -',e.args)


    def detect_tonality(text):
        model1 = pd.read_pickle(r'resources/tonality_model.pickle')
        with open(os.getcwd()+'/resources/tonality_vect.pickle', 'rb') as handle:
            vect1 = pickle.load(handle)

        #Testing HAM and SPAM Predection text
        print("lets test whether text is HAM or SPAM: ")
        t=np.array([text])
        print(t)
        t=vect1.transform(t)
        prediction = model1.predict(t)
        if prediction == 0:
            return "HAM!"
        else:
            return "SPAM!"


    def sentiment_detect(params):
        try:
            text = params
            sid = SentimentIntensityAnalyzer()
            scores = sid.polarity_scores(text)
            response = {}
            if scores["compound"] > 0:
                emotion = "POSITIVE"
                polarity = 3
            elif scores["compound"] < 0:
                emotion = "NEGATIVE"
                polarity = 1
            else:
                emotion = "NEUTRAL"
                polarity = 0
            response["emotion"] = emotion
            response["text"] = text
            response["polarity"] = polarity
            response["scores"] = scores
            return response
        except Exception as e:
            print("Exception generated inside sentiment method in "+os.getcwd()+'/dltk_ai/nlp.py -',e.args)


    def sarcasm_detect(text):
        with open(os.getcwd()+'/resources/sarcasm_tfidf.pickle', 'rb') as handle:
            tf_idf = pickle.load(handle)
        with open(os.getcwd()+'/resources/sarcasm_mnb.pickle', 'rb') as handle:
            mnb = pickle.load(handle)

        test = tf_idf.transform([text])
        if mnb.predict(test)[0]==1:
            return 'Sarcastic'
        else:
            return 'Non sarcastic'

"""
    def sentiment_analysis(text):
        try:
            maxlen = 50
            #embed_dim = 100
            #max_words = 20000
            print('inside detect function before cleaning')
            text=clean_text(str(text))
            print(text)
            print(type(text))
            with open(os.getcwd()+'/resources/tokenizer_sentiment.pkl', 'rb') as handle:
                tokenizer = pickle.load(handle)
            ls=[]
            ls.append(text)
            data = tokenizer.texts_to_sequences(ls)
            #print('tokenized data-',data)
            start_at = time.time()
            data = pad_sequences(data, maxlen=maxlen, padding='post')
            #print('padded-seq',data)
            model=load_model(os.getcwd()+'/resources/model_sentiment.h5')
            score=model.predict(data)
            include_neutral = True
            label = self.decode_sentiment(score, include_neutral=include_neutral)
            return {"label": label, "score": float(score), "elapsed_time": time.time()-start_at}

        except Exception as e:
            print("Exception generated inside toxic_comment_detect method in "+os.getcwd()+'/dltkai/nlp.py -',e.args)
"""
