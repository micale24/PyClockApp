##############===----Time Clock App Overview----===################### 
'''
    References 
    https://tkdocs.com/tutorial/index.html
    https://pyvisa.readthedocs.io/en/latest/introduction/index.html
    https://www.codegrepper.com/code-examples/python/how+to+append+a+list+to+a+text+file+in+python
     
'''
import os                                                                                                    #Import section for Python libaries 
import datetime as dt
import time 
import pyvisa                                                                                                #The test equipment optimzer libary 
import math as math
from tkinter import *                                                                                        #This the built gui libary 
import tkinter as tk
from tkinter import ttk, filedialog, Text, messagebox

rm = pyvisa.ResourceManager()                                                                                 #Connecting the test equipment to an obejct for Pyvisa 
rm.list_resources()                                                                                           #List resources commands the test equipment to produces the USB address for python it returns a tuple

def convertTuple(usb):                                                                                        #This function allows any frequency counter to be connected 
    ''' Converts 53230A USB Address tuple into string'''
    str = ''
    for item in usb:
        str = str + item
    return str
freq_counter_usb = convertTuple(rm.list_resources()[0])

try:                                                                                                           #The try/except statments ensures the USB Address is read correctly 
    freq_counter = rm.open_resource(freq_counter_usb)
except pyvisa.errors.VisaIOError:
    print("The 53230A Frequency Counter is not found!\nPlease check for connection.")
    messagebox.showinfo("Fail!",message="USB Address was incorrect, please check the connection!")

root = Tk()                                                                                                    #This section builds the gui frame
root.title("Clock Trip Calibration")
photo = PhotoImage(file = "C:/Users/KaiHall/PyApp/PyClockApp/pyclockapp_pic.png")
root.iconphoto(False, photo)
mainframe = ttk.Frame(root, padding="10 4 4 4")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

class FC:                                                                                                       #Creating the FC class enables the use of global variables and functions 

    '''Keysight 53230A Universal Frequency Counter/Timer Gui Time Interval measurment '''

    output_fileloc = StringVar()                                                                                #Initizaling all the global variables to either String or Integer or Float
    ch_signal = IntVar()
    measurement_mode = IntVar()
    measure_mode = IntVar()
    user_fileloc = StringVar()
    seconds_spin = IntVar()
    samples_spin = IntVar()
    avg_spin = IntVar()
    sample_output = StringVar()
    output_fileloc = StringVar()
    ch1_signal = IntVar()
    ch2_signal = IntVar()
    progress_bar = IntVar()
    user_input_mintues = IntVar()
    user_input_hours = IntVar()
    average_sample = IntVar()
    mjd = float()
    current_date = 0
    samples_run = IntVar()
    measurement_start_time = IntVar()
    timeout_min = IntVar()
    timeout_hrs = float()
    timeout_start = float()
    file_string = StringVar()
    measurement_end_time = StringVar()
    timeout_end = StringVar() 
    new_data = StringVar()
    
    def __init__(self) -> None:                                                                                 
         pass
