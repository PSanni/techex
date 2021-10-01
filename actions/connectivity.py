import sqlite3
import os


# to store the contact form info in database
def DataUpdate(Name, Contact, Subject):

    # path of the database
    mydb = sqlite3.connect('..\contacts.db')
    mycursor = mydb.cursor()

    # sql = 'CREATE TABLE contact_info(name, contact, subject)'
    sql = 'INSERT INTO contact_info(name, contact, subject) VALUES ("{0}","{1}","{2}");'.format(Name, Contact, Subject)
    mycursor.execute(sql)
    
    print(mycursor.rowcount, "record updated")
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