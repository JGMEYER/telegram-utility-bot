# README

Serverless bot based on this guide:
https://hackernoon.com/serverless-telegram-bot-on-aws-lambda-851204d4236c

## Required env values

```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
TELEGRAM_API_GATEWAY_ROOT
TELEGRAM_TOKEN
YOUTUBE_API_KEY
```

Some of these will be set in the instructions below.

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

POST - https://u3ir5tjcsf.execute-api.us-east-1.amazonaws.com/dev/telegram/endpoint1
POST - https://u3ir5tjcsf.execute-api.us-east-1.amazonaws.com/dev/telegram/endpoint2
```

Use this and update `$TELEGRAM_API_GATEWAY_ROOT` in secrets/api_keys to "<url\>/dev/telegram", e.g. "https://u3ir5tjcsf.execute-api.us-east-1.amazonaws.com/dev/telegram"

## Connect backend to Telegram Bot

Set `$TELEGRAM_TOKEN` (from @BotFather) in secrets/api_keys, then source:

```
$ source secrets/api_keys
```

Then run the following to set up the webhook.

```
$ curl --request POST --url "https://api.telegram.org/bot$TELEGRAM_TOKEN/setWebhook" --header "content-type: application/json" --data "{\"url\":\"$TELEGRAM_API_GATEWAY_ROOT\"}"
```

You should see something like:

```
{
  "ok": true,
  "result": true,
  "description": "Webhook was set"
}
```

## Adding a new endpoint

1. Add endpoint to serverless.yml.

  `IMPORTANT! The root of the endpoint is important. For example, telegram endpoints MUST begin with telegram/* to be recognized by the Telegram bot webhook.`

  ```
  functions:
    post:
      handler: handler.handler
      events:
      - http:
          path: telegram/myEndpoint
          method: post
          cors: true
  ```
1. Create a function in handler.py that will process incoming requests:
  ```
  def my_endpoint_logic(event, context):
      ...
  ```

  This function must return a dict like `{"statusCode": <http_status_code>}`.
1. Add a clause in handler() in handler.py to execute your function when the endpoint is invoked.
  ```
  elif event['path'] == "/telegram/myEndpoint":
      return my_endpoint_logic(event, context)
  ```
  You can easily mock out an endpoint like while it's being developed with:
  ```
  elif event['path'] == "/telegram/myEndpoint":
      return {"statusCode": 400}  # not yet available
  ```

## Local testing

I *think* you can test something along the lines of:

```
$ serverless invoke local --function post
```

## Test commands

### Telegram Bot Alert
```
$ curl --header "Content-Type: application/json" --request POST --data '{"alerter": "Knallharter"}' $TELEGRAM_API_GATEWAY_ROOT/alert
```

## Better Logging and Maintenance

Give this a shot? Should include local testing, monitoring, and logs.

https://serverless.com/blog/serverless-monitoring-the-good-the-bad-and-the-ugly/
