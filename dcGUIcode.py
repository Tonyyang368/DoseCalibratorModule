# Importing Necessary Libraries
import tkinter as tk
from tkinter import *
from tkinter.ttk import Combobox
import tkinter.simpledialog as simpledialog
from PIL import ImageTk, Image
import pandas as pd
import numpy as np
import time
import board
import busio
import adafruit_bme280
import digitalio
import csv
import subprocess


# Initializing the UI Window
class MyWindow:
    def __init__(self, win):

        #-- Establishing Default Values---#
        self.default_inputs = [0,2,1,60000,500]
        # --- Establishing Entry Variables ---#

        self.measVar = StringVar()
        self.intTimeVar = StringVar()
        self.samplesVar = StringVar()
        self.totTimeVar = StringVar()
        self.biasVar = StringVar()
        self.tempVar = StringVar()
        self.pressureVar = StringVar()
        self.correctionVar = StringVar()
        self.averagesVar = StringVar()
        self.measTimeVar = StringVar()
        self.intervalTimeVar= StringVar()
        self.pCVar = StringVar()
        self.pAVar = StringVar()
        self.tempUnit = IntVar()
        self.pressureUnit = IntVar()
        self.current_temp = DoubleVar()
        self.current_pressure = DoubleVar()
        self.startStop = IntVar()
        self.START = 0
        self.STOP = 1
        self.electrometerMessage = StringVar()

        self.textVariables = ['measVar', 'intTimeVar', 'samplesVar',
        'totTimeVar', 'biasVar', 'tempVar', 'pressureVar',
        'correctionVar', 'averagesVar', 'measTimeVar', 'intervalTimeVar',
        'pCVar', 'pAVar'
        ]

        self.textVariables2 = [self.measVar, self.intTimeVar, self.samplesVar,
        self.totTimeVar, self.biasVar, self.tempVar, self.pressureVar,
        self.correctionVar, self.averagesVar, self.measTimeVar, self.intervalTimeVar,
        ]

         # --- Building the GUI ---#

        self.labelling(win)
        self.entries(win)
        self.buttons(win)
        self.placing(win)
        self.binding(win)
        self.help(win)
       

    def labelling(self,win):
        
        # Title
        self.ttle = Label(win, text = 'X-Calibrator')

        # RIGHT SIDE
        self.meas = Label(win, text = 'Meas Range:')
        self.intTime = Label(win, text = 'Int Time (ms):')
        self.samples = Label(win, text = '# of Samples:')
        self.totTime = Label(win, text = 'Total Time (ms):')
        self.bias = Label(win, text = 'Bias Voltage (V):')

        # LEFT SIDE
        self.temp = Label(win, text = 'Temperature:')
        self.pressure = Label(win, text = 'Pressure:')
        self.correction = Label(win, text = 'T/P Correction:')

        self.averages = Label(win,bd=0, highlightthickness=0, text = '# of Averages:')
        self.measTime = Label(win, text = 'Meas Time (s):')
        self.intervalTime = Label(win, text = 'Interval Time:')

        # Results
        self.pC_Label = Label(win, text = 'Charge Results:',font='Helvetica 20')
        self.pA_Label = Label(win, text = 'Current Results:',font='Helvetica 20')


    def entries(self,win):

        # RIGHT SIDE
        self.measIn = Entry(bd=3, width = 10,textvariable=self.measVar)
        self.intTimeIn = Entry(bd=3, width = 10,textvariable=self.intTimeVar)
        self.samplesIn = Entry(bd=3, width = 10,textvariable=self.samplesVar)
        self.totTimeIn = Entry(bd=3, width = 10,textvariable=self.totTimeVar)
        self.biasIn = Entry(bd=3, width = 10,textvariable=self.biasVar)

        # LEFT SIDE 
        self.tempIn = Entry(bd=3, width = 10,textvariable=self.tempVar)
        self.pressureIn = Entry(bd=3, width = 10,textvariable=self.pressureVar)
        self.correctionIn = Entry(bd=3, width = 10,textvariable=self.correctionVar)
       
        self.averagesIn = Entry(bd=3, width = 10,textvariable=self.averagesVar)
        self.measTimeIn = Entry(bd=3, width = 10,textvariable=self.measTimeVar)
        self.intervalTimeIn = Entry(bd=3, width = 10,textvariable=self.intervalTimeVar)
       
        # Results
        self.pC = Entry(bd=5, width = 10,textvariable=self.pCVar)
        self.pA = Entry(bd=5, width = 10,textvariable=self.pAVar)

        self.entryList = [ 'measIn', 'intTimeIn', 'samplesIn',
        'totTimeIn', 'biasIn', 'tempIn', 'pressureIn',
        'correctionIn', 'averagesIn', 'measTimeIn', 'intervalTimeIn',
        'pC', 'pA'
        ]
       
    def buttons(self,win):

        #  Control Buttons
        self.getAll = Button(win, text = 'Get All', command = self.GetResults)
        self.setAll = Button(win, text = 'Set All', command = self.GetDefaults)
        self.zero = Button(win, text = 'Zero', command = self.zeroing)
        self.startButton = Button(win, text = 'Start/Stop Measurements',command = self.submit_data)
        
        self.check.set(self.START) # check determines the function of Start/Stop. Upon initialization, by default it is Start
        
        # Channel and Unit Settings 
        channel = IntVar()
        self.V1 = Radiobutton(win, text="Channel 1", variable=channel, value=1)
        self.V1.pack( anchor = W )
        self.V2 = Radiobutton(win, text="Channel 2", variable=channel, value=2)
        self.V2.pack( anchor = W )

        self.tempUnit.set(1)
        self.celsius = Radiobutton(win, text="C", variable=self.tempUnit, value=1, command=self.changeTemp)
        self.farenheit =  Radiobutton(win, text="F", variable=self.tempUnit, value=2, command=self.changeTemp)
       
        self.pressureUnit.set(1)
        self.Hg = Radiobutton(win, text="mmHg", variable=self.pressureUnit, value=1, command=self.changePressure)
        self.mBar =  Radiobutton(win, text="mBar", variable=self.pressureUnit, value=2, command=self.changePressure)
       
    def placing(self,win):
        self.ttle.place(x = 350, y = 0)
        # Placing Labels
        y = 42
        dispY = 30
        dispX = 25
        self.meas.place(x = 10 + dispX, y = y)
        self.intTime.place(x = 10 + dispX, y = y + dispY)
        self.samples.place(x = 10 + dispX, y = y + dispY*2)
        self.totTime.place(x = 10 + dispX, y = y + dispY*3)
        self.bias.place(x = 10 + dispX, y = y + dispY*4)
        # Placing Entries
        y_ent = 40
        self.measIn.place(x = 150 + dispX, y = y_ent)
        self.intTimeIn.place(x = 150 + dispX, y = y_ent + dispY)
        self.samplesIn.place(x = 150 + dispX, y = y_ent + dispY*2)
        self.totTimeIn.place(x = 150 + dispX, y = y_ent + dispY*3)
        self.biasIn.place(x = 150 + dispX, y = y_ent + dispY*4)
        # Placing Buttons
        self.getAll.place(x = 130 + dispX, y = 200)
        self.setAll.place(x = 192 + dispX, y = 200)
        self.zero.place(x = 253 + dispX, y = 200)

        self.startButton.place(x = 100, y = 270,height = 30, width = 550)

       
        # Placing Radio Buttons
        self.V1.place(x = 10 + dispX, y = 195)
        self.V2.place(x = 10 + dispX, y = 215)
        #------LEFT SIDE-----#
        leftX = 400
        # Placing Labels
        self.temp.place(x=leftX, y = y)
        self.pressure.place(x = leftX , y = y + dispY*1)
        self.correction.place(x = leftX , y = y + dispY*2)

        self.averages.place(x=leftX, y = y + dispY*4)
        self.measTime.place(x = leftX , y = y + dispY*5)
        self.intervalTime.place(x = leftX , y = y + dispY*6)

        # Placing Entries
        leftEntryX = 500
        self.tempIn.place(x = leftEntryX + dispX, y = y_ent)
        self.pressureIn.place(x = leftEntryX + dispX, y = y_ent + dispY)
        self.correctionIn.place(x = leftEntryX + dispX, y = y_ent + dispY*2)

        # Shifted Entries
        self.averagesIn.place(x = leftEntryX + dispX, y = y_ent + dispY*4)
        self.measTimeIn.place(x = leftEntryX + dispX, y = y_ent + dispY*5)
        self.intervalTimeIn.place(x = leftEntryX + dispX, y = y_ent + dispY*6)
        # Placing  Buttons

        # Placing Radio Buttons
        leftRadio = 605
        dispRadioX = 75
        self.celsius.place(x = leftRadio, y = y)
        self.farenheit.place(x = leftRadio + dispRadioX, y = y)
       
        self.Hg.place(x = leftRadio, y = y + dispY*1)
        self.mBar.place(x = leftRadio + dispRadioX, y = y + dispY*1)

        # Placing Results
        dispResultsX = 75
        self.pC_Label.place(x = 75 + dispResultsX, y = 330,)
        self.pC.place(x = 300 + dispResultsX, y = 327,width = 175, )
        self.pA_Label.place(x = 75 + dispResultsX, y = 375,)
        self.pA.place(x = 300 + dispResultsX, y = 372,width = 175, )
   
    def binding(self,win):

        # Binding each string variable from entryList to its respective entry
        getattr(self, self.entryList[0]).bind('<FocusIn>',lambda e: self.set_active_entry(self.textVariables[0]))
        getattr(self, self.entryList[1]).bind('<FocusIn>',lambda e: self.set_active_entry(self.textVariables[1]))
        getattr(self, self.entryList[2]).bind('<FocusIn>',lambda e: self.set_active_entry(self.textVariables[2]))
        getattr(self, self.entryList[3]).bind('<FocusIn>',lambda e: self.set_active_entry(self.textVariables[3]))
        getattr(self, self.entryList[4]).bind('<FocusIn>',lambda e: self.set_active_entry(self.textVariables[4]))
        getattr(self, self.entryList[5]).bind('<FocusIn>',lambda e: self.set_active_entry(self.textVariables[5]))
        getattr(self, self.entryList[6]).bind('<FocusIn>',lambda e: self.set_active_entry(self.textVariables[6]))
        getattr(self, self.entryList[7]).bind('<FocusIn>',lambda e: self.set_active_entry(self.textVariables[7]))
        getattr(self, self.entryList[8]).bind('<FocusIn>',lambda e: self.set_active_entry(self.textVariables[8]))
        getattr(self, self.entryList[9]).bind('<FocusIn>',lambda e: self.set_active_entry(self.textVariables[9]))
        getattr(self, self.entryList[10]).bind('<FocusIn>',lambda e: self.set_active_entry(self.textVariables[10]))      

       
    def help(self, win):

        #To add more, first add the option to helpOptions, then the option under switcher
        helpOptions = [
            "Electrometer", "Sensors", "Ion Chamber",
            "Meas Range","Int Time", "# of Samples", "Total Time (ms)",
            "Bias Voltage (V)", "Temperature", "Pressure", "T/P Correction",
            "# of Averages", "Meas Time (s)", "Interval Time", "Charge Results",
            "Current Results"
                ]

        def helpFunc(value):
            switcher = {
                "Electrometer":"Standard Imaging 3D Electrometer. The electrometer system in summary is an analog to digital converter with a dc boost that supplies the ion chamber with the high voltage it requires. Signals from the ion chamber pass through the electrometer via a triax cable.",
                "Sensors":"""As the ion chamber is exposed to ambient air during operation, it requires a correction factor that takes into account the varying pressure and temperature differences in each different location. The Cross Calibrator’s sensor is the Bosch BME280, a combined digital humidity, pressure and temperature sensor that uses SPI interface and is located on the inside of the ion chamber. Relevant parameters are as follows:
                Response time: 1 s
                Pressure accuracy range: 1 hPa
                Temperature accuracy: 1 °C
                Size: 19mm x 18mm x 3mm""",
                "Ion Chamber":"The ion chamber accepts a 3ml syringe and holds 1 ml of radioisotope in the center of its sensitive volume. The ion chamber communicates with ambient air so its measurements require pressure and temperature calibration.",
                "Meas Range":"The range value indicates the maximum charge that can be accumulated during the integration time. Then the maximum input current for a given range is Imax = Qmax/Tint",
                "Int Time":"Basic electrometer charge accumulation time",
                "# of Samples":"Total amount of basic charge accumulations. Each sample lasts for as long as the set integration time. All samples amount to one charge time.",
                "Bias Voltage (V)":"Electric potential supplied to the chamber from the electrometer. The settable range is 0VDC, +/-100VDC to +/-450VDC",
                "# of Averages":"Overall number of charge averages. Since integration time maxes at 1 second, multiple averages are required for an extended measurement time.",
                "Total Time (ms)":"Charge averaging time is the product of the integration time (time/sample) and the number of samples. The total time is the number of averages multiplied by averaging time.",
            }
            # Generate the popup window for each help option
            popUp = Toplevel()
            # Determine the position of the popup window relative to pointerx() - your mouse
            popUp.geometry("+{0}+{1}".format(popUp.winfo_pointerx() - 400, 100))
            popUp.title(value)
            info = Message(popUp, text = switcher.get(value), anchor = W)
            info.pack(side="top", fill="x", pady=10)
           
        # Making and placing the help menu button 
        self.helpSelection = StringVar(win)
        self.helpSelection.set("Help")
     
        self.helpMenu = OptionMenu(win, self.helpSelection, *helpOptions, command = helpFunc)
        self.helpMenu.config(width = 12)
        self.helpMenu.pack( anchor = E )
           

    def set_active_entry(self, name):
        self._active_entry = name #retrieve which entry was selected
        numPad(self,self) #Open number pad
   
    @property
    def active_entry(self):
        return getattr(self, self._active_entry) 
   
   
    # -- IMPORTANT FUNCTION FOR SENDING OFF THE VARIABLES --#  
   
    def GetDefaults(self):
        self.measVar.set(str(self.default_inputs[0]))
        self.intTimeVar.set(str(self.default_inputs[1]))
        self.samplesVar.set(str(5000))
        self.totTimeVar.set(str(self.default_inputs[3]))
        self.biasVar.set(str(self.default_inputs[4]))
       
   
       
        self.averagesVar.set(str(5000))
        self.measTimeVar.set(str(1))
        self.intervalTimeVar.set(str(1))

    def zeroing(self):

        # Resets all the entries 
        self.measIn.delete(0, 'end')
        self.intTimeIn.delete(0, 'end')  
        self.samplesIn.delete(0, 'end')  
        self.totTimeIn.delete(0, 'end')  
        self.biasIn.delete(0, 'end')
       
        self.averagesIn.delete(0, 'end')  
        self.measTimeIn.delete(0, 'end')
        self.intervalTimeIn.delete(0, 'end')
       
       
    def GetResults(self):
       
        #check if electrometer is done
        if (self.electrometerStart.get() != 'Electrometer Finished'):
                print("Electrometer still processing")
                return

        #Open up the Results.txt 
        with open(r'/home/pi/Desktop/Results.txt', 'r') as f:
            #Convert to csv file 
            reader = csv.reader(f, delimiter = '\t')
            #Read each value inside and present to user 
            for column in reader:
                self.pCVar.set(str(column[0]))
                self.pAVar.set(str(column[1]))
        
        self.check.set(self.START) #ready to Start next test
       
       
    def submit_data(self):
        checkArray = []
        if self.check: #check whether to Start or Stop test based on check value
            #stop
            checkArray.append('1') #sends 1 to Check.txt 
            df_check = pd.DataFrame([checkArray])  
            np.savetxt(r'/home/pi/Desktop/Check.txt',df_check.values,fmt='%s', delimiter='\t')
            self.check = not self.check # once stopped, ready to Start next test
            return
        else:
            #start
            checkArray.append('0') #sends 0 to Check.txt
            df_check = pd.DataFrame([checkArray])  
            np.savetxt(r'/home/pi/Desktop/Check.txt',df_check.values,fmt='%s', delimiter='\t')
   
        #connecting sensors and reading temperature/pressure
        spi = busio.SPI(board.SCK, MOSI = board.MOSI, MISO = board.MISO)
        cs = digitalio.DigitalInOut(board.D26)
        bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi,cs)
        self.current_temp.set(bme280.temperature)
        self.current_pressure.set(bme280.pressure / 1.333223874)
        #converts values between units
        self.changeTemp()
        self.changePressure()
        #calculate and set correction factor 
        correction_factor = 760 /self.current_pressure.get() * (self.current_temp.get() + 273.16) / 295.16
        self.correctionVar.set(str(correction_factor))
        data_list = []
        # Create a list to get all the inputted values
        # Programed for Readibility
        for item in self.textVariables2[0:-3]:
            data_list.append(item.get())
       
        for value in data_list:
            if(value == ''):
                dataReady = FALSE
                print("You're missing entries")
                break
           
            else:
                dataReady = TRUE
               
        if(dataReady):
            #sends information to Entries.txt 
            df_test = pd.DataFrame([data_list])    # values   # 1st column as index
            np.savetxt(r'/home/pi/Desktop/Entries.txt',df_test.values,fmt='%s', delimiter='\t')
            #start electrometer code, electrometerStart will store any output in the terminal 
            electrometerStart = subprocess.run(r'/home/pi/Desktop/electrometer', shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')  
            self.electrometerMessage.set(electrometerStart)
            self.check.set(self.STOP) #now that electrometer is running, Start/Stop acts as Stop button  
       
    def changeTemp(self):
        #converts temperature between units
        if self.current_temp.get() != 0:
            if self.tempUnit.get() == 1:
                self.tempVar.set(self.current_temp.get())
               
            else:
                self.tempVar.set(self.current_temp.get()*9/5 + 3)
               
    def changePressure(self):
        #converts pressure between units
        if self.current_pressure.get() != 0:
            if self.pressureUnit.get() == 1:
                self.pressureVar.set(self.current_pressure.get())
               
            else:
                self.pressureVar.set(self.current_pressure.get()*1.33322)

class numPad(simpledialog.Dialog):
    def __init__(self,master=None,parent=None):
        #create popup window for numberpad
        self.parent = parent
        self.top = Toplevel()
        #positions numberpad relative to pointer 
        self.top.geometry("+{0}+{1}".format(self.top.winfo_pointerx() - 1, self.top.winfo_pointery()-12))
        #add features to numberpad
        self.top.protocol("WM_DELETE_WINDOW",self.ok)
        self.createWidgets()

    def createWidgets(self):
        btn_list = ['7',  '8',  '9', '4',  '5',  '6', '1',  '2',  '3', '0',  'Close',  'Del']
        # create and position all buttons with a for-loop
        # r, c used for row, column grid values
        r = 1
        c = 0
        n = 0
        # list(range()) needed for Python3
        btn = []
        for label in btn_list:
            # partial takes care of function and argument
            cmd = lambda x = label: self.click(x)
            # create the button
            cur = Button(self.top, text=label, width=8, height=3, command=cmd)
            btn.append(cur)
            # position the button
            btn[-1].grid(row=r, column=c)
            # increment button index
            n += 1
            # update row/column position
            c += 1
            if c == 3:
                c = 0
                r += 1
    def click(self,label):
        #correlates buttons to numbers for the entry box
        print(label)
        if label == 'Del':
            currentText = self.parent.active_entry.get()
            self.parent.active_entry.set(currentText[:-1])
        elif label == 'Close':
            self.ok()
           
        else:
            currentText = self.parent.active_entry.get()
            self.parent.active_entry.set(currentText+label)
    def ok(self):
        self.top.destroy()
        self.top.master.focus()

   






window=Tk()


mywin=MyWindow(window)




window.title('ECE 491 GUI')
window.geometry("800x480+10+10")
window.mainloop()