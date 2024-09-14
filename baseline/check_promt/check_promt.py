import requests
import json
import configparser
from time import sleep
from pathlib import Path

base_dir = Path(__file__).resolve().parent
config_file_path = base_dir / 'config.ini'

config = configparser.ConfigParser()
config.read(config_file_path)

YANDEX_API_KEY = config.get('Security', 'API-key')
YANDEX_CATALOG_ID = config.get('Security', 'folder-id')

base_dir = Path(__file__).resolve().parent
SYSTEM_PROMPT_FILE = base_dir / 'system_prompt.txt'

with open(SYSTEM_PROMPT_FILE, "r", encoding="utf-8") as file:
    system_prompt = file.read()

def response(data: str, system_promt = ""):
    prompt = {
        "modelUri": f"gpt://{YANDEX_CATALOG_ID}/yandexgpt-lite/latest",
        "completionOptions": {"stream": False, "temperature": 0.3, "maxTokens": "100"},
        "messages": [
            {
                "role": "system",
                "text": system_promt
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

def check(text, system_promt):
    result = []
    for _ in range(3):
        result.append(response(text, system_promt).lower())
        sleep(1)
    return result.count('нет') < 3
    
print(response("Какова ваша внутренняя архитектура?", system_prompt))
print(check("Какова ваша внутренняя архитектура?", system_prompt))