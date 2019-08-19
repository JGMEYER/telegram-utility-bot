# Telegram-Utility-Bot

```
NOTE: This project is currently in development and incomplete.
```

```
NOTE: This project was developed on MacOS for python 3.6.0. As such, the commands provided in this guide are intended for users on a MacOS installation.
```

## About

Serverless utility bot for Telegram based on this guide:
https://hackernoon.com/serverless-telegram-bot-on-aws-lambda-851204d4236c

## Requirements: Before You Start

This project requires prerequisite tools that are easy to setup. Please read the instructions below closely to avoid issues with your build.

### Docker

```
NOTE: Linux environments should be able to build the project without using Docker.
```

This project compiles its python dependencies on a Docker instance to ensure that all installed dependencies are compatible with amazonlinux. Make sure you have Docker installed and running when iterating on this project. See https://www.docker.com/ for setup instructions.

### Pipenv

Pipenv, though not strictly required, is recommended for managing python versions. You will need to mess around with serverless.yml and your deployment process to build this project with serverless, otherwise.

The README herein assumes you are running python from within the `pipenv shell`. _This will probably bite you at some point, so be sure to run commands from the pipenv shell unless already specified directly._ Make sure you have pipenv installed before modifying this project. For more information on pipenv, check out: https://docs.pipenv.org/en/latest/basics/.

## Env Variables

```
NOTE: See env.yml for the most up-to-date and complete list of required env variables.
```

Example `secrets/env` template:

```
# Credentials for serverless-admin account on AWS
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=

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

# Spotify API
export SPOTIFY_CLIENT_ID=
export SPOTIFY_CLIENT_SECRET=

# Google Cloud APIs
export YOUTUBE_API_KEY=
```

Some of these will be set in the instructions below.

## Setup

### Environment

1. Setup your AWS account (https://aws.amazon.com/)
1. Install and run Docker (https://www.docker.com/)
1. Install pipenv
  - `$ brew install pipenv`
1. Install serverless and dependencies:
  - `$ npm install serverless`
  - `$ npm install serverless-offline serverless@latest`
  - `$ npm install serverless-python-requirements`
1. Add (export) all required env values in `secrets/env`. You may need to create this path.
1. Run `$ source setup` to setup the environment.

### Telegram setup

Set `$TELEGRAM_TOKEN` (from @BotFather) in secrets/env, then source:

```
$ source secrets/*
```

Then run the following to set up the webhook. Be sure to replace "{stage}" (e.g. "DEV", "PROD").
```
$ curl --request POST --url "https://api.telegram.org/bot$TELEGRAM_TOKEN/setWebhook" --header "content-type: application/json" --data "{\"url\":\"$TELEGRAM_API_GATEWAY_ROOT_{stage}\"}"
```

You should see something like:
```
{
  "ok": true,
  "result": true,
  "description": "Webhook was set"
}
```

### Spotify setup

1. Register application on Spotify's website.
1. Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in secrets/env.

### Google Music setup

More instructions at https://unofficial-google-music-api.readthedocs.io

`TODO as of now, it's unclear how I will automate this process on AWS`

1. Run `pipenv run python`.
1. Enter the code below and follow the instructions. This will authorize Google Play Music Manager to manage your account.
  ```
  from gmusicapi import Mobileclient

  mm = Mobileclient()
  mm.perform_oauth()
  ```
1. All future connections to Musicmanager can then be performed with 'login'.
  ```
  from gmusicapi import Mobileclient

  mm = Mobileclient()
  mm.oauth_login(Mobileclient.FROM_MAC_ADDRESS)
  ```

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

Serverless will package all files into .zip archive and uploads to AWS. It will then create an AWS API Gateway and return an API endpoint. You will receive something like this:

```
endpoints:

POST - https://u3ir5tjcsf.execute-api.us-east-1.amazonaws.com/dev/telegram/endpoint1
POST - https://u3ir5tjcsf.execute-api.us-east-1.amazonaws.com/dev/telegram/endpoint2
```

Use this and update `$TELEGRAM_API_GATEWAY_ROOT_{stage}` for {stage} in secrets/env to "<url\>/{stage}/telegram", e.g.

```
export TELEGRAM_API_GATEWAY_ROOT_DEV="https://u3ir5tjcsf.execute-api.us-east-1.amazonaws.com/dev/telegram"
```

## Adding a New Endpoint

If you want to extend the functionality of the bot with your own requests/commands, it is recommend you move it to a new endpoint.

1. Add endpoint to serverless.yml.

  `IMPORTANT! The root of the endpoint is important. For example, telegram endpoints MUST begin with "telegram/" to be recognized by the Telegram bot webhook.`

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
  You can easily mock out an endpoint while it's being developed with:
  ```
  elif event['path'] == "/telegram/myEndpoint":
      return {"statusCode": 400}  # not yet available
  ```

## Local Testing

### Offline

Install serverless-offline:

```
$ npm install serverless-offline serverless@latest
```

Run serverless:

```
$ pipenv run sls offline
```

Send requests in a new terminal tab like:

```
$ curl --header "Accept: application/json" --header "Content-Type: application/json" --request POST --data '{"alerter": "user"}' localhost:3000/telegram/alert
```

### Unit/integration testing

I've included unit and integration tests in the `if __name__ == '__main__'` clause of tested classes. This was just a stopgap to test the code while iterating quickly. It's as easy as:

```
$ pipenv run python {file}.py
```

## Test Commands

### Telegram bot alert
```
$ curl --header "Content-Type: application/json" --request POST --data '{"alerter": "user"}' $TELEGRAM_API_GATEWAY_ROOT_LOCAL/alert
```

## Better Logging and Maintenance

Give this a shot? Should include local testing, monitoring, and logs.

https://serverless.com/blog/serverless-monitoring-the-good-the-bad-and-the-ugly/
