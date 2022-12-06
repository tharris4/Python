import csv
import math
import tkinter as tk
from tkinter import ttk

class state:
    def __init__(self, name, lat, long, abbr):
        self.name = name
        self.lat = lat
        self.long = long
        self.abbr = abbr


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Geo Guesser!")
        self.createWidgets()

    def isValidSate(self, checkStateName):
        stateFound = False
        for curState in self.states:
            if curState.name.lower() == checkStateName.lower():
                stateFound = curState
                break
        return stateFound

    def getStates():
        states = []
        with open('usstates.csv') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            for row in csv_reader:
                newState = state(abbr=row['state'], name=row['name'], lat=row['latitude'], long=row['longitude'])
                states.append(newState)

        if len(states) == 52:
            print("Got all the states!")
            return states

    states = getStates()

    def showMessage(self, text):
        self.answerLabel.config(text = text)

    def calcDistance(self):
        
        state1 = self.firstStateEntry.get()
        state2 = self.secondStateEntry.get()

        firstState = self.isValidSate(state1)
        secondState = self.isValidSate(state2)
        
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
            #convert to miles
            dist = dist/1609.34

            self.showMessage(["The distance is {:,} ".format(int(dist)), "miles."])

        else:
            self.showMessage("Not a valid state.")

    def createWidgets(self):
        self.resizable(width=False, height=False)

        self.frm_entry = tk.Frame(master=self)
        self.welcomeLabel = ttk.Label(master=self.frm_entry, text="Type two states and guess the distance between them.")

        self.firstStateLabel = ttk.Label(master=self.frm_entry, text="State #1: ")
        self.firstStateEntry = ttk.Entry(master=self.frm_entry, width=25)
        self.secondStateLabel = ttk.Label(master=self.frm_entry, text="State #2: ")
        self.secondStateEntry = ttk.Entry(master=self.frm_entry,  width=25)

        self.welcomeLabel.grid(row=0, column=0, columnspan=2, sticky="n")

        self.firstStateLabel.grid(row=1, column=0, sticky="w")
        self.firstStateEntry.grid(row=1, column=1, sticky="w")

        self.secondStateLabel.grid(row=2, column=0, sticky="w")
        self.secondStateEntry.grid(row=2, column=1, sticky="w")

        self.answerLabel = ttk.Label(master=self, text="")

        self.submit_btn = ttk.Button(
            master=self,
            text="Enter",
            command=self.calcDistance
        )

        self.frm_entry.grid(row=0, column=0, padx=10)
        self.submit_btn.grid(row=3, column=0, pady=10)
        self.answerLabel.grid(row=4, column=0, padx=10)

if __name__ == '__main__':
    app = App()
    app.mainloop()