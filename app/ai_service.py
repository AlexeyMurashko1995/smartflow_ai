from openai import AsyncOpenAI
from app.schemas import AIExpenseExtract

async def extract_expense_from_text(text: str) -> AIExpenseExtract:
    client = AsyncOpenAI(api_key='test')
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
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        response_format=AIExpenseExtract,
    )
    return response.choices[0].message.parsed


async def transcribe_audio(audio_bytes: bytes) -> str:
    client = AsyncOpenAI(api_key='test')
    response = await client.audio.transcriptions.create(
        model="whisper-1",
        file=("voice.ogg", audio_bytes, "audio/ogg")
    )
    return response.text