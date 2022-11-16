import re

# Sample Preprocessor that returns True if the input appears to be true boolean value like
# "true", "1", "t", "y", and otherwise returns False
def BoolPreprocessor(text):
    if re.match(r"^(true|1|t|y)$", text, re.IGNORECASE):
        return True
    return False

class Handler:
    """Basic handler that converts input to output via service."""
    def __init__(self, service):
        """Initialize the handler with a result preprocessor."""
        self.service = service

    def get_prompt(self, input):
        return input

    def handle(self, input):
        prompt = self.get_prompt(input)
        output = self.service.call(prompt)
        return output


class PromptHandler(Handler):
    """Basic handler that formats a provided string template"""
    def __init__(self, prompt, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prompt = prompt

    def get_prompt(self, input):
        return self.prompt.format(input)
