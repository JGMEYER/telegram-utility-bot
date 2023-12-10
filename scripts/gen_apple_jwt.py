#!/usr/bin/env python

import argparse
import jwt
import time

parser = argparse.ArgumentParser(
    description="Generate Developer JSON Web Token (JWT) for Apple Music"
)
parser.add_argument("key_id", help="developer key id (kid)")
parser.add_argument("team_id", help="apple developer team id")
parser.add_argument(
    "path_to_authkey",
    help="path to AuthKey file, ending in .p8, e.g. `./secrets/AuthKey_abc123.p8`",
)
args = parser.parse_args()

issued_timestamp = int(time.time())
expiration_timestamp = issued_timestamp + 15777000  # 6 months

payload = {
    "iss": args.team_id,
    "iat": issued_timestamp,
    "exp": expiration_timestamp,
}
with open(args.path_to_authkey) as f:
    private_key = f.read()
headers = {"kid": args.key_id}
encoded = jwt.encode(payload, private_key, algorithm="ES256", headers=headers)

print(f"\n{encoded}")