#############################################################-------Functions-------##################################################################
    def julian_date():
        ''' Coverts UTC to Julian Date'''
        #Striping thing relevant numbers of UTC
        hour_utc = dt.datetime.utcnow().hour
        min_utc = dt.datetime.utcnow().minute
        sec_utc = dt.datetime.utcnow().second
        month_utc = dt.datetime.utcnow().month
        year_utc = dt.datetime.utcnow().year
        day_utc = dt.datetime.utcnow().day
        tsc= dt.datetime.utcnow().microsecond
        #Calculation of JD and MJD
        tA = math.floor((14-month_utc)/12)
        julian_year = (year_utc + 4800 - tA)
        julian_month = (month_utc + (12*tA)-3)
        jdn = (day_utc + math.floor(((153*julian_month+2)/5) + (365*julian_year) + math.floor(julian_year/4) 
                                        - math.floor(julian_year/100) + math.floor(julian_year/400) - 32045))
        FC.mjd = ((jdn + ((hour_utc-12)/24) + (min_utc/1400) + (tsc/86400)) - 2400000.5)
        return FC.mjd

    def display_mdj():
        '''Pop up box for the display MJD button'''                                                                      
        FC.julian_date()
        messagebox.showinfo("The MJD ", message=FC.julian_date())

    def display_time():
        '''Calulates the current time for output variables'''
        FC.samples_run = 0
        FC.timeout_min = 60*(FC.user_input_mintues.get())
        FC.timeout_hrs = (FC.user_input_hours.get())/60
        FC.timeout_start = time.time()
        FC.measurement_start_time = (time.asctime(time.localtime(FC.timeout_start)))
        FC.file_string = FC.measurement_start_time + ".txt"
        FC.timeout_end = time.time()
        FC.measurement_end_time = (time.asctime(time.localtime(FC.timeout_end)))                               

        return FC.samples_run,FC.timeout_min, FC.timeout_hrs, FC.timeout_start,FC.measurement_start_time, FC.file_string, FC.timeout_end, FC.measurement_end_time

    def file_save():
        '''Creates a text docutment of readings at user location or default location'''
        FC.julian_date()
        file = FC.output_fileloc
        #temp_file = 'C:\Users\KaiHall\Desktop'                                                             #Keep temp_file variable if you need to change the default file locaiton
        try:
            with open(file, "a") as textfile:                                                               #Python is creating/opening/writing to the file variable, appending the data
                textfile.write(f"{FC.samples_run}    {FC.mjd}     {FC.new_data}\n")
                FC.samples_run +=1
                print(f"Sample {FC.samples_run} completed at {FC.measurement_end_time}"'\n')
                time.sleep(FC.seconds_spin.get())
        except FileNotFoundError and TypeError:                                                         
            with open('C:/Users/KaiHall/Desktop/temp_file_data.txt', "a") as textfile:                      #Default folder needs to be updated for each laptop using the app 
                textfile.write(f"{FC.samples_run}    {FC.mjd}     {FC.new_data}\n")
                FC.samples_run +=1
                print(f"Sample {FC.samples_run} completed at {FC.measurement_end_time}"'\n')
                time.sleep(FC.seconds_spin.get())
        return  

    def SCPI():
        '''SCPI is the test equipment scipting language'''                                                  #Python is sending and recieving commands, then stripping reapted digits in fetched data 
        freq_counter.write('MEAS:TINT? (@1), (@2)')
        sample_data = freq_counter.query_ascii_values('FETCH?', converter='s') 
        sample_Data = str(sample_data[0])
        if FC.measure_mode.get() == 3:
           FC.new_data = float(sample_Data[:-23])
        else:
            FC.new_data = sample_Data[:-23]
        return 

    def time_interval():
        '''Runs the time interval for an alloted number of samples and with n seconds inbetween each sample'''
        FC.samples_run = 0
        FC.display_time()
        while FC.samples_run < FC.samples_spin.get():
            FC.SCPI()
            FC.file_save() 
        return

    def infinity_samples():
        '''Runs the time interval for a period of time '''
        FC.display_time()
        try:                                                                                                #Try/Except statments for minute/hour ran intervals 
            if FC.timeout_min > 0:                                                                              
                while time.time() < FC.timeout_start + FC.timeout_min:                                      #Adds the local start time to the time selected by the user
                    FC.SCPI()                                                                              
                    FC.timeout_end = time.time()                                                            #Python updating the time stamp variables for the output variables
                    FC.measurement_end_time = (time.asctime(time.localtime(FC.timeout_end))) 
                    FC.file_save()
        except:
            print("You need to add some time")
        try:
            if FC.timeout_hrs > 0:
                while time.time() < FC.timeout_start + FC.timeout_hrs:
                    FC.SCPI()
                    FC.timeout_end = time.time()
                    FC.measurement_end_time = (time.asctime(time.localtime(FC.timeout_end))) 
                    FC.file_save()
        except:
            print("You need to add some time to infinity measurement")   
        return print(f"Infinite Measurement Completed at {FC.measurement_end_time}!")

    def average_samples(samples_run = 0):
        ''' Calcuates an average of 'n' number of samples'''
        sample_list = []                                                                                      #List holding the samples to average
        print(f"Averaging {FC.avg_spin.get()} samples, stand-by..."'\n')
        while samples_run < FC.avg_spin.get():
            FC.SCPI()
            time.sleep(1)
            sample_list.append(FC.new_data)
            samples_run +=1
        numbers = 0
        for i in sample_list:                                                                                  #Adding all the samples together
            numbers += i
        print(sample_list,'\n')
        try:
            FC.average_sample = numbers/len(sample_list)                                                       #Calculating the average 
            FC.display_time()
            FC.file_save()
        except ZeroDivisionError:
            print("You cannot average zero readings. Please enter a number of average samples greater than 0!")   
        print(f'Your average reading is: {FC.average_sample}''\n')      
        return 

    def start(): 
        '''Runing a clock measurement basded on user selections'''
        FC.display_time()
        print(f"The measurements started at {FC.measurement_start_time}"'\n')
        print("Here we go..."'\n')

        if FC.ch1_signal.get() == FC.ch2_signal.get():                                                          
           print("You choose the same single type for two different channels.  Make sure the channel 1 and 2 have different signals!") 
        elif FC.measure_mode.get() == 1:
            try:
                if FC.seconds_spin.get() > 0 and FC.samples_spin.get() > 0: FC.time_interval()
            except:
                print("I need user to enter numbers for samples to read, both number of samples and the time between them!")          
        elif FC.measure_mode.get() == 2: FC.infinity_samples()
        elif FC.measure_mode.get() == 3: FC.average_samples()
        
        return print("PyClock App is Finished. Restart app for another measurment"'\n')

    def choose_file():
        '''Brings up file dictionary for user to select save file location'''
        FC.output_fileloc = filedialog.asksaveasfilename(initialdir="Desktop",defaultextension=("txt"))
    
        return print(f'Your data will be saved at: {FC.output_fileloc}''\n'), FC.output_fileloc   

    def counter_init():
        '''Initializes the counter the the proper settings depending on user selections mode and type of measurment.'''

        freq_counter.write('*CLS; *RST') #Clearing and reseting the counter
        freq_counter.write('SEN:ROSC:EXT') #Sesnsing the external refference as the 5MHz source
        freq_counter.write('SEN:ROSC:EXT:CEC ONCE') #Checking the external refference as the 5MHz source
        freq_counter.write('CONF:TINT (@1),(@2)') # Sets trigger parameters to default values for time interval
        freq_counter.write('INP1:IMP 50;:INP2:IMP 50') # Sets the level of input 1 and 2 and impendance to 50 OHMs 
        
        if FC.ch1_signal.get() == 1 and FC.ch2_signal.get() == 2:
            freq_counter.write('INP1:COUP DC; LEV 1.0;:INP2:COUP AC; LEV 0') #Ch.1 Couping to DC, level to 1V
            print("Channel 1 is set to DC"'\n')
            print("Channel 2 is set to AC"'\n')
        
        elif FC.ch1_signal.get() == 2 and FC.ch2_signal.get() == 1:
            freq_counter.write('INP1:COUP AC; LEV 0;:INP2:COUP DC; LEV 1.0') #Ch.1 Couplling to AC for Sine Wave, level to 0V
            print("Channel 1 is set to AC"'\n')
            print("Channel 2 is set to DC"'\n')
    
        else:
            print("------You didn't select a mode setting for Channel 1 and 2! \nSelect channel pulse and initization again.-----")
            freq_counter.write('*CLS; *RST') 

        return print("Initialization is Complete"'\n')         
