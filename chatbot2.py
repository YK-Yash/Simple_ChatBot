# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 09:55:04 2018

@author: Dell
"""

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.trainers import ListTrainer

import pandas as pd

# Importing the dataset
dataset = pd.read_csv('student_dataset.csv', sep=',')

d_sex = dataset['Sex']
d_age = dataset['Age']
d_regno = dataset['RegNo']
d_name = dataset['Name']
d_marks = dataset['Marks']
d_mobno = dataset['MobNo']

# Create a new instance of a ChatBot
bot = ChatBot(
    "Terminal",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[
            "chatterbot.logic.MathematicalEvaluation",
        {
            'import_path': 'chatterbot.logic.BestMatch'
            
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.50,
            'default_response': 'I am sorry, but I do not understand.'
        }
    ],
    input_adapter="chatterbot.input.TerminalAdapter",
    output_adapter="chatterbot.output.TerminalAdapter"
)

lowest_name = ''
lowest_regno = ''
topper_name = ''
topper_regno = ''
no_of_failures = 0
failures = ''
no_of_people_90 = 0

for i in range(0,len(d_marks)):
    if d_marks[i] == min(d_marks):
        lowest_name = d_name[i]
        lowest_regno = d_regno[i]
        
    if d_marks[i] == max(d_marks):
        topper_name = d_name[i]
        topper_regno = d_regno[i]
    
    if d_marks[i] < 40:
        no_of_failures = no_of_failures + 1
        failures = failures + ', '+ d_name[i] +' ('+d_regno[i]+')'
        
    if d_marks[i] >= 90:
        no_of_people_90 = no_of_people_90 + 1


bot.set_trainer(ChatterBotCorpusTrainer)
bot.train("chatterbot.corpus.english")
bot.set_trainer(ListTrainer)
for i in range(0,len(d_marks)):
    
    bot.train([
            "Give me the complete details of {}".format(d_regno[i]),
            "\nHere are the details:Registeration No.: {}; Name: {}  Age: {}  Sex: {}  Marks: {}  Mobile No.: {}".format(d_regno[i], d_name[i], d_age[i], d_sex[i], d_marks[i], d_mobno[i]),
            "complete details of {}".format(d_regno[i]),
            "\nHere are the details:Registeration No.: {}; Name: {}  Age: {}  Sex: {}  Marks: {}  Mobile No.: {}".format(d_regno[i], d_name[i], d_age[i], d_sex[i], d_marks[i], d_mobno[i]),
    ])
    
    bot.train([
        "what is the marks of {}".format(d_regno[i]),
        "Marks of {} - {} is {}".format(d_regno[i], d_name[i], d_marks[i]),])
    bot.train([
        "what is the age of {}".format(d_regno[i]),
        "Age of {} - {} is {}".format(d_name[i], d_regno[i], d_age[i]),])
    bot.train([
        "what is the mobile number of {}".format(d_regno[i]),
        "Mobile number of {} - {} is {}".format(d_regno[i], d_name[i], d_mobno[i]),])
    bot.train([
        "what is the marks of {}".format(d_name[i]),
        "I prefer Registeration numbers.. Since you have been good to me, I'll show the results : Marks of {} - {} is {}".format(d_regno[i], d_name[i], d_marks[i]),])
    bot.train([
        "what is the age of {}".format(d_name[i]),
        "I prefer Registeration numbers.. Since you have been good to me, I'll show the results :Age of {} - {} is {}".format(d_name[i], d_regno[i], d_age[i]),
        ])
    bot.train([
        "what is the mobile number of {}".format(d_name[i]),
        "I prefer Registeration numbers.. Since you have been good to me, I'll show the results :Mobile number of {} - {} is {}".format(d_regno[i], d_name[i], d_mobno[i]),
    ])

bot.train([
  "what is the class average?",
   "The class average is {}".format(sum(d_marks)/len(d_marks))
])    
    
bot.train([
  "what is the lowest marks?",
   "The Lowest marks is {}".format(min(d_marks))
])    

bot.train([
  "how many failures?",
  "These many guys got below 40 {}".format(no_of_failures)
])

bot.train([
  "who all failed?",
  "Sad.. But these people could'nt cross 40  {}".format(failures)
])
    
bot.train([
  "what is the highest marks?",
  "The highest marks is {}".format(max(d_marks))
])

bot.train([
  "who got the highest marks?",
  "The highest marks is {}, obtained by {} - {}".format(max(d_marks), topper_name, topper_regno)
])
    
bot.train([
  "who got the lowest marks?",
  "The lowest marks is {}, obtained by {} - {} - Feel sad for the chap".format(min(d_marks), lowest_name, lowest_regno)
])    

bot.train([
   "Who all got above 90"
   "{}".format(no_of_people_90)
        ])
    
bot.train("chatterbot.corpus.english")

CONVERSATION_ID = bot.storage.create_conversation()


def get_feedback():
    from chatterbot.utils import input_function

    text = input_function()

    if 'yes' in text.lower():
        return False
    elif 'no' in text.lower():
        return True
    else:
        print('Please type either "Yes" or "No"')
        return get_feedback()


print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nHi, I'm Silence - The Chatbot\nHere to help!\n\n")
from chatterbot.utils import input_function

while True:
    try:
        input_statement = bot.input.process_input_statement()
        statement, response = bot.generate_response(input_statement, CONVERSATION_ID)
        bot.output.process_response(response)
        print('\n')
       
    except (KeyboardInterrupt, EOFError, SystemExit):
        break