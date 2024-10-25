#!/usr/bin/env python3
"""Simple GUI for recording into a WAV file.

There are 3 concurrent activities: GUI, audio callback, file-writing thread.

Neither the GUI nor the audio callback is supposed to block.
Blocking in any of the GUI functions could make the GUI "freeze", blocking in
the audio callback could lead to drop-outs in the recording.
Blocking the file-writing thread for some time is no problem, as long as the
recording can be stopped successfully when it is supposed to.

"""

import os
import ctypes
from ctypes import *
class AlgoProcess:
    def __init__(self, value=None):
        BLOCK_SIZE_MAX = 1024
        CHAN_NUM_MAX =16
        para = c_void_p(None)
        path = os.getcwd()
        parafile = path+r'\resources\main_mic.apu'
        AudioLib = ctypes.CDLL(path+r'\resources\mylib.dll') # default path
        print(AudioLib)
        AudioLib.Lib_Init.argtypes = [c_void_p,c_char_p]
        AudioLib.Lib_Init.restype = ctypes.c_void_p        

        para = c_void_p(None)
        self.func_init= AudioLib.Lib_Init
        self.Vc_ptr=self.func_init(byref(para),c_char_p(parafile.encode('utf-8')))
        if self.Vc_ptr is None:
            print("Lib_Init failed")
        else:
            print("Lib_Init succeeded")

        # init the data and the process function
        AudioLib.Lib_Process.argtypes = [c_void_p,c_void_p,c_void_p]
        AudioLib.Lib_Process.restype = c_int
        IntArray10 = c_float*(BLOCK_SIZE_MAX*CHAN_NUM_MAX)
        self.dataIn = IntArray10()
        self.dataOut = IntArray10()
        self.func_process = AudioLib.Lib_Process
        #self.func_process(self.Vc_ptr,byref(self.dataIn),byref(self.dataOut))
 
    def process(self):
        self.func_process(self.Vc_ptr,byref(self.dataIn),byref(self.dataOut)) 
    def destory(self):
        self.func_process(self.Vc_ptr,byref(self.dataIn),byref(self.dataOut)) 