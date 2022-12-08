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
    csv_reader = csv.DictReader(csvdata)
    errCount = 0
    for row in csv_reader:
        timeStamp = time.mktime(datetime.datetime.strptime(row['DateTime'], "%m/%d/%Y %H:%M").timetuple())
        try:
            amplitude = float(row['Gearbox - DS'])
        except:
            errCount +=1
            amplitude = 0
        newSample = sample(timeStamp,amplitude)
        samples.append(newSample)

print("Found", errCount, "error" if errCount == 1 else "errors.")

runTime = 0
inRun = False

for dataPoint in samples:
    if dataPoint.amplitude > 0.01 and not inRun:
        startRun = dataPoint.timestamp
        inRun = True
    elif dataPoint.amplitude < 0.01 and inRun:
        endRun = dataPoint.timestamp
        runTime += (endRun - startRun)
        inRun = False

print(runTime/60/60, "Hours")