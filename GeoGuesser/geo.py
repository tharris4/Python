import csv
import math
import tkinter as tk

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

def calcDistance():
    firstState = isValidSate(states, firstStateEntry.get())
    secondState = isValidSate(states, secondStateEntry.get())

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

        answerText = "The distance is {:,} ".format(int(dist)), "miles."
        answerLabel.config(text = answerText)

    else:
        answerLabel["text"] = "Not a valid state."

window = tk.Tk()
window.title("Geo Guesser!")
window.resizable(width=False, height=False)

frm_entry = tk.Frame(master=window)
welcomeLabel = tk.Label(master=frm_entry, text="Type two states and guess the distance between them.")
firstStateLabel = tk.Label(master=frm_entry, text="State #1: ")
firstStateEntry = tk.Entry(master=frm_entry, width=25)
secondStateLabel = tk.Label(master=frm_entry, text="State #2: ")
secondStateEntry = tk.Entry(master=frm_entry,  width=25)

welcomeLabel.grid(row=0, column=0, columnspan=2, sticky="n")

firstStateLabel.grid(row=1, column=0, sticky="w")
firstStateEntry.grid(row=1, column=1, sticky="w")

secondStateLabel.grid(row=2, column=0, sticky="w")
secondStateEntry.grid(row=2, column=1, sticky="w")

submit_btn = tk.Button(
    master=window,
    text="Enter",
    command=calcDistance
)

answerLabel = tk.Label(master=window, text="")

frm_entry.grid(row=0, column=0, padx=10)
submit_btn.grid(row=3, column=0, pady=10)
answerLabel.grid(row=4, column=0, padx=10)

window.mainloop()

