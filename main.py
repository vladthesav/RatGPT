import threading
from src.Listen import Listen


#listen to user and transcribe
listen = Listen()

#talk to LLM
chat = Chat() 

#prepare response using TTS 
speak = Speak() 

listen_thread = None

def main():
    global listen_thread

    # Start the listening thread
    listen_thread = threading.Thread(target=listen_and_respond)
    listen_thread.start()

    try:
        # Keep the main thread running until interrupted
        while True:
            time.sleep(1)  # Or perform other tasks here
    except KeyboardInterrupt:
        print("Stopping...")
        listen_thread.stop()

    # Gracefully stop the listening thread
    listen.stop()
    listen_thread.join()

def listen_and_respond():
    listen.start()

    while listen.is_recording:
        # Do whatever you want with the transcribed text
        # For example, print it, send it to an API, etc.
        transcript = listen.transcribe()
        print(f"Transcribed text: {transcript}")

if __name__ == '__main__':
    main()
