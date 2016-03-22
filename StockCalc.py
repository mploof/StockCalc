from __future__ import print_function
from io import StringIO
import numpy as np
import re
import os


'''
Quote format

[0]     [1]    [2]    [3]    [4]    [5]     [6]         [7]     [8]
Date    Open   High   Low    Close  Volume  Adj Close   Vel     Accel
'''

DATE = 0
OPEN = 1
HIGH = 2
LOW = 3
CLOSE = 4
VOL = 5
ADJCLOSE = 6
VEL = 7
ACCEL = 8


'''
Method Definitions
'''

def printQuotes(qList, start, stop):
    printHeader()
    for x in range(start, stop):
        printQuoteH(qList, x, False)

def printQuote(qList, which):
    printQuoteH(qList, which, True)

def printQuoteH(qList, which, header):
    if header is True:
        printHeader()
    i = 0
    for x in qList[which]:
        if i == 0:
            print(x, end="")
        else:
            print("%.2f" % x, end="")
        print("\t", end="")
        i += 1
    print("")

def printHeader():
    print("\nDate\t\tOpen\tHigh\tLow\tClose\tVol\t\tAdj C\tVel\tAccel")

def sumCol(col):
    total = 0
    for x in quotes:
        total += x[col]
    return total

def aveCol(col):
    return sumCol(col) / len(quotes)


'''
Add open / close price pct differential
'''
'''
i = 0
for x in quotes:
    if(i == len(quotes)-1):
        x.append(0)
    else:
        openCloseDiff = (x[4] - quotes[i+1][7]) / quotes[i+1][7]
        #val = int((val * 100) + 0.5) / 100.0
        x.append(openCloseDiff)
    i += 1
'''

def printDate(quote):
    print("\nDate: " + str(quote[0]))

'''
Make Investments
'''

class Sim():

    count = 0

    def __init__(self, symbol, aveDays):
        Sim.defaultCash = 1000
        self.symbol = symbol
        self.aveDays = aveDays
        self.quotes = []
        self.initializeQuotes()
        self.buyPrice = 0
        self.cash = Sim.defaultCash
        self.minCash = self.cash
        self.maxCash = self.cash
        self.invested = False
        self.startPrice = 0
        self.endPrice = 0
        self.passiveReturn = 0
        self.velAccel()

    def initializeQuotes(self):
        '''
        Read the quote data and create an array of floats from it
        '''
        path = os.path.dirname(os.path.realpath(__file__));
        with open(path + "/" + self.symbol + ".csv") as f:
            strings = f.read().splitlines()

        for i in range(1, len(strings)):
            x = strings[i]
            thisQuote = []
            # Split using tabs, spaces, or commas as delimiters
            splitOutput = x.split(",")
            # Add the date
            thisQuote.append(splitOutput[0])
            # Add the prices
            for y in range(1, len(splitOutput)):
                thisQuote.append(float(splitOutput[y]))
            # Add this quote to the quote list
            self.quotes.append(thisQuote)

        #print(str(len(self.quotes)) + " days of data collected")

    def velAccel(self):
        '''
        Add price velocity and accel
        '''

        i = 0
        for x in self.quotes:
            if(i >= len(self.quotes)-(1+self.aveDays)):
                x.append(0)
            else:
                vel = (x[ADJCLOSE] - self.quotes[i+self.aveDays][ADJCLOSE]) / self.quotes[i+1][ADJCLOSE]
                x.append(vel)
            i += 1

        i = 0
        for x in self.quotes:
            if(i >= len(self.quotes)-(1+self.aveDays)):
                x.append(0)
            else:
                accel = x[VEL] - self.quotes[i+self.aveDays][VEL]
                x.append(accel)
            i += 1

    def buy(self, quote):
        #printDate(quote)
        #print("Buying at $" + str(quote[ADJCLOSE]))
        self.buyPrice = quote[ADJCLOSE]
        self.invested = True

    def sell(self, quote):
        #printDate(quote)
        #print("Selling at $" + str(quote[ADJCLOSE]))
        sellPrice = quote[ADJCLOSE]
        payoff = sellPrice / self.buyPrice
        #print("Payoff = " + str(payoff))
        self.cash *= payoff
        self.invested = False
        if self.cash < self.minCash:
            self.minCash = self.cash
        elif self.cash > self.maxCash:
            self.maxCash = self.cash
        #print("Current cash: $" + str(self.cash))

    def simulate(self):
        i = 0
        readyToBuy = False
        for x in reversed(self.quotes):
            if i == 0:
                self.startPrice = x[ADJCLOSE]
            # Buy when velocity is positive, sell when it first becomes negative
            if x[ACCEL] > 0 and not self.invested:
                #if readyToBuy:
                    self.buy(x)
                #readyToBuy = True
            elif x[ACCEL] < 0 and self.invested:
                self.sell(x)
                readyToBuy = False
            else:
                readyToBuy = False
            if i == len(self.quotes)-1:
                self.passiveReturn = x[ADJCLOSE] / self.startPrice * Sim.defaultCash
            i += 1

        Sim.count += 1

        print("**** Simulation " + str(Sim.count) + " ****\n")
        print("Stock symbol: " + self.symbol)
        print("Averaging days: " + str(self.aveDays))
        print("Final cash: $" + str(self.cash))
        print("Max cash: $" + str(self.maxCash))
        print("Min cash: $" + str(self.minCash))
        print("Passive Return: $ " + str(self.passiveReturn))
        print("\n")

symbols = ["feye", "amzn", "aapl", "goog", "tsla", "agnc", "ugaz", "dgaz"]
managedCash = 0
passiveCash = 0
for sym in symbols:
    test = Sim(sym, 8)
    test.simulate()
    managedCash += test.cash
    passiveCash += test.passiveReturn

print("Managed total: $ " + str(managedCash))
print("Passive total: $ " + str(passiveCash))
