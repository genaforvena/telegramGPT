import json
import os
import sys
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))

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

        response = openai.Completion.create(
            engine="babbage",
            prompt=message,
            max_tokens=2048,
            n=1,
            temperature=0.5,
        ).choices[0].text

        payload = {"text": response, "chat_id": chat_id}
        url = f"{BASE_URL}/sendMessage"
        requests.post(url, json=payload)

    except Exception as e:
        logger.error(e)

    return {"statusCode": 200}