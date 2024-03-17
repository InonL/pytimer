import tkinter as tk
from tkinter import filedialog
import myfuncs
from datetime import datetime, timedelta

class timerGUI:
    
    def __init__(self):

        self.root = tk.Tk()
        self.timerRun = False

        self.buttonFrame = tk.Frame(self.root)

        for i in range(3):
            self.buttonFrame.rowconfigure(i, weight=1)

        for i in range(7):
            self.buttonFrame.columnconfigure(i, weight=1)

        self.StartButton = tk.Button(self.root, text="Start", font=('Arial', 12), command=self.open_file)
        self.StartButton.grid(row=1, column=0, sticky=tk.W+tk.E, padx=(20,20), pady=(0,20))

        self.PauseButton = tk.Button(self.root, text="Pause", font=('Arial', 12), command=self.pause_timer)
        self.PauseButton.grid(row=1, column=1, sticky=tk.W+tk.E, padx=(20,20), pady=(0,20))

        self.CancelButton = tk.Button(self.root, text="Cancel", font=('Arial', 12), command=self.cancel_timer)
        self.CancelButton.grid(row=1, column=2, sticky=tk.W+tk.E, padx=(20,20), pady=(0,20))

        self.StopButton = tk.Button(self.root, text="Stop", font=('Arial', 12), command=self.stop_timer)
        self.StopButton.grid(row=1, column=3, sticky=tk.W+tk.E, padx=(20,20), pady=(0,20))

        self.timeTarget = tk.Label(self.root, text="Time Target (s)")
        self.timeTarget.grid(row=0, column=4, sticky=tk.W+tk.E+tk.N, padx=(20,20))    
        
        self.elapsedTime = tk.Label(self.root, text="Elapsed Time (s)")
        self.elapsedTime.grid(row=0, column=5, sticky=tk.W+tk.E+tk.N, padx=(20,20))

        self.ttBox = tk.Entry(self.root)
        self.ttBox.grid(row=1, column=4, sticky=tk.E+tk.W, padx=(20,20))
        
        self.etBox = tk.Entry(self.root)
        self.etBox.grid(row=1, column=5, sticky=tk.E+tk.W, padx=(20,20))        

    def open_file(self):
        filepath = filedialog.askopenfile(filetypes=[('Comma Separated Values', '*.csv')])
        self.timerList = myfuncs.readcsv(filepath)
        self.timerIter = iter(self.timerList)
        self.targetTime = next(self.timerIter)
        self.ttBox.delete(0,'end')
        self.ttBox.insert(0, self.targetTime)
        self.timerRun = True
        self.startTime = datetime.now()
        self.etBox.insert(0,"0.00")

    def pause_timer(self):
        self.timerRun = not self.timerRun

    def cancel_timer(self):
        try:
            self.targetTime = next(self.timerIter)
            self.ttBox.delete(0, 'end')
            self.ttBox.insert(0, self.targetTime)
            self.startTime = datetime.now()
        except:
            self.stop_timer()
    
    def stop_timer(self):
        self.timerRun = False
        self.ttBox.delete(0, 'end')
        self.etBox.delete(0, 'end')

    def update(self):
        
        if self.timerRun:
            self.etBox.delete(0,'end')
            self.passedTime = datetime.now() - self.startTime
            self.etBox.insert(0, ('%d.%02d'%(self.passedTime.seconds, self.passedTime.microseconds))[:-4])
        else:
            pass
        
        self.timer = self.root.after(10, self.update)

