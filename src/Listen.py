from openai import OpenAI
import webrtcvad
import pyaudio
import threading


import time
import wave
import sys




class Listen:

    def __init__(self, model="whisper-1", aggressiveness=2 ):
        #idk how to do VAD, just going to do ASR first 

        #self.client = OpenAI()
        self.model = "whisper-1"

        self.vad = webrtcvad.Vad(aggressiveness)

        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.FRAME_LENGTH = 30  # milliseconds
        self.SAMPLES_PER_FRAME = int(self.RATE * self.FRAME_LENGTH / 1000)

        p = pyaudio.PyAudio()
        self.stream = p.open(format=self.FORMAT,channels=self.CHANNELS, \
                rate=self.RATE, input=True, \
                frames_per_buffer=self.SAMPLES_PER_FRAME)

        self.is_recording = False
        self.a = None
        
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
    
    def start(self):
            self.is_recording = True

            first_detection = None 
            last_detection = None 
            found_something = False
            since_last_det = None

            self.a = time.time()



    def stop(self):
        self.is_recording = False 
        self.stream.close()
        self.thread.join()

    def run(self):
        self.start()
        while self.is_recording: 
            #read 30ms samples at 16000Hz 
            #and run VAD
            is_speech = self.vad.is_speech(self.stream.read(self.SAMPLES_PER_FRAME), self.RATE)
            
            t = time.time() -  self.a
            if is_speech: print("yee ", t)

    def transcribe(self, audio_bytes):

        transcript = self.client.audio.transcriptions.create(
            model=self.model, 
            file=audio_bytes,
            response_format="text"
            )

        return transcript



#does the transcribe function work?
listen = Listen() 
listen.start()
#audio_file= open("../tests/data/audio_file.wav", "rb")
#print(listen.transcribe(audio_file))



    