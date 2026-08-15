from openai import AsyncOpenAI
from app.schemas import AIExpenseExtract

async def extract_expense_from_text(text: str) -> AIExpenseExtract:
    client = AsyncOpenAI(base_url="https://api.groq.com/openai/v1")
    system_prompt = (
    "You are an intelligent financial assistant. Your task is to analyze user text "
    "and extract expense details into the structured format.\n\n"
    "Follow these strict rules:\n"
    "1. Extract the expense amount, category name, and a short description.\n"
    "2. If the user mentions multiple expenses in a single message, sum them up "
    "into a single total amount.\n"
    "3. Be concise and accurate with category names."
)
    response = await client.beta.chat.completions.parse(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        response_format=AIExpenseExtract,
    )
    return response.choices[0].message.parsed


async def transcribe_audio(audio_bytes: bytes) -> str:
    client = AsyncOpenAI(base_url="https://api.groq.com/openai/v1")
    response = await client.audio.transcriptions.create(
        model="whisper-large-v3-turbo",
        file=("voice.ogg", audio_bytes, "audio/ogg")
    )
    return response.text