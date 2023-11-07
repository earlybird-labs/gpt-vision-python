from openai import OpenAI

import logging
import json
from app.config import Config

class Example:
    input: str
    output: str


class OpenAIService:
    """
    This class is used to interact with the OpenAI API.
    """

    def __init__(self, mode, max_retry=2):
        """
        Initialize the OpenAI class with the provided model.
        """
        # API key for OpenAI
        self.api_key = Config.OPENAI_KEY
        # Mapping of model names to their identifiers
        self.model_map = {
            "smart": "gpt-4",
            "fast": "gpt-3.5-turbo-1106",
            "long": "gpt-3.5-turbo-16k",
        }
        # Model to be used for the API call
        self.model = self.model_map[mode]
        self.example_model = Example
        self.max_retry = max_retry
        self.client = OpenAI(api_key=self.api_key)

    def set_params(
        self,
        conversation,
        temperature=0.0,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        max_tokens=None,
        json_output=False,
    ):
        """
        Set the parameters for the OpenAI API call.
        """
        # Create a dictionary with the required parameters
        params = {
            "model": self.model,
            "messages": conversation,
            "temperature": temperature,
            "top_p": top_p,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
        }
        # If max_tokens is not None, add it to the parameters
        if max_tokens is not None:
            params["max_tokens"] = max_tokens

        if json_output:
            params["response_format"] = {
                "type": "json_object",
            }

        return params

    def fix_json(self, message):
        system_prompt = """
            You are a helpful assistant that fixes JSON errors from a string with potential JSON errors,
            your task is to fix the errors and return a valid JSON string.
        """

        conversation = [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": message,
            },
        ]

        params = self.set_params(conversation, temperature=0.0, json_output=True)

        response = self.chat_completion(params)

        return response

    def chat_completion(self, params, json_output=False):
        """
        Call the OpenAI API with the provided parameters and return the response.
        """
        try:
            if json_output:
                params["response_format"] = {
                    "type": "json_object",
                }

            # Call the ChatCompletion.create method with the parameters
            completion = self.client.chat.completions.create(**params)
            
            

            # Extract the message from the response
            message = completion.choices[0].message.content.strip()

            # If json_output is True, call json_completion function
            if json_output:
                return self.json_completion(message)
            else:
                return self.text_completion(message)

        except Exception as e:
            # Log an error if the API call failed
            logging.error(f"Failed to call OpenAI API. Error: {e}")
            return None

    def json_completion(self, message):
        """
        Parse the message as JSON and return it.
        """
        max_retry = self.max_retry

        for retry in range(max_retry):
            try:
                message = json.loads(message)
                break
            except Exception as e:
                # Log a warning if the message could not be parsed as JSON
                logging.warning(f"Failed to parse OpenAI response. Error: {e}")
                if retry < max_retry - 1:  # if not the last retry
                    message = self.fix_json(message)
                else:
                    raise
        return message

    def text_completion(self, message):
        """
        Strip the message if necessary and return it.
        """
        try:
            # Only strip if they are on outside of string
            if message.startswith('"') and message.endswith('"'):
                message = message[1:-1]
        except Exception as e:
            # Log a warning if the message could not be stripped
            logging.warning(f"Failed to strip OpenAI response. Error: {e}")
        return message

if __name__ == "__main__":
    # Instantiate the OpenAIService
    openai_service = OpenAIService(mode="fast")
    # Define a conversation for testing
    conversation = [
        {"role": "system", "content": "You are a helpful assistant who only outputs JSON loadable text."},
        {"role": "user", "content": "Who won the world series in 2020?"},
    ]
    # Set the parameters for the API call
    params = openai_service.set_params(conversation, json_output=True)
    # Call the API and print the response
    response = openai_service.chat_completion(params)
    print(response)
