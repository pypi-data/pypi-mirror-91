#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import nltk
from word_lists import Contracted_word,Stop_words,neg_words
import pandas as pd
from nltk.corpus import stopwords  



class TextPreprocessing():
    def __init__(self,include_negative_words,replacement_word=None,stop_words=None):
        nltk.download("stopwords")
        self.include_negative_words=include_negative_words
        self.replacement_word=replacement_word
        self.stop_words=stop_words
        self.Contracted_word={k.lower():v.lower() for k,v in Contracted_word.items()}
    def replace_word(self):
        if self.replacement_word:
            z = {**self.Contracted_word, **self.replacement_word}
            return z
        else:
            return Contracted_word
    def remove_words(self):
        if self.stop_words:
            stop_=Stop_words.extend(self.stop_words)
            return stop_
        else:
            return Stop_words
    def text_preprocessing(self,data):
        
        STOP_WORDS=self.remove_words()
        STOP_WORDS=list(map(lambda x:x.lower(),Stop_words))
        if self.include_negative_words:
            pass
        else:
            STOP_WORDS=[word for word in STOP_WORDS if not word in neg_words]
        data=data.text.apply(lambda x:x.lower())
        data=data.replace(self.replace_word(),regex=True)
        
        Sents=[]
        for sentence in data:
            sent=re.sub('[^a-zA-Z]'," ",sentence)
            sent=sent.split()
            sent=[word for word in sent if not word in set(STOP_WORDS)]
            Sents.append(" ".join(sent))
        return Sents


