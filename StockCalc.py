from __future__ import print_function
from io import StringIO
import numpy as np
import re
import os


'''
Quote format

[0]     [1]    [2]    [3]    [4]    [5]    [6]    [7]    [8]    [9]
Count - Day - Month - Year - Open - High - Low - Close - Vel - Accel
'''


'''
Method Definitions
'''

def printQuotes(start, stop):
    printHeader()
    for x in range(start, stop):
        printQuoteH(x, False)

def printQuote(which):
    printQuoteH(which, True)

def printQuoteH(which, header):
    if header is True:
        printHeader()
    i = 0
    for x in quotes[which]:
        if i < 4:
            print(x, end="")
        else:
            print("%.2f" % x, end="")
        print("\t", end="")
        i += 1
    print("")

def printHeader():
    print("\nCount\tDay\tMonth\tYear\tOpen\tHigh\tLow\tClose\tVel\tAccel")

def sumCol(col):
    total = 0
    for x in quotes:
        total += x[col]
    return total

def aveCol(col):
    return sumCol(col) / len(quotes)


'''
Linear Execution
'''


'''
Read the quote data and create an array of floats from it
'''
path = os.path.dirname(os.path.realpath(__file__));
with open(path + "\data.txt") as f:
    strings = f.read().splitlines()

quotes = []
for x in strings:
    thisQuote = []
    splitOutput = re.split(r'\t+',x)
    for y in range(0, 4):
        thisQuote.append(int(splitOutput[y]))
    for y in range(4, len(splitOutput)):
        thisQuote.append(float(splitOutput[y]))
    quotes.append(thisQuote)



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

'''
Add price velocity and accel
'''
aveDays = 7
i = 0
for x in quotes:
    if(i >= len(quotes)-(1+aveDays)):
        x.append(0)
    else:
        vel = (x[7] - quotes[i+aveDays][7]) / quotes[i+1][7]
        x.append(vel)
    i += 1

i = 0
for x in quotes:
    if(i >= len(quotes)-(1+aveDays)):
        x.append(0)
    else:
        accel = x[8] - quotes[i+aveDays][8]
        x.append(accel)
    i += 1

printQuotes(0, 50)

print("")

def printDate(quote):
    print("\nDay: " + str(quote[0]) + " " + str(quote[1]) + "-" + str(quote[2]) + "-" + str(quote[3]))

'''
Make Investments
'''

class investor():

    def __init__(self):
        self.buyPrice = 0
        self.cash = 1000
        self.invested = False

    def buy(self, quote):
        printDate(quote)
        print("Buying at $" + str(quote[7]))
        self.buyPrice = quote[7]
        self.invested = True

    def sell(self, quote):
        printDate(quote)
        print("Selling at $" + str(quote[7]))
        sellPrice = quote[7]
        payoff = sellPrice / self.buyPrice
        print("Payoff = " + str(payoff))
        self.cash *= payoff
        self.invested = False

    def simulate(self, quotes):
        for x in reversed(quotes):
            # Buy when velocity is positive, sell when it first becomes negative
            #print("Invested? " + str(invested))
            if x[9] > 0 and not self.invested:
                self.buy(x)
            elif x[9] < 0 and self.invested:
                self.sell(x)
            else:
                continue

        print("\nFinal cash: $" + str(self.cash))

me = investor()
me.simulate(quotes)