##################################################################-------Gui Layout-------#############################################################
ttk.Label(mainframe, text="Channel 1 Signal:").grid(column=0, row=1)
ch1_1pps = ttk.Radiobutton(mainframe, text='1PPS', variable=FC.ch1_signal, value=1)
ch1_1pps.grid(column=1, row=1, sticky="W")
ch1_sine_wave = ttk.Radiobutton(mainframe, text='Sine Wave', variable=FC.ch1_signal, value=2)
ch1_sine_wave.grid(column=2, row=1)

ttk.Label(mainframe, text="Channel 2 Signal:").grid(column=0, row=2)
ch2_2pps = ttk.Radiobutton(mainframe, text='1PPS', variable=FC.ch2_signal, value=1)
ch2_2pps.grid(column=1, row=2, sticky="W")
ch2_sine_wave = ttk.Radiobutton(mainframe, text='Sine Wave', variable=FC.ch2_signal, value=2)
ch2_sine_wave.grid(column=2, row=2)

ttk.Button(mainframe, text="Initialize Counter", command=FC.counter_init).grid(column=0, row=4, pady=4,padx=2, columnspan=2)
ttk.Button(mainframe, text="Display MJD", command=FC.display_mdj).grid(column=1, row=4, pady=4,padx=2, columnspan=2)

