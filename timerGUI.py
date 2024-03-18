import tkinter as tk
from tkinter import filedialog
import myfuncs
from datetime import datetime, timedelta

class timerGUI:
    
    def __init__(self):

        self.root = tk.Tk()
        self.timerRun = False
        self.finish = True
        self.pausedTime = timedelta(0) # saved time when paused
        self.passedTime = timedelta(0) 
        self.targetTime = '0'

        ### GUI definition ---------------------------
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
        self.ttBox.bind("<Key>", lambda a: "break") # prevents textbox from being overriden by user
        self.ttBox.grid(row=1, column=4, sticky=tk.E+tk.W, padx=(20,20))
        
        self.etBox = tk.Entry(self.root)
        self.etBox.bind("<Key>", lambda a: "break") # prevents textbox from being overriden by user
        self.etBox.grid(row=1, column=5, sticky=tk.E+tk.W, padx=(20,20))
        self.etBox.insert(0,"0.00")
        ### GUI definition ---------------------------

    def open_file(self): # linked to start button
        try:
            filepath = filedialog.askopenfile(filetypes=[('Comma Separated Values', '*.csv')])
            self.timerList = myfuncs.readcsv(filepath) # function to read csv file
        except:
            return
        self.timerIter = iter(self.timerList) # to iterate on the list of values
        self.targetTime = next(self.timerIter)
        self.ttBox.delete(0,'end')
        self.ttBox.insert(0, self.targetTime)
        self.finish = False
        self.timerRun = True
        self.startTime = datetime.now()
        self.root.after(1, self.update) # start updating the GUI

    def pause_timer(self): # linked to pause button
        self.timerRun = not self.timerRun # toggle the run flag
        if self.finish:
            return # if the list of values has been cleared, pause does not affect timer
        if self.timerRun:
            self.startTime = datetime.now() # when unpaused, start counting from now
            self.root.after(10, self.update) # run the update function in 10 miliseconds
        else:
            self.pausedTime = self.passedTime # when paused, store the passed time

    def cancel_timer(self): # linked to cancel button
        try:
            self.targetTime = next(self.timerIter) # skip to next time on file
            self.ttBox.delete(0, 'end')
            self.ttBox.insert(0, self.targetTime)
            self.etBox.delete(0, 'end')
            self.etBox.insert(0,"0.00")
            self.startTime = datetime.now()
            self.pausedTime = timedelta(0) # reset the passed time
        except:
            self.stop_timer() # if reached end of list, stop
            self.finish = True
    
    def stop_timer(self): # linked to stop button
        self.finish = True
        self.timerRun = False
        self.ttBox.delete(0, 'end')
        self.etBox.delete(0, 'end')
        self.etBox.insert(0,"0.00")
        self.pausedTime = timedelta(0) # reset the passed time
        self.timerIter = None # stop the timer operation

    def update(self): # GUI update function
        if self.timerRun:
            self.etBox.delete(0,'end')
            self.passedTime = (datetime.now() - self.startTime) + self.pausedTime # calculate delta since start time + saved pause time
            self.etBox.insert(0, ('%d.%02d'%(self.passedTime.seconds, self.passedTime.microseconds))[:-4]) # display precision of 10 miliseconds
            if (self.passedTime.seconds >= int(self.targetTime[0])):
                self.cancel_timer() # if passed time > target time, continue to next time in file
            if self.finish: # cancel update function if finished iterating over list
                self.root.after_cancel(self.update) 
            else:
                self.root.after(10, self.update) # repeat this function every 10 miliseconds
