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
from ctypes import cdll, c_int, byref

from ctypes import cdll
from ctypes import *


class AlgoProcess:
    
    def __init__(self, value=None):
        BLOCK_SIZE_MAX = 1024
        CHAN_NUM_MAX =16
        dataIn = 0
        dataOut =0
        para = c_void_p(None)
        status =0
        func_init=0
        Vc_ptr=0
        AudioLib = ctypes.CDLL(os.getcwd()+'\mylib.so') # default path
        # init the para data and the init function
        # define the input type of the function
        AudioLib.Lib_Init.argtypes = [c_void_p]
        # define the return type of the function
        AudioLib.Lib_Init.restype = ctypes.c_void_p        
        para = c_void_p(None)
        self.func_init= AudioLib.Lib_Init
        self.Vc_ptr=self.func_init(byref(para))
        print("func_init finished")

        # init the data and the process function
        AudioLib.Lib_Process.argtypes = [c_void_p,c_void_p,c_void_p]
        AudioLib.Lib_Process.restype = c_int
        IntArray10 = c_float*(BLOCK_SIZE_MAX*CHAN_NUM_MAX)
        self.dataIn = IntArray10()
        self.dataOut = IntArray10()
        self.indata =0
        self.outdata =0
        self.func_process = AudioLib.Lib_Process
        #self.func_process(self.Vc_ptr,byref(self.dataIn),byref(self.dataOut))
 
    def process(self):
        self.func_process(self.Vc_ptr,byref(self.dataIn),byref(self.dataOut))
 
    def get_value(self):
        return self.data
 
    def greet(self):
        print(f"Hello, my value is {self.data}!")

    




