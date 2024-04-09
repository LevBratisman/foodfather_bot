from openai import AsyncOpenAI

from app.config import settings


client = AsyncOpenAI(
    api_key=settings.PROXY_API_KEY,
    base_url=settings.OPENAI_BASE_URL
)

def generate_request(text: str) -> str:
    request = f'Напиши необходимые ингридиенты и пошаговый рецепт для приготовления блюда - {text}, если есть несколько блюд с похожим названием, то выведи их по очереди.'
    return request


async def generate_response(recipe: str) -> str:
    request = generate_request(recipe)
    
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": request}],
    )
    return response.choices[0].message.content
