import csv
import time
import datetime
import sys

class sample:
    def __init__(self, timestamp, amplitude):
        self.timestamp = timestamp
        self.amplitude = amplitude

samples = []

#open the waites csv file and create list of timestamps
with open("ag1009.csv") as csvdata:
    csv_reader = csv.reader(csvdata, delimiter=',')
    errCount = 0
    for row in csv_reader:
        timeStamp = time.mktime(datetime.datetime.strptime(row[0], "%m/%d/%Y %H:%M").timetuple())
        try:
            amplitude = float(row[1])
        except:
            errCount +=1
            amplitude = 0
        newSample = sample(timeStamp,amplitude)
        samples.append(newSample)

print("Found", errCount, "error" if errCount == 1 else "errors.")

highCount = 0

for dataPoint in samples:
    if dataPoint.amplitude > 0.01:
        highCount +=1

print(highCount)