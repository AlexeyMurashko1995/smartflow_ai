import json
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from app.schemas import AIExpenseExtract

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


async def extract_expense_from_text(text: str) -> AIExpenseExtract:
    system_prompt = (
        "You are an intelligent financial assistant. Analyze user text and extract expense details.\n\n"
        "Rules:\n"
        "1. Extract 'amount' (number), 'category_name' (string), and 'description' (string or null).\n"
        "2. If multiple expenses are mentioned, sum them up into a single total amount.\n"
        "3. Be concise and accurate with category names.\n"
        "4. Return strictly a JSON object with keys: 'amount', 'category_name', 'description'."
    )

    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        response_format={"type": "json_object"},
    )

    data = json.loads(response.choices[0].message.content)
    return AIExpenseExtract(**data)


async def transcribe_audio(audio_bytes: bytes) -> str:
    response = await client.audio.transcriptions.create(
        model="whisper-large-v3-turbo",
        file=("voice.ogg", audio_bytes, "audio/ogg")
    )
    return response.text