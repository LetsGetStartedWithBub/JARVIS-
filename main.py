"""
Installations:
pip install nltk
pip install newspaper3k
pip install numpy
pip install sklearn
pip install pyttsx3
pip install py-espeak-ng
pip install pywin32
"""

"""Import Libraries"""

import random
import nltk
import string
import numpy as np
from newspaper import Article
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pyttsx3 as pp
from espeakng import ESpeakNG
import warnings
warnings.filterwarnings('ignore')

"""Download Punkt Package"""

nltk.download('punkt',quiet=True)

# This is the part where we are going to convert text output into audio
"""Import pyttsx3"""

engine = pp.init()
voices = engine.getProperty('voices')
# getting details of current voice
print(voices)
engine.setProperty('voice', voices[0].id)


def speak(word):
  engine.say(word)
  engine.runAndWait()

"""Get the articles from the webpage"""
#List of all the possible input
input_list = [['taj', 'taj mahal', 'what is taj mahal', 'where is taj mahal', 'agra taj mahal'],
              ['humanyun','humayun tomb','humanyun tomb delhi'],
              ['khajuraho', 'khajuraho temple', 'khajuraho group of munuments', 'khajuraho mp'],
              ['ajanta', 'ajanta caves'],
              ['ellora', 'ellora caves']]

#Dictionary of all the articles
article_dictionary ={0 :'https://en.wikipedia.org/wiki/Taj_Mahal',
                     1 :'https://en.wikipedia.org/wiki/Humayun%27s_Tomb',
                     2 :'https://en.wikipedia.org/wiki/Khajuraho_Group_of_Monuments',
                     3 :'https://en.wikipedia.org/wiki/Ajanta_Caves',
                     4 :'https://en.wikipedia.org/wiki/Ellora_Caves'}

#Function to match user's input to the list of possible inputs
def match_input(user_input):
  user_input = user_input.lower()
  for i,count in enumerate(input_list):
    for j in count:
      if j == user_input:
        b = article_dictionary[i]
        a = Article(b)
        a.download()
        a.parse()
        a.nlp()
        corpus = a.text
        text = corpus
        sentence_list = nltk.sent_tokenize(text)
        return sentence_list

"""Function for greeting responses"""

def greeting_responses(text):
  # firstly we'll convert the inputed text into lower form
  text = text.lower()
  #Jarvis Greetings
  jarvis_greetings=['hi this is jarvis....how can i help u..?', 'hi jarvis there','hey ...how jarvis can help u...', 'hello', 'hi', 'hi there', 'hola', 'howdy', 'hey', 'hey there....', 'holaaa...']
  #user Greetings
  user_greetings = ['hello', 'hi', 'hi there', 'holaa...', 'howdy', 'hey', 'hey there', 'hellooooo', 'hiiiii']

  for words in text.split():
    if words in user_greetings:
      return random.choice(jarvis_greetings)

"""Function for checking the highest index value in the similarity score list"""

def index_sort(list_var):
  #length is the similarity score list
  length = len(list_var)
  list_index = list(range(0, length))

  x = list_var
  for i in range(length):
    for j in range(length):
      if x[list_index[i]] > x[list_index[j]]:
        #Swaping
        temp = list_index[i]
        list_index[i] = list_index[j]
        list_index[j] = temp

  return list_index

"""Function for jarvis responses"""

def jarvis_responses(user_input,sentence_list1):
  user_input = user_input.lower()
  sentence_list1.append(user_input)
  jarvis_response = ''
  cm = CountVectorizer().fit_transform(sentence_list1)
  similarity_score = cosine_similarity(cm[-1], cm)
  similarity_score_list = similarity_score.flatten()
  index = index_sort(similarity_score_list)
  index = index[1:]
  response_flag = 0

  j = 0
  for i in range(len(index)):
    if similarity_score_list[i] > 0.0:
      jarvis_response = jarvis_response + ' ' + sentence_list1[index[i]]
      response_flag = 1
      j += 1

      if j > 2:
        break

  if response_flag == 0:
    jarvis_response = jarvis_response +' '+"I apologies, i don't understand."
    jarvis_response = str(jarvis_response)
  sentence_list1.remove(user_input)

  return jarvis_response

print("JARVIS : Hi , I am JARVIS ..............How can I help you ? .................If you want to quit type bye or quit...........")

exit_list = ['exit', 'bye', 'quit', 'break']
while(True):
  user_input = input()
  if user_input.lower() in exit_list:
    print("JARVIS : Nice meeting you :)")
    speak("Nice meeting you")
    break
  else:
    if greeting_responses(user_input) != None:
      print("JARVIS : "+greeting_responses(user_input))
      speak(greeting_responses(user_input))
    else:
      sentence_list1 = match_input(user_input)
      print("JARVIS : "+jarvis_responses(user_input,sentence_list1))
      speak(jarvis_responses(user_input,sentence_list1))


