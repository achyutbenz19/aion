from openai import OpenAI

class VisionLLM:
    def __init__(self):
        self.client = OpenAI()
        self.prompt = """
            You are a vision AI that is taking a screenshot of the user's screen. Take only relevant information into the screen and explain it.
        """

    def vision(self, url):
        response = self.client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "user",
            "content": [
                {"type": "text", "text": "What’s in this image?"},
                {
                "type": "image_url",
                "image_url": {
                    "url": url,
                },
                },
            ],
            }
        ],
        max_tokens=300,
        )
        return(response.choices[0].message.content)
