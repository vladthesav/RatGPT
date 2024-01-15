from openai import OpenAI


class Speak:

    def __init__(self):
        self.client = OpenAI()
        self.model="tts-1"
        self.voice="alloy"

        #where should TTS output go?
        self.destination = "file"


    def tts(self, text):
        response = self.client.audio.speech.create(
            model=self.model,
            voice=self.voice,
            input=text
            )

        return response

    def stream(self, tts_response, fpath = "out.mp3"):
        #audio needs to go somewhere
        dest = self.destination

        if dest == 'file':
            tts_response.stream_to_file(fpath)
        else: 
            pass

    def speak(self, text):
        tts_response = self.tts(text)
        self.stream(tts_response)



#im too lazy to write unit tests 
#speak = Speak()
#speak.speak("hi there, it's RatGPT")


        
