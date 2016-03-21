from __future__ import print_function
from io import StringIO
import numpy as np
import re
import os


'''
Quote format

[0]     [1]    [2]    [3]    [4]    [5]    [6]    [7]       [8]
Count - Day - Month - Year - Open - High - Low - Close - O/C Diff %
'''


'''
Method Definitions
'''

def printQuotes(start, stop):
    printHeader()
    for x in range(start, stop):
        printQuote(x, False)

def printQuote(which):
    printQuote(which, True)

def printQuote(which, header):
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
    print("\nCount\tDay\tMonth\tYear\tOpen\tHigh\tLow\tClose\tO/C %\tVel\tAccel")

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

#printQuotes(0, 1000)

print("")
print("Days: " + str(len(quotes)))
print("Sum: " + str(sumCol(8)))
print("Ave: " + str(aveCol(8)))


'''
up = np.empty([0])
down = np.empty([0])
count = 0
lastVal = 0
iterator = 0
for x in vals:
    if(iterator != 0):
        if x < 0 and lastVal >= 0:
            up = np.append(up, [count])
            count = 0
        elif x >= 0 and lastVal < 0:
            down = np.append(down, [count])
            count = 0
        count += 1
    lastVal = x
    iterator += 1

print str(up) + "\n"
print str(down) + "\n"
print "Up average: " + str(np.average(up))
print "Up stdev: " + str(np.std(up)) + "\n"
print "Down average: " + str(np.average(down))
print "Down stdev: " + str(np.std(down))
'''
