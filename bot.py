import telegram
import requests
import gspread
import gspread_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import matplotlib.pyplot as plt
import numpy
import dataframe_image as dfi
#token that can be generated talking with @BotFather on telegram

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("testapi.json", scope)
gc = gspread.authorize(creds)
wk = gc.open('Data').sheet1
wk1 = gc.open('Data').worksheet('Sheet2')
data = wk.get_all_records()
data1 = wk1.get_all_records()
df = pd.DataFrame(data)
df1 = pd.DataFrame(data1)
df = df.drop_duplicates(subset = ['Nama'], keep = 'last')


base_url = "https://api.telegram.org/bot1756201877:AAE9xiTKief52rbuJDXs9-onmqvJa6FXIJc"
def read_msg(offset):
    parameters = {
        "offset" : offset
        }
    resp = requests.get(base_url + "/getUpdates", data = parameters)
    data = resp.json()

    print(data)

    for result in data["result"]:
        send_msg(result)

    if data["result"]:
        return data["result"][-1]["update_id"]+1

def auto_answer(message):
    
    df['Usia']= df['Usia'].astype(str)
    answer = df.loc[df['Nama'].str.lower() == message.lower()]
    if not answer.empty:
        output = {
        "Timestamp : " + answer.iloc[0]['Timestamp']+ "\n" +
        "Nama : " + answer.iloc[0]['Nama']+ "\n" +
        "Email : " + answer.iloc[0]['Email']+ "\n" +
        "Usia : " + answer.iloc[0]['Usia']+ "\n" +
        "Jenis Kelamin : " + answer.iloc[0]['Jenis Kelamin']+ "\n" +
        "Tempat Lahir : " + answer.iloc[0]['Tempat Lahir']+ "\n" +
        "Tanggal Lahir : " + answer.iloc[0]['Tanggal Lahir']+ "\n" +
        "Upload : " + answer.iloc[0]['Data']
        }
        answer = output
        return answer
    else:
        return "Data tidak tersedia"

def send_msg(message):
    text = message["message"]["text"]
    param = text[1]
    message_id = message["message"]["message_id"]
    answer = auto_answer(text)

    

    parameters = {
        "chat_id":"-409010984",
        "text":answer,
        "reply_to_message_id":message_id
        }

    resp = requests.get(base_url + "/sendMessage", data = parameters)
    print(resp.text)
offset = 0
while True: 
    offset = read_msg(offset)
  
'''
base_url = "https://api.telegram.org/bot1756201877:AAE9xiTKief52rbuJDXs9-onmqvJa6FXIJc/sendMessage"
parameters = {
    "chat_id":"-409010984",
    "text":"Hello123 "
    }
resp = requests.get(base_url, data = parameters)
print(resp.text)
'''

