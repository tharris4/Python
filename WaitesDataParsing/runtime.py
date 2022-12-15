import csv
import time
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

class sample:
    def __init__(self, timestamp, amplitude):
        self.timestamp = timestamp
        self.amplitude = amplitude

samples = []

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Run Time Calculator")
        self.createWidgets()

    def getCurrentValue(self):
        return '{: .2f}'.format(self.currValue.get())

    def calcRunTime(self, vibThreshold):
        runTime = 0
        inRun = False

        for dataPoint in samples:
            if dataPoint.amplitude > vibThreshold and not inRun:
                startRun = dataPoint.timestamp
                inRun = True
            elif dataPoint.amplitude < vibThreshold and inRun:
                endRun = dataPoint.timestamp
                runTime += (endRun - startRun)
                inRun = False

        self.rtLabel['text'] = str(round(runTime/60/60,1)) + ' hours'
    
    #open the waites csv file and create list of timestamps
    def getVibFile(self):
        f = filedialog.askopenfilename()
        with open(f) as csvdata:
            csv_reader = csv.DictReader(csvdata)
            errCount = 0
            for row in csv_reader:
                timeStamp = time.mktime(datetime.datetime.strptime(row['DateTime'], "%m/%d/%Y %H:%M").timetuple())
                #timeStamp = time.mktime(datetime.datetime.strptime(row['DateTime'], "%Y-%m-%d %H:%M:%s").timetuple())
                try:
                    amplitude = float(row['Motor - DS'])
                except:
                    errCount +=1
                    amplitude = 0
                newSample = sample(timeStamp,amplitude)
                samples.append(newSample)

        print("Found", errCount, "error" if errCount == 1 else "errors.")
    
    def ThresholdChanged(self, Event):
        self.calcRunTime(self.vibThreshold.get())
        self.sliderLabel['text'] = self.getCurrentValue()
        line = self.line2.pop(0)
        line.remove()
        self.line2 = self.plot1.plot([self.currValue.get()] * len(samples), label="Threshold", color='black')
        self.canvas.draw()

    def createWidgets(self):
        #slider value
        self.currValue = tk.DoubleVar()
        
        self.getVibFile()
        maxAmp = max(samples, key = lambda x:x.amplitude).amplitude

        self.resizable(width=True, height=True)

        self.welcomeLabel = ttk.Label(master=self, text="Move the slider to change vibration threshold.")

        self.rtLabel = ttk.Label(master=self, font=("Arial", 15), text="")

        self.submit_btn = ttk.Button(
            master=self,
            text="Calculate",
            command=self.calcRunTime
        )
        
        self.sliderLabel = ttk.Label(text=self.getCurrentValue())

        
        self.vibThreshold = ttk.Scale(from_=0, 
                                      to=maxAmp,
                                      orient="horizontal",
                                      variable=self.currValue,
                                      command=self.ThresholdChanged)

        self.fig = Figure(figsize= (5,5), dpi=100)
        self.plot1 = self.fig.add_subplot(111)
        # x = [datetime.datetime.strptime(d,'%m/%d/%Y').date() for d in [sample.timestamp for sample in samples]]
        # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
        # plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        self.line1 = self.plot1.plot([sample.amplitude for sample in samples], label="Vibration Data")
        self.line2 = self.plot1.plot([self.currValue.get()] * len(samples), label="Threshold", color = "black")
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack()

        self.welcomeLabel.pack()
        self.vibThreshold.pack()
        self.sliderLabel.pack()
        self.submit_btn.pack()
        self.rtLabel.pack()


if __name__ == '__main__':
    app = App()
    app.mainloop()