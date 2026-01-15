from openai import AsyncOpenAI  # Naya tarika
import os
from dotenv import load_dotenv

load_dotenv()

class AIEngine:
    def __init__(self):
        # Naye version mein client aise banta hai
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    async def generate_astrology_prediction(self, kundli_data: dict, user_question: str):
        # Data extraction
        panchang = kundli_data.get('data', {}).get('data', {})
        nakshatra = panchang.get('nakshatra', [{}])[0].get('name', 'Unknown')
        tithi = panchang.get('tithi', [{}])[0].get('name', 'Unknown')
        vaara = panchang.get('vaara', 'Unknown')
        
        system_prompt = "You are an expert Vedic Astrologer. Answer queries in Hindi and English."
        
        user_prompt = f"""
        Vedic Context: Nakshatra {nakshatra}, Tithi {tithi}, Day {vaara}.
        Question: {user_question}
        """

        # Naya method call: client.chat.completions.create
        response = await self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content