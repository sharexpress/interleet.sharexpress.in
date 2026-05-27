from openai import OpenAI
from app.core.config import OPENAI_API_KEY


class thatAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    async def generate_text(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = "gpt-4.1-mini",
        json_output: bool = False,
    ):
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format=({"type": "json_object"} if json_output else None),
        )
        return response.choices[0].message.content

    async def text_to_speech(self, text: str, voice: str = "alloy"):
        response = self.client.audio.speech.create(
            model="gpt-4o-mini-tts", voice=voice, input=text
        )
        return response
