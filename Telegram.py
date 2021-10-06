#jo
import requests
import json
import config

key = config.API_KEY_TELEGRAM

def send_message(message, chat_id):
    x = requests.get('https://api.telegram.org/' + str(key) + '/sendMessage?chat_id=' + str(chat_id) + '&text=' + str(message))
    if x.text[2] == 'o' and x.text[3] == 'k':
        return 200
    else:
        return 0

def check_for_message():
    x = requests.get("https://api.telegram.org/" + str(key) +"/getUpdates")
    y = json.loads(x.text)
    return y["result"][len(y["result"]) - 1]["message"]["text"]

def check_for_message_date():
    x = requests.get("https://api.telegram.org/" + str(key) +"/getUpdates")
    y = json.loads(x.text)
    return y["result"][len(y["result"]) - 1]["message"]["date"]

def news(message_telegram, symbol, quantity, mtg, threshold):
    if message_telegram == "money" or message_telegram == "/money" or message_telegram == "wallet" or message_telegram == "/wallet":
        f = open("USDT.txt", "r")
        z = f.readline()
        f.close()
        symbol = symbol.upper()
        f = open(symbol.upper() + ".txt", "r")
        x = f.readline()
        f.close()
        send_message(f"Money: {z}", config.chad_id)
        send_message(f"{symbol}: {x}", config.chad_id)
    if message_telegram == "history" or message_telegram == "/history" or message_telegram == "orderhistory" or message_telegram == "/orderhistory":
        f = open("OrderHistory.txt", "r")
        send_message(f"History:\n{f.read()}", config.chad_id)
        f.close()
    if message_telegram == "help":
        send_message(f"Money - /wallet or /money\nHistory - /history\nTrades(mtg) - /change_mtg\nNew Coin - /change_coin\nNew Quantity - /change_quantity\nchange percent - /change_percent", config.chad_id)
    if message_telegram == "restart orderhistory" or message_telegram == "restart history":
        with open("OrderHistory.txt", 'r+') as f:
            f.truncate(0)
        send_message("!Finished!", config.chad_id)
    if message_telegram == "restart evrything":
        send_message(f"Please write your amount of money:   /exit", config.chad_id)
        return 1
    if message_telegram == "change quantity" or message_telegram == "/change_quantity" or message_telegram == "change_quantity":
        send_message(f"Quantity now: {quantity}\nPlease write new quantity!", config.chad_id)
        return 2
    if message_telegram == "change coin" or message_telegram == "change_coin" or message_telegram == "/change_coin" or message_telegram == "/change coin":
        print(symbol)
        send_message(f"Coin now: {symbol}\nPlease write new coin!   /exit", config.chad_id)
        return 3
    if message_telegram == "change mtg" or message_telegram == "trades" or message_telegram == "/change_mtg":
        send_message(f"MTG now: {mtg}\nPlease write new mtg!   /exit", config.chad_id)
        return 4
    if message_telegram == "percent" or message_telegram == "change percent" or message_telegram == "/change_percent":
        send_message(f"Percent now: {threshold}\nPlease write new percent!   /exit", config.chad_id)
        return 5
    return False
