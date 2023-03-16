import json
import os
import sys
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./venv/lib/python3.8/site-packages"))

import requests
import openai

try:
    TOKEN = os.environ['TELEGRAM_TOKEN']
    OPENAI_KEY = os.environ['OPENAI_KEY']
except KeyError:
    logger.error("Failed to get required environment variable")
    sys.exit(1)

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
openai.api_key = OPENAI_KEY

def gpt(event, context):
    """Processes a message received via Telegram and returns a response generated by the OpenAI GPT-3 model.

    Parameters:
    event (dict): Event data passed by AWS Lambda.
    context (object): Context data passed by AWS Lambda.

    Returns:
    dict: Status code for the HTTP response.
    """
    try:
        data = json.loads(event["body"])
        message = data["message"]["text"]
        chat_id = data["message"]["chat"]["id"]

        message_history = [
            {"role": "user",
             "content": "Отвечай в стиле четкого пацана с района, который увверен в себе и не боится никого. "
                        "Но он очень добрый и всегда готов поддержать. Еще он обожает поделиться пацанскими историями или мудростями. "
                        "Ответ должен иметь яркий марксисткий или постмодернистский характер. "
                        "Ответ должен быть на языке вопроса. "
                        "Say OK if you understood"},
            {"role": "assistant", "content": "OK"}
        ]

        message_history.append({"role": "user", "content": f"{message}"})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message_history,
        ).choices[0].message.content

        message_history.append({"role": "assistant", "content": f"{response}"})

        print("response is " + response)

        payload = {"text": response, "chat_id": chat_id}
        url = f"{BASE_URL}/sendMessage"
        requests.post(url, json=payload)

    except Exception as e:
        logger.error(e)

    return {"statusCode": 200}