# Telegram-Utility-Bot

> NOTE: This project was developed on MacOS for python 3.6.0. As such, the
commands provided in this guide are intended for users on a MacOS installation.

## About

Serverless utility bot for Telegram originally based on [this guide](https://hackernoon.com/serverless-telegram-bot-on-aws-lambda-851204d4236c).

## Pricing

> NOTE: Prices may change based on AWS's pricing model. Values below are estimates.

While the code is free to use, there is a small cost to host the bot on AWS.

* $9/yr Route 53 Registered Domain
* $0.50/mo Route 53 Hosted Zone

Total: $15/yr

## Requirements: Before You Start

This project requires prerequisite tools that are easy to setup. Please read the instructions below closely to avoid issues with your build.

### Docker

> NOTE: Linux environments should be able to build the project without using
Docker.

This project compiles its python dependencies on a Docker instance to ensure that all installed dependencies are compatible with amazonlinux. Make sure you have Docker installed and running when iterating on this project. See [Docker's website](https://www.docker.com/) for setup instructions.

### Pipenv

Pipenv, though not strictly required, is recommended for managing python versions. You will need to mess around with serverless.yml and your deployment process to build this project with serverless, otherwise.

The README herein assumes you are running python from within the `pipenv shell`. _This will probably bite you at some point, so be sure to run commands from the pipenv shell unless already specified directly._ Make sure you have pipenv installed before modifying this project. For more information on pipenv, check out [the basics](https://docs.pipenv.org/en/latest/basics/).

## Env Variables

> NOTE: See env.yml for the most up-to-date and complete list of required env
variables.

Example `secrets/env` template:

```bash
# Credentials for serverless-admin account on AWS
export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=

# Domains
export BOT_DOMAIN_DEV=
export BOT_DOMAIN_PROD=

# Telegram API
export TELEGRAM_CHAT_ID_DEV=
export TELEGRAM_CHAT_ID_PROD=
export TELEGRAM_TOKEN_DEV=
export TELEGRAM_TOKEN_PROD=

# logging (recommend same credentials as DEV chat if no other group setup)
export TELEGRAM_LOG_CHAT_ID_DEV=
export TELEGRAM_LOG_TOKEN=

# specific to telegram functionality
# format like JSON e.g. ='["user1", "user2", "user3"]'
export TELEGRAM_ALERT_GROUP=

# helpers for testing calls locally
export TELEGRAM_API_GATEWAY_ROOT_LOCAL="localhost:3000"
export TELEGRAM_API_GATEWAY_ROOT_DEV="https://$BOT_DOMAIN_DEV"
export TELEGRAM_API_GATEWAY_ROOT_PROD="https://$BOT_DOMAIN_PROD"

# Spotify API
export SPOTIFY_CLIENT_ID=
export SPOTIFY_CLIENT_SECRET=

# Google Cloud APIs
export YOUTUBE_API_KEY=
```

`env.yml` and `serverless.yml` help serverless resolve which environment variables to use.

## Setup

> NOTE: Some steps may be out of order, incomplete, or missing. Please open an
issue on GitHub for clarification questions or open a PR if you have a fix.

Follow the steps below to setup your environment. Check out each tool's corresponding sections for additional instructions

1. Create a new path/file "./secrets/env"
1. Setup your [AWS account](https://aws.amazon.com/)
1. Install and run [Docker](https://www.docker.com/)
1. Install pipenv: `brew install pipenv`
1. Install pre-commit hooks: `pipenv run pre-commit install`
1. Setup serverless
1. Setup the environment: `. setup`

### AWS Setup

This tool uses Telegram's webhooks to send push notifications to the bot on channel updates. In order for Telegram to securely communicate channel information to your bot, you'll need to register a domain with appropriate certificates.

Use [this guide](https://serverless.com/blog/serverless-api-gateway-domain) to register a domain and set up your certificates. Register two separate certificates for `prod.{yourdomain}` and `dev.{yourdomain}`.

It will take some time for your certificate to go from "pending" to "issued".

Once you have the domain registered, update all `$BOT_DOMAIN_{stage}` in secrets/env.

### Serverless setup

> NOTE: You can view the domain configurations in serverless.yml:custom:customDomain

1. `$ npm install` - install this serverless package and its dependencies
1. `$ sls create_domain` - create a custom dev domain
1. `$ sls create_domain --s prod` - create a custom prod domain
1. Once the domains are reachable in your browser, deploy dev and prod with `$ sls deploy && sls deploy --s prod`

### Telegram setup

Create two bots by messaging @BotFather in Telegram: one for DEV, one for PROD. I recommend you create a test group for the DEV bot to avoid annoying your friends. You can configure different `$TELEGRAM_CHAT_ID_{stage}` in secrets/env.

**Important!** Next, turn off privacy mode for these bots via @BotFather to allow them to send message data via the Telegram webhooks.

Set the tokens you get from @BotFather to `$TELEGRAM_TOKEN_{stage}` in secrets/env, then source:

```bash
. secrets/env
```

Then run the following to set up the webhook. Run this for each stage (e.g. "DEV", "PROD").

```bash
curl --request POST --url "https://api.telegram.org/bot$TELEGRAM_TOKEN_{stage}/setWebhook" --header "content-type: application/json" --data "{\"url\":\"$TELEGRAM_API_GATEWAY_ROOT_{stage}/webhookUpdate\"}"
```

You should see something like:

```json
{
  "ok": true,
  "result": true,
  "description": "Webhook was set"
}
```

If you ever want to remove the webhook, e.g. to test getUpdates GET requests on dev, you can send a POST request to `deleteWebhook`. Just remember to reconfigure the webhook once you're done.

For other assistance, check out the [Telegram documentation](https://core.telegram.org/bots/webhooks) for everything webhook.

### Spotify setup

1. Register application on Spotify's website.
1. Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in secrets/env.

### Google Music setup

1. Run `pipenv run python`.

1. Enter the code below and follow the instructions. This will authorize Google Play Music Manager to manage your account.

```python
import os
from gmusicapi import Mobileclient

mm = Mobileclient()
mm.perform_oauth(storage_filepath=os.path.join(os.getcwd(), 'secrets/gmusicapi.cred'), open_browser=True)
```

This file will be pushed as part of the zip archive to S3, which will allow AWS to interact with the api.

For more information on the API, check out [the docs](https://unofficial-google-music-api.readthedocs.io).

## Deploy to AWS

Dev:

```bash
. setup
sls deploy
```

Prod:

```bash
. setup
sls deploy --s prod
```

Serverless will package all files into .zip archive and uploads to AWS. It will then create an AWS API Gateway and return an API endpoint. You will receive something like this:

```bash
$ sls deploy

...

endpoints:

POST - https://u3ir5tjcsf.execute-api.us-east-1.amazonaws.com/dev/endpoint1
POST - https://u3ir5tjcsf.execute-api.us-east-1.amazonaws.com/dev/endpoint2
```

Use this and update `$TELEGRAM_API_GATEWAY_ROOT_{stage}` for {stage} in secrets/env to "<url\>/{stage}/telegram", e.g.

```bash
export TELEGRAM_API_GATEWAY_ROOT_DEV="https://u3ir5tjcsf.execute-api.us-east-1.amazonaws.com/dev/telegram"
```

## Adding a New Endpoint

If you want to extend the functionality of the bot with your own requests/commands, you need to create a new endpoint.

1. Add endpoint to serverless.yml.

```yaml
functions:
  post:
    handler: handler.handler
    events:
    - http:
        path: myEndpoint
        method: post
        cors: true
```

1. Create a function in handler.py that will process incoming requests:

```python
def my_endpoint_logic(event, context):
    ...
```

  This function must return a dict like `{"statusCode": <http_status_code>}`.

1. Add a clause in handler() in handler.py to execute your function when the endpoint is invoked.

```python
elif event['path'] == "/myEndpoint":
    return my_endpoint_logic(event, context)
```

  You can easily mock out an endpoint while it's being developed with:

```python
elif event['path'] == "/myEndpoint":
    return {"statusCode": 400}  # not yet available
```

### Adding new webhookUpdate parser

All webhook updates currently go to the `webhookUpdate/` endpoint. Update `handle_webhook_update()` in handler.py with your new message-parsing logic. Make sure you consider how this will interact with other tools that are looking to parse messages.

## Tailing Logs

You can tail cloudwatch logs on dev and prod using a variation of the command below:

```bash
sls logs -f post -t
```

## Local Testing

### Offline

Install serverless-offline:

```bash
npm install serverless-offline serverless@latest
```

Run serverless:

```bash
pipenv run sls offline
```

Send requests in a new terminal tab like:

```bash
curl --header "Accept: application/json" --header "Content-Type: application/json" --request POST --data '{"alerter": "user"}' localhost:3000/alert
```

### Unit tests

```bash
pipenv run pytest -m 'not integ' -rf
```

### Integration tests

```bash
. setup
pipenv run pytest -m 'integ' -rf --log-level=WARNING
```

### All unit/integration tests

```bash
. setup
pipenv run pytest -rf
```

## Test Commands

### Telegram bot alert

```bash
curl --header "Content-Type: application/json" --request POST --data '{"alerter": "user"}' $TELEGRAM_API_GATEWAY_ROOT_LOCAL/alert
```

### Music link

```bash
curl --tlsv1.2 -v -k -H "Content-Type: application/json" -H "Cache-Control: no-cache"  -d '{"update_id":10000, "message":{ "date":99999999999, "chat":{ "last_name":"Test Lastname", "id":1111111, "first_name":"Test", "username":"Test" }, "message_id":1365, "from":{ "last_name":"Test Lastname", "id":1111111, "first_name":"Test", "username":"Test" }, "text":"https://open.spotify.com/track/43ddJFnP8m3PzNJXiHuiyJ?si=T3ZApBErTF-M1esGJoRMmw" } }' $TELEGRAM_API_GATEWAY_ROOT_LOCAL/webhookUpdate
```

## Better Logging and Maintenance

Give [this](https://serverless.com/blog/serverless-monitoring-the-good-the-bad-and-the-ugly/) a shot? Should include local testing, monitoring, and logs.
