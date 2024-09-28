#!/usr/bin/env python3
"""Simple GUI for recording into a WAV file.

There are 3 concurrent activities: GUI, audio callback, file-writing thread.

Neither the GUI nor the audio callback is supposed to block.
Blocking in any of the GUI functions could make the GUI "freeze", blocking in
the audio callback could lead to drop-outs in the recording.
Blocking the file-writing thread for some time is no problem, as long as the
recording can be stopped successfully when it is supposed to.

"""
import queue
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import *
import numpy as np
import sounddevice as sd
from ctypes import c_float 
from datetime import datetime

from AlgoProcess import AlgoProcess
from FileThread import FileWriting
#from Led import LED
import MenuWindow

class RecGui(tk.Tk):
    stream = None
  
    def __init__(self):
        super().__init__()
        
        self.device=0
        self.instance = AlgoProcess()
        self.title('SoundSimulation')
        self.geometry('1000x500') 
        
        menubar = Menu(self)
        self.config(menu=menubar)        
        menu1=Menu(menubar,tearoff=False)
        menubar.add_cascade(label='Device Setting',menu=menu1)
        menu1.add_command(label='Source/Device',command=self.on_settings)

        menu3=Menu(menubar,tearoff=False)
        menubar.add_cascade(label='Generation',menu=menu3)
        menu3.add_command(label='Config',command=self.generation_settings)

        self.Info ='NONE'
        self.Info_label = ttk.Label(text=self.Info, font=('Arial', 10),justify="left" )
        self.Info_label.pack(side=tk.BOTTOM,anchor='nw')

        # Frame for simualation status
        f = ttk.Frame().pack()
        self.rec_button = ttk.Button(f)
        self.rec_button.pack(anchor='w')

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
        self.create_stream()
        self.recording = self.previously_recording = False
        self.audio_q = queue.Queue()
        self.audio_temp = queue.Queue()
        self.peak = 0
        self.metering_q = queue.Queue(maxsize=1)

        self.protocol('WM_DELETE_WINDOW', self.close_window)
        self.init_buttons()
        self.update_gui()

    def on_settings(self, *args):
        w = MenuWindow.SettingsWindow(self, 'Input Settings')
        if(w.result!=None):
            print(w.result)
            #self.device =w.result
            self.create_stream(device=w.result)

    def generation_settings(self, *args):
        w = MenuWindow.Generate(self, 'Generate')

    def create_stream(self, device=None,):
        if self.stream is not None:
            self.stream.abort()
            self.stream.stop()
            self.stream.close()
        chan = 2
        if 'USB' in sd.query_devices(self.device)['name']:
            chan = max(16,sd.query_devices(device)['max_input_channels'])
        else:
            chan = 2
        #chan = 2
        print(self.device)
        #print(self.stream.samplerate)
        self.stream = sd.InputStream(
            device=device, channels=chan, callback=self.audio_callback)
        self.stream.start()
        #sd.stream()

    def audio_callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if self.recording:
            self.audio_q.put(indata.copy())
            self.previously_recording = True
            c_float_array = indata.astype(np.ctypeslib.as_ctypes_type(c_float))
            for j in range(self.stream.channels):
                for i in range(self.stream.blocksize):
                    self.instance.dataIn[j*self.stream.blocksize + i] = c_float_array[i,j]
            self.instance.process()
            self.angle = float(self.instance.dataOut[0])
        else:
            if self.previously_recording:
                self.audio_q.put(None)
                self.previously_recording = False

        self.peak = max(self.peak, np.max(np.abs(indata)))
        try:
            self.metering_q.put_nowait(self.peak)
        except queue.Full:
            pass
        else:
            self.peak = 0

    def on_rec(self):
        self.recording = True
        filename = 'Sim_'+datetime.now().strftime('%Y_%m_%d_%H_%M_%S')+'.wav'
        if self.audio_q.qsize() != 0:
            print('WARNING: Queue not empty!')
        self.thread = threading.Thread(
            target=FileWriting.file_writing_thread,
            kwargs=dict(
                file=filename,
                mode='x',
                samplerate=int(self.stream.samplerate),
                channels=self.stream.channels,
                q=self.audio_q,
            ),
        )
        self.thread.start()
        # NB: File creation might fail!  For brevity, we don't check for this.
        self.rec_button['text'] = 'stop'
        self.rec_button['command'] = self.on_stop
        self.rec_button['state'] = 'normal'
        self.file_label['text'] = 'Recording filename:'+filename

    def on_stop(self, *args):
        self.rec_button['state'] = 'disabled'
        self.recording = False
        self.wait_for_thread()

    def wait_for_thread(self):
        self.after(10, self._wait_for_thread)

    def _wait_for_thread(self):
        if self.thread.is_alive():
            self.wait_for_thread()
            return
        self.thread.join()
        self.init_buttons()

    def init_buttons(self):
        self.rec_button['text'] = 'Simulation'
        self.rec_button['command'] = self.on_rec
        if self.stream:
            self.rec_button['state'] = 'normal'

    def update_gui(self):
        self.Info = 'Source device:\n'+sd.query_devices(self.device)['name']+'\tSampleRate:'+str(self.stream.samplerate)+'\tChannel Number.:'+str(self.stream.channels)
        self.Info_label['text'] = self.Info
        try:
            peak = self.metering_q.get_nowait()
        except queue.Empty:
            pass
        else:
            self.meter['value'] = peak
        content = 'DOA(Direction Of Arrival) Angle:'+str(round(self.angle/3.1415926*18)*10)
        self.angle_label['text'] = content
        #self.LedOBJ.LED_Control(int(self.angle/3.1415926*16))
        self.after(500, self.update_gui)

    def close_window(self):
        if self.recording:
            self.on_stop()
        self.destroy()

def main():
    
    app = RecGui()
    app.mainloop()

if __name__ == '__main__':
    main()