ttk.Label(mainframe, text="File To Save Data:").grid(column=0, row=6)
ttk.Button(mainframe, text="Choose File", command=FC.choose_file).grid(column=1, row=6, pady=8, sticky="W")

ttk.Label(mainframe, text="Measurement Mode:").grid(column=0, row=8, pady=7)
single_shot_mode = ttk.Radiobutton(mainframe, text='Single-Shot',variable=FC.measure_mode, value=1)
single_shot_mode.grid(column=1, row=8, pady=7, sticky="W")

ttk.Label(mainframe, text="Seconds\nBetween Readings (0-100):").grid(column=0, row=9, sticky="W")
single_shot_seconds = ttk.Spinbox(mainframe, from_=1, to=100, textvariable=FC.seconds_spin, width=6)  
single_shot_seconds.grid(column=1, row=9, pady=8)
        
ttk.Label(mainframe, text="Samples:").grid(column=0, row=10, sticky="W")
number_samples = ttk.Spinbox(mainframe, from_=1, to=9999999, textvariable=FC.samples_spin, width=6) 
number_samples.grid(column=1, row=10, pady=8)

ttk.Label(mainframe, text="Measurement Mode:").grid(column=0, row=11, pady=7)
infinite_mode = ttk.Radiobutton(mainframe, text='Infinite',variable=FC.measure_mode, value=2)
infinite_mode.grid(column=1, row=11, pady=7, sticky="W")

ttk.Label(mainframe, text="Hours:").grid(column=0, row=12, sticky="E")
user_input_hours = ttk.Spinbox(mainframe, from_=1, to=25, textvariable=FC.user_input_hours, width=6)
user_input_hours.grid(column=1, row=12, pady=8)
        
ttk.Label(mainframe, text="Mintutes:").grid(column=0, row=13, sticky="E")
user_input_mintues = ttk.Spinbox(mainframe, from_=1, to=59, textvariable=FC.user_input_mintues, width=6)
user_input_mintues.grid(column=1, row=13, pady=8)

ttk.Label(mainframe, text="Measurement Mode:").grid(column=0, row=14, pady=10)
average_mode = ttk.Radiobutton(mainframe, text='Averaged', variable=FC.measure_mode, value=3)
average_mode.grid(column=1, row=14, pady=10)

ttk.Label(mainframe, text="Average Samples\n(2-99,000,000):").grid(column=0, row=15, sticky="W")
avg_spin_entry = ttk.Spinbox(mainframe, from_=1, to=100, textvariable=FC.avg_spin, width=6)
avg_spin_entry.grid(column=1, row=15, pady=8)  

ttk.Label(mainframe, textvariable=FC.sample_output).grid(column=3, row=13, columnspan=4)
measure_button = ttk.Button(mainframe, text="Start Reading", command=FC.start).grid(column=3, row=15, pady=3)

root.mainloop()