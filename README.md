# ChatGPT Telegram Bot
This is a Telegram bot that uses OpenAI's ChatGPT model to respond to messages. It is hosted on AWS and uses the free tier of all services.

# Running Your Own Version
To run your own version of this bot, you will need the following:

- Node.js and Serverless framework
- An AWS account
- Set your AWS access key ID and secret access key as environment variables:
  ```
  export AWS_ACCESS_KEY_ID=<YOUR_AWS_ACCESS_KEY_ID>
  export AWS_SECRET_ACCESS_KEY=<YOUR_AWS_SECRET_ACCESS_KEY>
  ```
- A Telegram bot created with Bot Father
- Set your Telegram bot token as an environment variable:
  ```
  export TELEGRAM_TOKEN=<YOUR_TELEGRAM_BOT_TOKEN>
  ```
To install dependencies and deploy the bot:

1. Install dependencies locally:
   ```
   pip install -r requirements.txt -t vendored
   ```
2. Deploy the bot:
   ```
   serverless deploy
   ```
3. Set the new endpoint as the webhook for your bot:
   ```
   https://api.telegram.org/bot<TOKEN>/setWebHook?url=<AWS_URL>