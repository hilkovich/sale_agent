from config import GPT_Settings
import requests
import json


YANDEX_CATALOG_ID = GPT_Settings.YANDEX_KATALOG_ID
YANDEX_API_KEY = GPT_Settings.YANDEX_API_KEY


def response(data: str):
    prompt = {
        "modelUri": f"gpt://{YANDEX_CATALOG_ID}/yandexgpt-lite/latest",
        "completionOptions": {"stream": False, "temperature": 0.3, "maxTokens": "100"},
        "messages": [
            {
                "role": "system",
                "text": "Ты бизнес консультант. Всегда возвращаешь текст только на русском."
                "В тексте запрещено использовать: фотография, изображение, затем, фото, арафед, arafed, развернутое, описание, *, #",
            },
            {
                "role": "user",
                "text": data,
            },
        ],
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {YANDEX_API_KEY}",
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = json.loads(response.text)

    return result["result"]["alternatives"][0]["message"]["text"]
