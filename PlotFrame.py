import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import spectrogram
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#class Frame:
#    def __init__(self, audio_data, sample_rate):
#        self.audio_data = audio_data
#        self.sample_rate = sample_rate
#
#    def plot_time_domain(self):
#        if self.audio_data is not None:
#            self.ax_time.clear()
#            self.ax_time.plot(np.linspace(0, len(self.audio_data) / self.sample_rate, num=len(self.audio_data)), self.audio_data)
#            self.ax_time.set_title('Time Domain Signal')
#            self.ax_time.set_xlabel('Time [s]')
#            self.ax_time.set_ylabel('Amplitude')
#            self.ax_time.grid()
#            self.canvas_time.draw()
#
#    def plot_time_frequency(self):
#        if self.audio_data is not None:
#            self.ax_freq.clear()
#            f, t, Sxx = spectrogram(self.audio_data, self.sample_rate)
#            c = self.ax_freq.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
#            self.ax_freq.set_title('Time-Frequency Representation')
#            self.ax_freq.set_ylabel('Frequency [Hz]')
#            self.ax_freq.set_xlabel('Time [s]')
#            plt.colorbar(c, ax=self.ax_freq, label='Intensity [dB]')
#            self.ax_freq.set_ylim(0, self.sample_rate / 2)  # Display only up to Nyquist frequency
#            self.canvas_freq.draw()
#
#class AudioApp:
#    def __init__(self, root):
#        self.root = root
#        self.root.title("Audio Frame Viewer")
#
#        self.load_button = tk.Button(root, text="Load Audio File", command=self.load_audio)
#        self.load_button.pack(pady=20)
#
#        self.plot_time_button = tk.Button(root, text="Plot Time Domain", command=self.plot_time_domain, state=tk.DISABLED)
#        self.plot_time_button.pack(pady=5)
#
#        self.plot_freq_button = tk.Button(root, text="Plot Time-Frequency", command=self.plot_time_frequency, state=tk.DISABLED)
#        self.plot_freq_button.pack(pady=5)
#
#        self.audio_data = None
#        self.sample_rate = None
#
#        # 创建 matplotlib 图形和坐标轴
#        self.fig, self.ax = plt.subplots(figsize=(8, 4))
#        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
#        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
#
#    def load_audio(self):
#        file_path = filedialog.askopenfilename(title="Select Audio File", filetypes=[("WAV files", "*.wav")])
#        if file_path:
#            self.sample_rate, self.audio_data = wavfile.read(file_path)
#            if self.audio_data.ndim > 1:  # If stereo, take one channel
#                self.audio_data = self.audio_data[:, 0]
#            self.plot_time_button.config(state=tk.NORMAL)
#            self.plot_freq_button.config(state=tk.NORMAL)
#
#    def plot_time_domain(self):
#        if self.audio_data is not None:
#            frame = Frame(self.audio_data, self.sample_rate)
#            frame.plot_time_domain(self.ax)
#
#    def plot_time_frequency(self):
#        if self.audio_data is not None:
#            frame = Frame(self.audio_data, self.sample_rate)
#            frame.plot_time_frequency(self.ax)
#
#if __name__ == "__main__":
#    root = tk.Tk()
#    app = AudioApp(root)
#    root.mainloop()
#


