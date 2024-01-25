from openai import OpenAI
import webrtcvad
import pyaudio

import time
import wave
import sys
import os
import datetime

class Listen:

    def __init__(self, model="whisper-1", aggressiveness=2, buffer_duration=2, min_speech_duration=2, post_speech_duration=0.5 ):

        self.client = OpenAI()
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
    
        self.buffer_duration = buffer_duration
        self.audio_buffer = []
        self.speech_frames = []
        self.MAX_BUFFER_FRAMES = int(self.buffer_duration * 1000 / self.FRAME_LENGTH)

        self.is_speech_detected = False
        self.output_directory = "recordings"
        self.current_audio_file = None
        self.current_wave_file = None

        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        self.min_speech_duration = min_speech_duration  # Minimum duration to qualify as speech (in seconds)
        self.post_speech_duration = post_speech_duration  # Duration to wait after speech ends (in seconds)
        self.speech_start_time = None
        self.last_speech_time = None


    def start(self):
        self.is_recording = True

    def stop(self):
        self.is_recording = False 
    def get_clip(self):
        
        frame = self.stream.read(self.SAMPLES_PER_FRAME)
        is_speech = self.vad.is_speech(frame, self.RATE)
        current_time = time.time()

        if is_speech:
            if not self.is_speech_detected:
                self.is_speech_detected = True
                self.speech_start_time = current_time
                self.start_new_file()

            self.last_speech_time = current_time
            self.current_wave_file.writeframes(frame)

        elif self.is_speech_detected:
            # Check if speech duration was long enough and if post-speech silence duration has passed
            if current_time - self.speech_start_time >= self.min_speech_duration and current_time - self.last_speech_time >= self.post_speech_duration:
                transcript = self.close_file_and_transcribe() 
                return transcript 
        
        return None

    def run(self):
        self.start()
        while self.is_recording:
            frame = self.stream.read(self.SAMPLES_PER_FRAME)
            is_speech = self.vad.is_speech(frame, self.RATE)
            current_time = time.time()

            if is_speech:
                if not self.is_speech_detected:
                    self.is_speech_detected = True
                    self.speech_start_time = current_time
                    self.start_new_file()

                self.last_speech_time = current_time
                self.current_wave_file.writeframes(frame)

            elif self.is_speech_detected:
                # Check if speech duration was long enough and if post-speech silence duration has passed
                if current_time - self.speech_start_time >= self.min_speech_duration and current_time - self.last_speech_time >= self.post_speech_duration:
                    self.close_file_and_transcribe()

    def transcribe_speech_frames(self):
        audio_data = b''.join(self.speech_frames)
        with io.BytesIO() as wav_io:
            with wave.open(wav_io, 'wb') as wav_file:
                wav_file.setnchannels(self.CHANNELS)
                wav_file.setsampwidth(pyaudio.PyAudio().get_sample_size(self.FORMAT))
                wav_file.setframerate(self.RATE)
                wav_file.writeframes(audio_data)
        
            wav_io.seek(0)
            transcript = self.transcribe(wav_io)
            print("Transcript:", transcript)
    def start_new_file(self):
        self.is_speech_detected = True
        filename = os.path.join(self.output_directory, datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".wav")
        self.current_audio_file = open(filename, 'wb')
        self.current_wave_file = wave.open(self.current_audio_file, 'wb')
        self.current_wave_file.setnchannels(self.CHANNELS)
        self.current_wave_file.setsampwidth(pyaudio.PyAudio().get_sample_size(self.FORMAT))
        self.current_wave_file.setframerate(self.RATE)
        self.file_start_time = time.time()

    def close_file_and_transcribe(self):
        self.current_wave_file.close()
        self.current_audio_file.close()

        # Calculate the duration of the recording
        recording_duration = time.time() - self.file_start_time

        # Get the path of the saved file
        saved_file_path = self.current_audio_file.name

        # Reset the flag
        self.is_speech_detected = False

        # Check if the recording is long enough
        if recording_duration >= self.min_speech_duration:
            # Open the saved file for reading
            with open(saved_file_path, 'rb') as audio_file:
                # Transcribe the audio
                transcript = self.transcribe(audio_file)
                return transcript
        else:
            print(f"Discarding short audio file (Duration: {recording_duration:.2f}s).")
            os.remove(saved_file_path)
        return None
    
        

    def transcribe(self, audio_bytes):
        try:
            transcript = self.client.audio.transcriptions.create(
                model=self.model, 
                file=audio_bytes,
                response_format="text"
                )
        except Exception as e: 
            print("error: ", e)
            return None

        return transcript

#does the transcribe function work?
#listen = Listen() 
#listen.run()
#audio_file= open("../tests/data/audio_file.wav", "rb")
#print(listen.transcribe(audio_file))



    