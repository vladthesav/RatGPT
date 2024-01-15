from openai import OpenAI


DEFAULT_SYSTEM_PROMPT = """
You are RatGPT, a friendly rat sitting on your shoulder. 
You will help the user with any task.
You will keep it's responses short and to the point, as all outputs will be spoken via a TTS API."""


class Chat:

    def __init__(self, endpoint=None, model="gpt-3.5-turbo",system_prompt = DEFAULT_SYSTEM_PROMPT):

        #set endpoint to something else if we want (e.g. huggingface, litellm, ollama, etc.)
        if endpoint != None: pass 


        self.client = OpenAI()
        
        self.model = model 
        self.messages = [
            {"role": "system", "content":system_prompt}
        ]


    def chat(self, content):
        message ={"role": "user", "content": content}
        self.messages.append(message)


        completion = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages
            )

        output = completion.choices[0].message 

        return output




#sanity check
#chat = Chat() 
#print(chat.chat("hi RatGPT, i want to make ratatouille"))