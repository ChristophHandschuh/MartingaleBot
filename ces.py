import requests
import json

startcapital = 500

def buy(symbol, quantity):
    global startcapital
    try:
        f = open("USDT.txt", "r")
        startcapital = float(f.read())
        f.close()
    except IOError:
        f = open("USDT.txt", "w")
        f.write(str(startcapital))
        f.close()
    symbolprice = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=' + symbol.upper())
    symbolprice = json.loads(symbolprice.text)
    symbolprice = float(symbolprice["price"])
    if symbolprice*quantity > startcapital:
        return "You are broke"
    else:
        try:
            f = open(symbol.upper() + ".txt", "r")
            oldquantity = float(f.read())
            f.close()
        except IOError:
            f = open(symbol.upper() + ".txt", "w")
            f.write("0")
            f.close()
            oldquantity = 0
        fee = (quantity/1000) * symbolprice
        #print(fee)
        f = open(symbol.upper() + ".txt", "w")
        f.write(str(quantity + oldquantity))
        f.close()
        f = open("USDT.txt", "r")
        usdt = float(f.read())
        f.close()
        f = open("USDT.txt", "w")
        f.write(str(usdt - (symbolprice*quantity + fee)))
        f.close()
        return 200

def sell(symbol, quantity):
    f = open(symbol.upper() + ".txt", "r")
    crypto = float(f.read())
    f.close()
    if quantity > crypto:
        return "You are broke"
    else:
        symbolprice = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=' + symbol.upper())
        symbolprice = json.loads(symbolprice.text)
        symbolprice = float(symbolprice["price"])
        usdtcurrent = symbolprice*quantity
        f = open(symbol.upper() + ".txt", "w")
        f.write(str(crypto - quantity))
        f.close()
        f = open("USDT.txt", "r")
        usdt = float(f.read())
        f.close()
        f = open("USDT.txt", "w")
        f.write(str(usdt + usdtcurrent))
        f.close()
        return 200
