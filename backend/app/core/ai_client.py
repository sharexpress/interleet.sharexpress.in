# Copyright 2026 Sharexpress Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
