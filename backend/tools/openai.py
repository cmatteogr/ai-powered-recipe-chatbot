"""

"""
from openai import Client


class OpenAIClient:
    _instance = None

    def __new__(cls, api_key=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = Client(api_key=api_key)
        return cls._instance

    def query_to_chatgpt(self, system_content: str, user_content: str, model: str = 'gpt-3.5-turbo'):
        """
        Query to chat GPT
        :param system_content: system content
        :param user_content: user content
        :param model: model
        :return: model response
        """
        print("Querying to chat GPT")
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ]
        )
        return response.choices[0].model_dump()['message']['content']
