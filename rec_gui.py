#!/usr/bin/env python3
"""Simple GUI for recording into a WAV file.

There are 3 concurrent activities: GUI, audio callback, file-writing thread.

Neither the GUI nor the audio callback is supposed to block.
Blocking in any of the GUI functions could make the GUI "freeze", blocking in
the audio callback could lead to drop-outs in the recording.
Blocking the file-writing thread for some time is no problem, as long as the
recording can be stopped successfully when it is supposed to.

"""
import tkinter as tk
from tkinter import ttk
from tkinter import *
from datetime import datetime

from DeviceStream import DeviceStream
#from Led import LED
import MenuWindow
from Led import LED

class RecGui(tk.Tk):
    stream = None
  
    def __init__(self):
        super().__init__()
        self.manageStream = DeviceStream()
        self.title('SoundSimulation')
        self.geometry('1000x500') 
        self.LedOBJ = LED()
        menubar = Menu(self)
        self.config(menu=menubar)        
        menu1=Menu(menubar,tearoff=False)
        menubar.add_cascade(label='Device Setting',menu=menu1)
        menu1.add_command(label='Source/Device',command=self.on_settings)

        menu3=Menu(menubar,tearoff=False)
        menubar.add_cascade(label='Generation',menu=menu3)
        menu3.add_command(label='Config',command=self.generation_settings)

        menu2=Menu(menubar,tearoff=False)
        menubar.add_cascade(label='HELP',menu=menu2)
        menu2.add_command(label='HELP',command=self.generation_Help)


        self.Info ='NONE'
        self.Info_label = ttk.Label(text=self.Info, font=('Arial', 10),justify="left" )
        self.Info_label.pack(side=tk.BOTTOM,anchor='nw')

        # Frame for simualation choice and status
        fbutton = ttk.Frame(self)#.pack(anchor='w')
        fbutton.pack(fill="both", expand=False)
        self.button_text=['Record','Play','VOIP','LounderSpeaker/HearingAid','CarAudio','KWS','ASR','TTS','Meansurement']
        self.buttons=[]
        for i in range(5):
            _button = ttk.Button(fbutton,text=self.button_text[i])
            _button.grid(row=0, column=i, sticky="news")
            self.buttons.append(_button)
        self.buttons[0]['command']=lambda: self.on_simulation(self,0)
        self.buttons[1]['command']=lambda: self.on_simulation(self,1)
        self.buttons[2]['command']=lambda: self.on_simulation(self,2)
        self.buttons[3]['command']=lambda: self.on_simulation(self,3)

        self.file_label = ttk.Label(text='<file name>')
        self.file_label.pack(anchor='w')

        self.angle = 0
        self.angle_label = ttk.Label(text = 'Angle:')
        self.angle_label.pack(anchor='w')

        self.meter = ttk.Progressbar()
        self.meter['orient'] = 'horizontal'
        self.meter['mode'] = 'determinate'
        self.meter['maximum'] = 1.0
        self.meter.pack(fill='x')

        # We try to open a stream with default settings first, if that doesn't
        # work, the user can manually change the device(s)
        self.protocol('WM_DELETE_WINDOW', self.close_window)
        self.recording = False 
        self.play = False
        self.update_gui()
        
    def on_settings(self, *args):
        w = MenuWindow.SettingsWindow(self, 'Settings')
        self.manageStream.input_device = w.input_dev_id
        if 'USB' in w.Info:
            print(self.manageStream.input_device)
            self.LedOBJ = LED()
        self.manageStream.output_device = w.output_dev_id
        self.manageStream.Info = w.Info

    def generation_settings(self, *args):
        w = MenuWindow.Generate(self, 'Generate')

    def generation_Help(self, *args):
        w = MenuWindow.HELP(self, 'Generate')

    def on_simulation(self,*args):
        ID =args[1]
        self.buttons[ID]['text']='stop'
        self.buttons[ID]['command']=lambda: self.on_stop(self,ID)
        self.buttons[ID]['state'] = 'normal'
        if ID==0:  # start recording
            self.recording = True
            filename = 'Sim_'+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+'.wav'
            self.manageStream.create_stream(self.manageStream.input_device,filename)
            self.file_label['text'] = 'Recording filename:'+filename
        if ID==1: # start playing
            #filename = 'Sim_'+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+'.wav'q
            filename = 'E:\Project\PythonAudio\hongge2.wav'
            self.file_label['text'] = 'Playing filename:'+filename
            self.manageStream.create_play_stream(self.manageStream.output_device,filename)
        if ID==2:
            #filename = 'Sim_'+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+'.wav'q
            filename = 'E:\Project\PythonAudio\hongge2.wav'
            self.file_label['text'] = 'Playing filename:'+filename
            self.manageStream.create_voip_stream(self.manageStream.input_device,self.manageStream.output_device,filename)

    def on_stop(self, *args):
        ID =args[1]
        self.buttons[ID]['text']=self.button_text[ID]
        self.buttons[ID]['command']=lambda: self.on_simulation(self,ID)
        self.buttons[ID]['state'] = 'normal'        
        if ID==0:
            self.manageStream.stop_stream(self.manageStream.input_device)
            self.recording = False 
        if ID==1:
            self.manageStream.stop_play_stream(self.manageStream.output_device)
            self.play = False
        if ID==2:
            self.manageStream.stop_voip_stream(self.manageStream.output_device)
            self.play = False
    def update_gui(self):
        self.Info_label['text'] = self.manageStream.Info
        
        self.meter['value'] = self.manageStream.peak/2147483648
        content = 'DOA(Direction Of Arrival) Angle:'+str(round(self.angle/3.1415926*18)*10)
        if self.recording ==True:
            self.angle_label['text'] = content
        if 'USB' in self.manageStream.Info:
            self.LedOBJ.LED_Control(int(self.manageStream.angle/3.1415926*180/11))
        self.after(200, self.update_gui)

    def close_window(self):
        #if self.recording
        #    self.on_stop()
        self.destroy()

def main():
    
    app = RecGui()
    app.mainloop()

if __name__ == '__main__':
    main()
