import MenuWindow
import tkinter as tk
from tkinter import ttk
import sounddevice as sd
import queue
import numpy as np

import threading
from FileThread import FileWriting
from FileThread import FileReading
from AlgoProcess import AlgoProcess
from ctypes import c_float 
import time
import sys
import soundfile as sf
import argparse
import argparse

import sounddevice as sd
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)

class DeviceStream:
    
    def __init__(self, value=None):
        self.stream = None
        self.play_stream = None
        self.play_buffersize = 2
        self.play_blocksize = 512

        self.peak =0
        self.input_device = sd.query_hostapis(sd.default.hostapi)['default_input_device']
        self.output_device = sd.query_hostapis(sd.default.hostapi)['default_output_device']
        self.recording =0
        self.Info = ''
        self.input_audio_q = queue.Queue()
        self.output_audio_q = queue.Queue()
        self.metering_q = queue.Queue(maxsize=1)
        self.instance = AlgoProcess()
    def input_audio_callback(self, indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if self.recording:
            self.input_audio_q.put(indata.copy())
            self.previously_recording = True
            c_float_array = indata.astype(np.ctypeslib.as_ctypes_type(c_float))
            for j in range(self.stream.channels):
                for i in range(self.stream.blocksize):
                    self.instance.dataIn[j*self.stream.blocksize + i] = c_float_array[i,j]
            self.instance.process()
            self.angle = float(self.instance.dataOut[0])
        else:
            if self.previously_recording:
                self.input_audio_q.put(None)
                self.previously_recording = False

        self.peak = max(self.peak, np.max(np.abs(indata)))
        try:
            self.metering_q.put_nowait(self.peak)
        except queue.Full:
            pass
        else:
            self.peak = 0


    def create_stream(self, device,filename):
        if self.stream is not None:
            self.stream.abort()
            self.stream.stop()
            self.stream.close()
        self.input_device = device
        print('start>>>>>>')
        #print(self.stream.samplerate)
        self.stream = sd.InputStream(
            device=device, channels=2, callback=self.input_audio_callback)
        self.recording =True

        self.stream.start()
        self.thread = threading.Thread(
            target=FileWriting.file_writing_thread,
            kwargs=dict(
                file=filename,
                mode='x',
                samplerate=int(self.stream.samplerate),
                channels=self.stream.channels,
                q=self.input_audio_q,
            ),
        )
        self.thread.start()
    def stop_stream(self, *args):
        self.recording = False
        #self.wait_for_thread()
        print('end')
        self.thread.join() 
        print('end2<<<<<<')

    def output_audio_callback(self, outdata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        #assert frames == args.blocksize
        if status.output_underflow:
            print('Output underflow: increase blocksize?', file=sys.stderr)
            raise sd.CallbackAbort
        assert not status
        try:
            data = self.output_audio_q.get_nowait()
        except queue.Empty as e:
            print('Buffer is empty: increase buffersize?', file=sys.stderr)
            raise sd.CallbackAbort from e
        if len(data) < len(outdata):
            outdata[:len(data)] = data
            outdata[len(data):] = b'\x00' * (len(outdata) - len(data))
            raise sd.CallbackStop
        else:
            outdata[:] = data

    def create_play_stream(self, device,filename):
        if self.play_stream is not None:
            self.play_stream.abort()
            self.play_stream.close()
        f= sf.SoundFile(filename)
        self.play_stream = sd.RawOutputStream(
                samplerate=f.samplerate, blocksize=self.play_blocksize,
                device=device, channels=f.channels, dtype='float32',
                callback=self.output_audio_callback)
        
        self.thread = threading.Thread(
            target=FileReading.file_read_thread,
            kwargs=dict(
                filename=filename,
                q=self.output_audio_q,
                play_blocksize = self.play_blocksize,
            ),
        )
        self.thread.start()
        self.play_stream.start()
    def stop_play_stream(self, *args):
        print('play end')
        self.thread.join() 
        print('play end2')

def main():
    root = tk.Tk()
    #root.withdraw()
    testMenu = MenuWindow.SettingsWindow(root,'test')
    filename = 'E:\Project\PythonAudio\AudioTestBench\hongge2.wav'
    #root.mainloop()
    recordfilename ='out.wav'
    print('debug')
    test = DeviceStream()
    print(test.input_device)
    print(test.output_device)
    print(testMenu.output_dev['name'])
    test.create_stream(testMenu.input_dev['index'],recordfilename)
    #test.create_stream(testMenu.output_dev['index'],filename)
    test.create_play_stream(testMenu.output_dev['index'],filename)
    print(testMenu.input_dev['index'])
    print(testMenu.output_dev['index'])
    #test.stop_stream(testMenu.input_dev['index'])
    root.mainloop()

if __name__ == '__main__':
    main()