import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import spectrogram
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AudioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Frame Viewer")

        self.load_button = tk.Button(root, text="Load Audio File", command=self.load_audio)
        self.load_button.pack(pady=20)

        self.plot_time_button = tk.Button(root, text="Plot Time Domain", command=self.plot_time_domain, state=tk.DISABLED)
        self.plot_time_button.pack(pady=5)

        self.plot_freq_button = tk.Button(root, text="Plot Time-Frequency", command=self.plot_time_frequency, state=tk.DISABLED)
        self.plot_freq_button.pack(pady=5)

        # 创建 matplotlib 图形和坐标轴
        self.fig_time, self.ax_time = plt.subplots(figsize=(8, 4))
        self.canvas_time = FigureCanvasTkAgg(self.fig_time, master=root)
        self.canvas_time.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.fig_freq, self.ax_freq = plt.subplots(figsize=(8, 4))
        self.canvas_freq = FigureCanvasTkAgg(self.fig_freq, master=root)
        self.canvas_freq.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.audio_data = None
        self.sample_rate = None

    def load_audio(self):
        file_path = filedialog.askopenfilename(title="Select Audio File", filetypes=[("WAV files", "*.wav")])
        if file_path:
            self.sample_rate, self.audio_data = wavfile.read(file_path)
            if self.audio_data.ndim > 1:  # If stereo, take one channel
                self.audio_data = self.audio_data[:, 0]
            self.plot_time_button.config(state=tk.NORMAL)
            self.plot_freq_button.config(state=tk.NORMAL)

    def plot_time_domain(self):
        if self.audio_data is not None:
            self.ax_time.clear()
            self.ax_time.plot(np.linspace(0, len(self.audio_data) / self.sample_rate, num=len(self.audio_data)), self.audio_data)
            self.ax_time.set_title('Time Domain Signal')
            self.ax_time.set_xlabel('Time [s]')
            self.ax_time.set_ylabel('Amplitude')
            self.ax_time.grid()
            self.canvas_time.draw()

    def plot_time_frequency(self):
        if self.audio_data is not None:
            self.ax_freq.clear()
            f, t, Sxx = spectrogram(self.audio_data, self.sample_rate)
            c = self.ax_freq.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
            self.ax_freq.set_title('Time-Frequency Representation')
            self.ax_freq.set_ylabel('Frequency [Hz]')
            self.ax_freq.set_xlabel('Time [s]')
            plt.colorbar(c, ax=self.ax_freq, label='Intensity [dB]')
            self.ax_freq.set_ylim(0, self.sample_rate / 2)  # Display only up to Nyquist frequency
            self.canvas_freq.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioApp(root)
    root.mainloop()



#import tkinter as tk
#from tkinter import ttk
#import pyaudio
#import numpy as np
#from scipy.fftpack import fft
#import matplotlib.pyplot as plt
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
#
#class AudioApp:
#    def __init__(self, root):
#        self.root = root
#        self.root.title("Audio Visualization")
#        
#        # Create main frame
#        mainframe = ttk.Frame(root, padding="10 10 10 10")
#        mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
#        
#        # Create time domain plot
#        self.fig_time, self.ax_time = plt.subplots()
#        self.ax_time.set_title("Time Domain")
#        self.canvas_time = FigureCanvasTkAgg(self.fig_time, master=mainframe)
#        self.canvas_time.get_tk_widget().grid(row=0, column=0)
#        
#        # Create frequency domain plot
#        self.fig_freq, self.ax_freq = plt.subplots()
#        self.ax_freq.set_title("Frequency Domain")
#        self.canvas_freq = FigureCanvasTkAgg(self.fig_freq, master=mainframe)
#        self.canvas_freq.get_tk_widget().grid(row=1, column=0)
#        
#        # Initialize audio stream
#        self.chunk = 1024
#        self.rate = 44100
#        self.p = pyaudio.PyAudio()
#        self.stream = self.p.open(format=pyaudio.paInt16,
#                                  channels=1,
#                                  rate=self.rate,
#                                  input=True,
#                                  frames_per_buffer=self.chunk)
#        
#        # Start updating plots
#        self.update_plots()
#    
#    def update_plots(self):
#        data = np.frombuffer(self.stream.read(self.chunk), dtype=np.int16)
#        
#        # Update time domain plot
#        self.ax_time.clear()
#        self.ax_time.plot(data)
#        self.ax_time.set_title("Time Domain")
#        self.canvas_time.draw()
#        
#        # Update frequency domain plot
#        freqs = fft(data)
#        freqs = np.abs(freqs[:len(freqs)//2])
#        self.ax_freq.clear()
#        self.ax_freq.plot(freqs)
#        self.ax_freq.set_title("Frequency Domain")
#        self.canvas_freq.draw()
#        
#        # Schedule next update
#        self.root.after(50, self.update_plots)
#
#if __name__ == "__main__":
#    root = tk.Tk()
#    app = AudioApp(root)
#    root.mainloop()