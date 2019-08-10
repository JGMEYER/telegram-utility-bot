# README

Serverless bot based on this guide:
https://hackernoon.com/serverless-telegram-bot-on-aws-lambda-851204d4236c

## Required env variables

See env.yml for the most up-to-date and complete list of required env variables.

Example `secrets/env` template:

```
# Credentials for serverless-admin account on AWS
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=

# Spotify API
export SPOTIFY_CLIENT_ID=
export SPOTIFY_CLIENT_SECRET=

# Telegram API
export TELEGRAM_CHAT_ID_DEV=
export TELEGRAM_CHAT_ID_PROD=
export TELEGRAM_TOKEN_DEV=
export TELEGRAM_TOKEN_PROD=

# specific to telegram functionality
# format like JSON e.g. ='["user1", "user2", "user3"]'
export TELEGRAM_ALERT_GROUP=

# helpers for testing calls locally (optional)
export TELEGRAM_API_GATEWAY_ROOT_LOCAL=
export TELEGRAM_API_GATEWAY_ROOT_DEV=
export TELEGRAM_API_GATEWAY_ROOT_PROD=

# Google Cloud APIs
export YOUTUBE_API_KEY=
```

Some of these will be set in the instructions below.

## Setup

1. Install serverless: `$ npm install serverless`
1. Install serverless-offline: `$ npm install serverless-offline serverless@latest`
1. Add (export) all required env values in `secrets/env`. You may need to create this path.
1. Run `$ source setup` to setup the environment.

## Deploy to AWS

Dev:
```
$ source setup
$ sls deploy
```

Prod:
```
$ source setup
$ sls deploy --s prod
```

Packages all files into .zip archive and uploads to AWS. It will then create an AWS API Gateway and return an API endpoint. You will receive something like this:

```
endpoints:

POST - https://u3ir5tjcsf.execute-api.us-east-1.amazonaws.com/dev/telegram/endpoint1
POST - https://u3ir5tjcsf.execute-api.us-east-1.amazonaws.com/dev/telegram/endpoint2
```

Use this and update `$TELEGRAM_API_GATEWAY_ROOT_{stage}` for {stage} in secrets/env to "<url\>/{stage}/telegram", e.g.

```
export TELEGRAM_API_GATEWAY_ROOT_DEV="https://u3ir5tjcsf.execute-api.us-east-1.amazonaws.com/dev/telegram"
```

## Connect backend to Telegram Bot

Set `$TELEGRAM_TOKEN` (from @BotFather) in secrets/env, then source:

```
$ source secrets/*
```

Then run the following to set up the webhook.

```
$ curl --request POST --url "https://api.telegram.org/bot$TELEGRAM_TOKEN/setWebhook" --header "content-type: application/json" --data "{\"url\":\"$TELEGRAM_API_GATEWAY_ROOT_DEV\"}"
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

Install serverless-offline:

```
$ npm install serverless-offline serverless@latest
```

Run serverless:

```
$ sls offline
```

Send requests in a new terminal tab like:

```
$ curl --header "Accept: application/json" --header "Content-Type: application/json" --request POST --data '{"alerter": "user"}' localhost:3000/telegram/alert
```

## Test commands

### Telegram Bot Alert
```
$ curl --header "Content-Type: application/json" --request POST --data '{"alerter": "user"}' $TELEGRAM_API_GATEWAY_ROOT_LOCAL/alert
```

## Better Logging and Maintenance

Give this a shot? Should include local testing, monitoring, and logs.

https://serverless.com/blog/serverless-monitoring-the-good-the-bad-and-the-ugly/
