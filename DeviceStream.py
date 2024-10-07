import MenuWindow
import tkinter as tk
from tkinter import ttk
import sounddevice as sd
import queue
import numpy as np

import threading
from FileThread import FileWriting
from AlgoProcess import AlgoProcess
from ctypes import c_float 
import time
import sys
import soundfile as sf
import argparse

class DeviceStream:
    
    def __init__(self, value=None):
        self.stream = None
        self.play_stream = None
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
            outdata[len(data):].fill(0)
            raise sd.CallbackStop
        else:
            outdata[:] = data        
            
    def create_play_stream(self, device,filename):
        event = threading.Event()
        try:
            with sf.SoundFile(filename) as f:
                for _ in range(args.buffersize):
                    data = f.read(args.blocksize)
                    if not len(data):
                        break
                    self.output_audio_q.put_nowait(data)  # Pre-fill queue
                    print("pre-fill queue")
                stream = sd.OutputStream(
                    samplerate=f.samplerate, blocksize=args.blocksize,
                    device=args.device, channels=f.channels,
                    callback=self.output_audio_callback, finished_callback=event.set)
                with stream:
                    timeout = args.blocksize * args.buffersize / f.samplerate
                    while len(data):
                        data = f.read(args.blocksize)
                        q.put(data, timeout=timeout)
                    print("fill queue")
                    event.wait()  # Wait until playback is finished
        except KeyboardInterrupt:
            print('\nInterrupted by user')
        except queue.Full:
            # A timeout occurred, i.e. there was an error in the callback
            print("time out occurred")
        except Exception as e:
            print(type(e).__name__ + ': ' + str(e))



        if self.play_stream is not None:
            self.play_stream.stop()
            self.play_stream.close()
        self.output_device = device
        print('play start>>>>>>')
        #print(self.stream.samplerate)
        self.play_stream = sd.OutputStream(
            device=device, channels=2, callback=self.output_audio_callback)
        self.playing =True

        self.play_stream.start()
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
    def stop_play_stream(self, *args):
        print('end')
        self.thread.join() 
        print('end2<<<<<<')



def main():
    root = tk.Tk()
    #root.withdraw()
    testMenu = MenuWindow.SettingsWindow(root,'test')

    #root.mainloop()
    filename ='out.wav'
    test = DeviceStream()
    print(test.input_device)
    print(test.output_device)
    test.create_stream(testMenu.input_dev['index'],filename)
    print(testMenu.input_dev['index'])
    print(testMenu.output_dev['index'])
    time.sleep(10)
    test.stop_stream(testMenu.input_dev['index'])
    root.mainloop()

    
if __name__ == '__main__':
    main()
