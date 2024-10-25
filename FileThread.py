#!/usr/bin/env python3


import soundfile as sf
import sounddevice as sd
import time
import numpy as np

class FileWriting:
    def file_writing_thread(*, q, **soundfile_args):
        """Write data from queue to file until *None* is received."""
        # NB: If you want fine-grained control about the buffering of the file, you
        #     can use Python's open() function (with the "buffering" argument) and
        #     pass the resulting file object to sf.SoundFile().
        with sf.SoundFile(**soundfile_args) as f:
            while True:
                data = q.get()
                if data is None:
                    break
                f.write(data)
class FileReading:
    def file_read_thread(*,filename,q,play_blocksize,event):
        with sf.SoundFile(filename) as f:
            while not event.is_set():
                data = f.buffer_read(play_blocksize, dtype='float32')
                print(q.qsize())
                q.put_nowait(data) 
                print(q.qsize())
                print('==========')
                print(f.tell())
                #q.put(data)
                #time.sleep(0.01)
                if len(data)<play_blocksize:
                    #print(len(data))
                    #print(play_blocksize)
                    #print('play file read')
                    break
            print('file read end') #waiting fro the q data time

def audio_generator(duration, fs):
    t = np.arange(0, duration, 1/fs)  # 时间向量
    freq = 440  # 音调的频率（A4）
    signal = np.sin(2 * np.pi * freq * t)  # 生成正弦波
    yield signal.astype(np.float32)  # 生成音频数据流
 

def main():
    #with sf.SoundFile('E:\Project\PythonAudio\AudioTestBench\myfile.wav', 'r+') as f:
    #    while f.tell() < f.frames:
    #        pos = f.tell()
    #        data = f.read(1024)
    #        f.seek(pos)
    #        f.write(data*2)
    #    f.close()
    filename = 'E:\Project\PythonAudio\AudioTestBench\myfile.wav'
    # 从文件中提取数据和采样率
    data, fs = sf.read(filename, dtype='float32')
    sd.play(data, fs)
    ## sd.play(data, fs)
#
    status = sd.wait()  # 等待，直到文件完成播放
    print(status)

        # 设置音频参数
    duration = 5  # 音频持续时间（秒）
    fs = 48000  # 采样率
    blocksize = 1024  # 块大小
    
    # 打开音频流，并设置回调函数
    stream = sd.OutputStream(callback=audio_generator(duration, fs).__next__,
                            samplerate=fs, blocksize=blocksize,
                            channels=1, dtype=np.float32)
    
    # 开始播放音频
    with stream:
        sd.sleep(duration * 1000)  # 休眠，以确保音频播放时间

    #time.sleep(2)
    #data1, fs1 = sf.read("test02.mp3", dtype='float32')
    #sd.play(data1, fs1)
    #status = sd.wait()  # 等待，直到文件完成播放
#
    ## sd.play(data1, fs1)
#
    #sd.play(data, fs)
    #status = sd.wait()  # 等待，直到文件完成播放
#
    #sd.play(data1, fs1)
    #status = sd.wait()  # 等待，直到文件完成播放


if __name__ == '__main__':
    main()
