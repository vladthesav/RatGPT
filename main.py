from src.Listen import Listen
from src.Speak import Speak
from src.Chat import Chat

listen = Listen()
listen.start()  # Start the listening process

# Initialize the Chat object
llm = Chat()

#TTS 
tts = Speak()

# Main loop to process transcriptions and get responses from the LLM
while True:
    # Wait for a new transcription
    transcription = listen.get_clip()
    if transcription==None: continue 
    #TODO - filter out crap transcriptions

    print("user: ", transcription)

    # Process the transcription with the LLM
    response = llm.chat(transcription)
    print("bot: ",response)

    #now play response using tts
    # Convert the LLM response to speech and play it
    tts.speak(response)

