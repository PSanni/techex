from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher

import sqlite3
import os

# to store the contact form info in database
def DataUpdate(Name, Contact, Subject):

    # path of the database
    mydb = sqlite3.connect('..\contacts.db')
    mycursor = mydb.cursor()

    mycursor.execute('CREATE TABLE IF NOT EXISTS contact_info(name, contact, subject)')
    sql = 'INSERT INTO contact_info(name, contact, subject) VALUES ("{0}","{1}","{2}");'.format(Name, Contact, Subject)
    mycursor.execute(sql)
    
    # print(mycursor.rowcount, "record updated")
    mydb.commit()
    mydb.close()

# if __name__ == "__main__":
#     DataUpdate("Harsh", "harshpraj80@gmail.com", "Talk about chatbots")


# to store chat in 'csv' file
def SaveChat(conv):
    # if chat.csv file not there
    if not os.path.isfile('chats.csv'):
        with open('chats.csv', 'w', encoding='utf-8') as file:
            file.write("intent,user_input,entity_name,entity_value,action,bot_reply\n")

    chat_data=''

    for i in conv:
        # chat by user
        if i['event'] == 'user':
            chat_data += i['parse_data']['intent']['name'] + ',' + i['text'] + ','
            #print('user: {}'.format(i['text']))

            # if any entity present in message
            if len(i['parse_data']['entities']) > 0:
                chat_data += i['parse_data']['entities'][0]['entity'] + ',' + i['parse_data']['entities'][0]['value'] + ','
                #print('extra data:', i['parse_data']['entities'][0]['entity'], '=', i['parse_data']['entities'][0]['value'])
            # if no entities present in message, simply add two commas
            else:
                chat_data += ",,"

        # chat by bot
        elif i['event'] == 'bot':
            #print('Bot: {}'.format(i['text']))
            try:
                chat_data += i['metadata']['utter_action'] + ',' + i['text'] + '\n'
            except KeyError:
                pass

    # if file already there then append to it
    else:
        with open('chats.csv', 'a', encoding='utf-8') as file:
            file.write(chat_data)
    #print(chat_data)

###########################################
############ CUSTOM ACTIONS ###############

class ActionContactConfirm(Action):

    def name(self) -> Text:
        return "action_contact_confirm"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        DataUpdate(tracker.get_slot("name"),tracker.get_slot("contact_details"),tracker.get_slot("subject"))
        response = "Thank you for reaching us, {}. You will hear from us.⏱️ \nWe usually reply within 24 business hours so stay tuned!".format(tracker.get_slot("name"))
        dispatcher.utter_message(response)
        
        # save conversation in csv file
        conversation = tracker.events
        SaveChat(conversation)

        return [AllSlotsReset()]

class ActionSaveConversation(Action):
    def name(self) -> Text:
        return "action_save_conversation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conversation = tracker.events
        # print(conversation) # to print raw conversation
        SaveChat(conversation)
        dispatcher.utter_message(text="All chat saved.")
        return []


 # To delete table
    # mydb = sqlite3.connect('..\contacts.db')
    # mycursor = mydb.cursor()

    # mycursor.execute('DROP TABLE contact_info')
    # # mycursor.execute('CREATE TABLE IF NOT EXISTS contact_info(name, contact, subject)')
    # # sql = 'INSERT INTO contact_info(name, contact, subject) VALUES ("{0}","{1}","{2}");'.format(Name, Contact, Subject)
    # # mycursor.execute(sql)
    
    # print(mycursor.rowcount, "record updated")
    # mydb.commit()
    # mydb.close()
