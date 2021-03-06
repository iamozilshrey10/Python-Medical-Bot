# -*- coding: utf-8 -*-
"""Chat_gui.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LBpvX_ob4Y7WKW8V47alVv4ngkCTfPbe
"""

# Importing Modules 

import nltk
from nltk.stem import WordNetLemmatizer 
lemmatizer = WordNetLemmatizer()

import numpy as np
import pickle 
import random

from keras.models import load_model 
model = load_model('chat_model.h5')

import json
intents = json.loads(open('intents.json').read())
words = pickle.load(open('Words.pkl','rb'))
classes = pickle.load(open('Classes.pkl','rb'))

#Perfrom Text Preprocessing and Predicting the Class 

def clean_sentence(sentence):
  sentence_words = nltk.word_tokenize(sentence)  #Splitting words into array
  sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
  return sentence_words

def bag_of_words(sentence, words, show_details = True):
  sentence_words = clean_sentence(sentence)
  bow = [0] * len(words)
  for s in sentence_words:
    for i,w in enumerate(words):
      if w == s:
        bow[i] == 1
        if show_details:
          print("Found : %s" % w)
  retrun(np.array(bow))

def predict_class(sentence, model):
  p = bag_of_words(sentence, words, show_details=False)
  r = model.predict(np.array([p]))[0]
  err_thresh = 0.25
  results = [[i,r] for i,r in enumerate(r) if r>err_thresh]
  results.sort(key=lambda x:x[1], reverse =True)
  return_list = []
  for r in results:
    return_list.append ({"intent" : classes[r[0]], "probability" : str(r[1])})
  return return_list

#Getting random response from intents 

def get_res(ints, intents_json):
  tag = ints[0]['intent']
  list_of_intents = intents_json['intent']
  for i in list_of_intents:
    if i['tag'] == tag:
      result = random.choice(i['responses'])
      break
  return result  

def chat_res(text):
  ints = predict_class(text, model)
  res = get_res(ints, intents)
  return res

#Building the GUI with tkinter 

import tkinter
from tkinter import *

def send():
  msg = EntryBox.get("1.0",'end-1c').strip()
  EntryBox.delete("0.0", END)

  if msg != '':
    ChatLog.config(state=NORMAL)
    ChatLog.insert(END, "You : " + msg + '\n\n')
    ChatLog.config(foreground = "#442265", font =("Verdana", 12))

    res = chat_res(msg)
    ChatLog.insert(END, "Bot : " + res + '\n\n')
    ChatLog.config(state=DISABLED)
    ChatLog.yview(END)

base = Tk()
base.title("Hello")
base.geometry("400x500")
base.resizable(width=FALSE, height=FALSE)

#Create Chat window

ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial",)
ChatLog.config(state=DISABLED)

#Bind scrollbar to Chat window

scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

#Create Button to send message

SendButton = Button(base, font=("Verdana",12,'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#32de97", activebackground="#3c9d9b",fg='#ffffff',
                    command= send )

#Create the box to enter message

EntryBox = Text(base, bd=0, bg="white",width="29", height="5", font="Arial")
#EntryBox.bind("<Return>", send)

#Place all components on the screen

scrollbar.place(x=376,y=6, height=386)
ChatLog.place(x=6,y=6, height=386, width=370)
EntryBox.place(x=128, y=401, height=90, width=265)
SendButton.place(x=6, y=401, height=90)
base.mainloop()