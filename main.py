from ces import buy, sell
import websocket
import json
import Telegram
import config

symbol = "waxpusdt" #hegicbusd - celrusdt
mtg = 10
quantity = 200
tradenum = 0
trades = [0,0,0,0,0,0,0,0,0,0]
json_message=[]
orders_made = 0
last_date_telegram = 0
change_coin_bool = False

a = 1
for i in range(mtg - 1):
        a = a*2
mtgt = quantity/a

SOCKET = "wss://stream.binance.com:9443/ws/" + symbol + "@kline_1m"

def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, msg):
    global tradenum, trades, symbol, quantity, last_date_telegram, orders_made, x, z, change_coin_bool, SOCKET, coin, coin_quantity

    message_telegram = Telegram.check_for_message()
    message_telegram.lower()
    date_telegram = Telegram.check_for_message_date()
    if date_telegram != last_date_telegram:
        print(message_telegram)
        if change_coin_bool == False:
            change_coin_bool = Telegram.news(message_telegram=message_telegram, symbol=symbol, quantity = quantity)
            print(change_coin_bool)
        else:
            if change_coin_bool == 1:
                if message_telegram != "/exit" and message_telegram != "exit":
                    for zahl in range(100000):
                        if message_telegram == str(zahl):
                            f = open(f"{symbol.upper()}.txt", "w")
                            f.write(str(0))
                            f.close()
                            f = open("USDT.txt", "w")
                            f.write(str(zahl))
                            f.close()
                            Telegram.send_message("!Finished!", config.chad_id)
                            change_coin_bool = False
            if change_coin_bool == 2:
                if message_telegram != "/exit" or message_telegram != "exit" and message_telegram != "change_quantity" and message_telegram != "change quantity" and message_telegram != "/change_quantity":
                    quantity = float(message_telegram)
                    Telegram.send_message("!Finished!", config.chad_id)
                    change_coin_bool = False
            if change_coin_bool == 3:
                if message_telegram != "/exit" and message_telegram != "exit" and message_telegram != "change_coin" and message_telegram != "change coin" and message_telegram != "/change_coin":
                    print("er ist in")
                    f = open(symbol.upper() + ".txt", "r")
                    coin_quantity = f.readline()
                    f.close()
                    sell(symbol=symbol, quantity=float(coin_quantity))
                    symbol = message_telegram
                    SOCKET = f"wss://stream.binance.com:9443/ws/{symbol.lower()}@kline_1m"
                    print(SOCKET)
                    f = open(f"{symbol.upper()}.txt", "w")
                    f.write(str(0))
                    f.close()
                    Telegram.send_message("!Finished!", config.chad_id)
                    change_coin_bool = False
                    trades = [0,0,0,0,0,0,0,0,0,0]
                    ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
                    ws.run_forever()
            if message_telegram == "/exit" or message_telegram == "exit":
                Telegram.send_message("!OK!", config.chad_id)
                change_coin_bool = False
        last_date_telegram = date_telegram

    #print(msg)
    msg_json = json.loads(msg)
    price = float(msg_json['k']['c'])
    print(price, trades)
    json_message.append(float(price))
    if len(json_message) == 15:
        win = 0
        lose = 0
        json_message.pop(0)
        for i in range(14):
            if json_message[i] < json_message[i + 1]:
                win = win + (json_message[i + 1] - json_message[i])
            else:
                lose = lose + (json_message[i] - json_message[i + 1])
            if win != 0 and lose != 0:
                rsi = 100 - 100 / (1 + (win / lose))
            else:
                rsi = 50
    if tradenum == 0:
        print("Rsi", rsi)
    #print(json_message)
    if trades[0] == 0 and rsi < 35:
        trades[0] = price
        tradenum = 1
        print("Buy", tradenum)
        buy(symbol, quantity)
        f = open("OrderHistory.txt", "a")
        f.write("BUY - " + str(price) + " - " + str(tradenum) + "\n")
        f.close()
        f = open("OrderHistory.txt", "a")
        f.write(str(trades) + "\n")
        f.close()
    else:   
        if trades[tradenum - 1] > price + trades[tradenum - 1]/100 and tradenum<mtg:
            trades[tradenum] = price
            tradenum = tradenum + 1
            print("Buy", tradenum)
            buy(symbol, quantity)
            f = open("OrderHistory.txt", "a")
            f.write("BUY - " + str(price) + " - " + str(tradenum) + "\n")
            f.close()
            f = open("OrderHistory.txt", "a")
            f.write(str(trades) + "\n")
            f.close()
        elif trades[tradenum - 1] < price - trades[tradenum - 1]/100 and tradenum >= 1:
            trades[tradenum - 1] = 0
            print("Sell", tradenum)
            sell(symbol, quantity)
            f = open("OrderHistory.txt", "a")
            f.write("SELL - " + str(price) + " - " + str(tradenum) + "\n")
            f.close()
            f = open("OrderHistory.txt", "a")
            f.write(str(trades) + "\n")
            f.close()
            tradenum = tradenum - 1

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()