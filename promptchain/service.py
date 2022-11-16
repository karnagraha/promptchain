import openai

class GPT3:
    def __init__(self, api_key):
        openai.api_key = api_key
        self.engine = engine
    
    def call(self, prompt):
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=["\n"],
        )
        return response.choices[0].text

class Loopback:
    def __init__(self, *args, **kwargs):
        pass
    
    def call(self, prompt):
        return prompt