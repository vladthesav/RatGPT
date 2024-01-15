from openai import OpenAI



class Listen:

    def __init__(self):
        #idk how to do VAD, just going to do ASR first 

        self.client = OpenAI()
        self.model = "whisper-1"


        self.is_recording = False

        #idk what else I need
    
    def start(self):
        self.is_recording = True 

    def stop(self):
        self.is_recording = False 

    def run(self):
        while self.is_recording: 
            #idk what to do here 

            #if we find anything, save audio as bytes and use self.transcribe(....) to get transcription 
            pass

    def transcribe(self, audio_bytes):

        transcript = self.client.audio.transcriptions.create(
            model=self.model, 
            file=audio_file,
            response_format="text"
            )

        return transcript


#does the transcribe function work?
#listen = Listen() 
#audio_file= open("../tests/data/audio_file.wav", "rb")
#print(listen.transcribe(audio_file))



    