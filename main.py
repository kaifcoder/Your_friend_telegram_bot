import os
import  requests

BOTKEY = os.environ['BOTKEY']
KEY = os.environ['KEY']
BID = os.environ['BID']

base_url = "https://api.telegram.org/"+BOTKEY

def readmsg(offset):

  parameters = {
      "offset" : offset,
  }
  resp = requests.get(base_url + "/getUpdates", data=parameters)
  
  data = resp.json()
  
  for result in data["result"]:
    sendmsg(result)

  if data["result"]: return data["result"][-1]["update_id"] + 1

def auto_answer(message,uid):
  if (message == "/start"):
    return "Hi!"
  else:
    uid = str(uid)
    request_url_brainshop = "http://api.brainshop.ai/get?bid="+BID+"&key="+KEY+"&uid="+uid+"&msg="+message
    resp = requests.get(request_url_brainshop)
    answer = resp.json()
    print(answer)
    return answer["cnt"]

def sendmsg(message):
  if(message["message"].get("text")):
    text = message["message"]["text"]
    chat_id = message["message"]["chat"]["id"]
    answer = auto_answer(text,chat_id)

    parameters = {
      "chat_id" : chat_id,
      "text" : answer,
    }

    resp = requests.get(base_url + "/sendMessage", data=parameters)
  else:
    text1 = "please use text only!"
    chat_id = message["message"]["chat"]["id"]
    parameters = {
    "chat_id" : chat_id,
    "text" : text1,
    }
    resp = requests.get(base_url + "/sendMessage", data=parameters)

offset = 0
while True:
  offset = readmsg(offset)
