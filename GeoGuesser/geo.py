import csv
import math

class state:
    def __init__(self, name, lat, long, abbr):
        self.name = name
        self.lat = lat
        self.long = long
        self.abbr = abbr

def isValidSate(stateList, checkStateName):
    stateFound = False
    for curState in stateList:
        if curState.name.lower() == checkStateName.lower():
            stateFound = curState
            break
    return stateFound

states = []

with open('usstates.csv') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    for row in csv_reader:
        newState = state(abbr=row['state'], name=row['name'], lat=row['latitude'], long=row['longitude'])
        states.append(newState)

if len(states) == 52:
    print("Got all the states!")


while True:
    firstStateName = input("Name the first state: ")
    secondStateName = input("Name the second state: ")

    firstState = isValidSate(states, firstStateName)
    secondState = isValidSate(states, secondStateName)

    if firstState and secondState:
        lat1, lat2 = float(firstState.lat), float(secondState.lat)
        long1, long2 = float(firstState.long), float(secondState.long)

        R = 6371000
        l1 = lat1 * math.pi/180
        l2 = lat2 * math.pi/180
        dlat = (lat2 - lat1) * math.pi/180
        dlong = (long2 - long1) * math.pi/180

        a = math.sin(dlat/2)*math.sin(dlat/2) + math.cos(l1)*math.cos(l2)*math.sin(dlong/2)*math.sin(dlong/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        dist = R * c
        #conver to miles
        dist = dist/1609.34

        print("The distance is {:,} ".format(int(dist)), "miles.")

    else:
        print("Not a valid state.")