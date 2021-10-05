from ces import buy, sell, Quantity
import websocket
import json
import Telegram
import config

symbol = "omgusdt" #hegicbusd - celrusdt -waxpusdt
mtg = 10
tradenum = 0
trades = [0,0,0,0,0,0,0,0,0,0]
json_message=[]
threshold = 1.5
last_date_telegram = "0"
nextrsi = False
change_coin_bool = False

SOCKET = "wss://stream.binance.com:9443/ws/" + symbol + "@kline_1m"

def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('closed connection')

def on_message(ws, msg):
    global tradenum, trades, symbol, quantity, nextrsi, last_date_telegram, SOCKET, change_coin_bool, mtg, threshold, mtgt, a

    message_telegram = Telegram.check_for_message()
    message_telegram = message_telegram.lower()
    date_telegram = Telegram.check_for_message_date()
    if date_telegram != last_date_telegram:
        print(message_telegram)
        if change_coin_bool == False:
            change_coin_bool = Telegram.news(message_telegram=message_telegram, symbol=symbol, quantity=quantity, mtg=mtg, threshold=threshold)
            print(change_coin_bool)
        else:
            if change_coin_bool == 1:
                if message_telegram != "/exit" and message_telegram != "exit":
                    f = open(f"{symbol.upper()}.txt", "w")
                    f.write(str(0))
                    f.close()
                    f = open("USDT.txt", "w")
                    f.write(str(message_telegram))
                    f.close()
                    Telegram.send_message("!Finished!", config.chad_id)
                    change_coin_bool = False
            if change_coin_bool == 2:
                if message_telegram != "/exit" or message_telegram != "exit":
                    quantity = float(message_telegram)
                    Telegram.send_message("!Finished!", config.chad_id)
                    change_coin_bool = False
            if change_coin_bool == 3:
                if message_telegram != "/exit" and message_telegram != "exit":
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
                    quantity = Quantity(mtg=mtg, symbol=symbol)
                    a = 1
                    print("er is da")
                    for i in range(mtg - 1):
                        print("er is da")
                        a = a * 2
                    mtgt = quantity / a
                    Telegram.send_message("!Finished!", config.chad_id)
                    change_coin_bool = False
                    trades = []
                    ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
                    ws.run_forever()
            if change_coin_bool == 4:
                if message_telegram != "/exit" and message_telegram != "exit":
                    mtg = float(message_telegram)
                    quantity = Quantity(mtg=mtg, symbol=symbol)
                    a = 1
                    for i in range(mtg - 1):
                        a = a * 2
                    mtgt = quantity / a
                    Telegram.send_message("!Finished!", config.chad_id)
                    change_coin_bool = False
            if change_coin_bool == 5:
                if message_telegram != "/exit" and message_telegram != "exit":
                    threshold = float(message_telegram)
                    Telegram.send_message("!Finished!", config.chad_id)
                    change_coin_bool = False
            if message_telegram == "/exit" or message_telegram == "exit":
                Telegram.send_message("!OK!", config.chad_id)
                change_coin_bool = False
        last_date_telegram = date_telegram

    #print(msg)
    msg_json = json.loads(msg)
    price = float(msg_json['k']['c'])
    is_candle_closed = msg_json['k']['x']
    print(price, trades)

    if is_candle_closed:
        json_message.append(float(price))
        if len(json_message) == 15:
            nextrsi = True
            win = 0
            lose = 0
            json_message.pop(0)
            for i in range(12):
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
    if trades[0] == 0 and rsi < 35 and nextrsi:
        nextrsi = False
        trades[0] = price
        tradenum = 1
        print("Buy", tradenum)
        buy(symbol, quantity)
        f = open("Order_Log.txt", "a")
        f.write("BUY - " + str(price) + " - " + str(tradenum) + "\n")
        f.close()
        f = open("Order_Log.txt", "a")
        f.write(str(trades) + "\n")
        f.close()
    else:
        if trades[tradenum - 1] > price + (trades[tradenum - 1]/100) * threshold and tradenum<mtg:
            trades[tradenum] = price
            tradenum = tradenum + 1
            print("Buy", tradenum)
            buy(symbol, quantity)
            f = open("Order_Log.txt", "a")
            f.write("BUY - " + str(price) + " - " + str(tradenum) + "\n")
            f.close()
            f = open("Order_Log.txt", "a")
            f.write(str(trades) + "\n")
            f.close()
        elif trades[tradenum - 1] < price - (trades[tradenum - 1]/100) * threshold and tradenum >= 1:
            trades[tradenum - 1] = 0
            print("Sell", tradenum)
            sell(symbol, quantity)
            f = open("Order_Log.txt", "a")
            f.write("SELL - " + str(price) + " - " + str(tradenum) + "\n")
            f.close()
            f = open("Order_Log.txt", "a")
            f.write(str(trades) + "\n")
            f.close()
            tradenum = tradenum - 1

quantity = float(Quantity(mtg=mtg, symbol=symbol))
a = 1
for i in range(mtg - 1):
        a = a*2
mtgt = quantity/a

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()
