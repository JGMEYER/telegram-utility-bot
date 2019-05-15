# README

Serverless bot based on this guide:
https://hackernoon.com/serverless-telegram-bot-on-aws-lambda-851204d4236c

## Required env values

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
TELEGRAM_TOKEN
TELEGRAM_API_GATEWAY_ENDPOINT
YOUTUBE_API_KEY
```

## Setup

1. Add (export) all required env values in `secrets/api_keys`. You may need to create this path.
1. Run `$ source setup` to setup the environment.

## Deploy to AWS

```
$ serverless deploy
```

Packages all files into .zip archive and uploads to AWS. It will then create an AWS API Gateway and return an API endpoint. You will receive something like this:

```
endpoints:

POST - https://u3ir5tjcsf.execute-api.us-east-1.amazonaws.com/dev/my-custom-url
```

## Connect backend to Telegram Bot

Set `$TELEGRAM_TOKEN` (from @BotFather) and `$TELEGRAM_API_GATEWAY_ENDPOINT` (from last step) in secrets/api_keys, then source:

```
$ source secrets/api_keys
```

Then run the following to set up the webhook.

```
$ curl --request POST --url "https://api.telegram.org/bot$TELEGRAM_TOKEN/setWebhook" --header "content-type: application/json" --data "{\"url\":\"$TELEGRAM_API_GATEWAY_ENDPOINT\"}"
```

You should see something like:

```
{
  "ok": true,
  "result": true,
  "description": "Webhook was set"
}
```

## Local testing

I *think* you can test something along the lines of:

```
$ serverless invoke local --function post
```

## Test commands

### Bopiz ENS Bot Alert
```
$ curl --header "Content-Type: application/json" --request POST --data '{"alerter": "Knallharter"}' https://7jqeooocuk.execute-api.us-east-1.amazonaws.com/dev/alert
```

## Better Logging and Maintenance

Give this a shot? Should include local testing, monitoring, and logs.

https://serverless.com/blog/serverless-monitoring-the-good-the-bad-and-the-ugly/
