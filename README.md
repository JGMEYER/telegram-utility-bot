# README

Serverless bot based on this guide:
https://hackernoon.com/serverless-telegram-bot-on-aws-lambda-851204d4236c

## Setup

This should configure the environment:

```
./setup.sh
```

Afterwards, it may display additional steps to run. Execute them, then proceed.

## Deploy to AWS

```
serverless deploy
```

Packages all files into .zip archive and uploads to AWS. It will then create an AWS API Gateway and return an API endpoint. You will receive something like this:

```
endpoints:

POST - https://u3ir5tjcsf.execute-api.us-east-1.amazonaws.com/dev/my-custom-url
```

## Connect backend to Telegram Bot

Set `$TELEGRAM_TOKEN` (from @BotFather) and `$TELEGRAM_API_GATEWAY_ENDPOINT` (from last step) in api_keys_DO_NOT_RENAME, then source:

```
source api_keys_DO_NOT_RENAME
```

Then run the following to set up the webhook.

```
curl --request POST --url "https://api.telegram.org/bot$TELEGRAM_TOKEN/setWebhook" --header "content-type: application/json" --data "{\"url\":\"$TELEGRAM_API_GATEWAY_ENDPOINT\"}"
```

You should see something like:

```
{
  "ok": true,
  "result": true,
  "description": "Webhook was set"
}
```
