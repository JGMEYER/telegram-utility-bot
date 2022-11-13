#!/bin/bash
# Generates JSON Web Token (JWT) for Apple Music
# usage: PRIVATE_KEY=<private_key> ./scripts/genapplejwt.sh <kid> <team_id>

main(){
  set -eo pipefail

  [ -n "$PRIVATE_KEY" ] || die "PRIVATE_KEY environment variable is not set."
  [ -z "$1" ] && die "missing kid"
  [ -z "$2" ] && die "missing team_id"

  kid="$1"
  team_id="$2"

  # number of seconds to expire token
  expire_seconds=15777000  # 6 months

  header="{
    \"alg\": \"ES256\",
    \"kid\": $kid,
  	\"typ\": \"JWT\"
  }"

  payload="{
    \"iss\": $team_id,
    \"iat\": $(date +%s),
    \"exp\": $(($(date +%s)+expire_seconds))
  }"

  echo $header
  echo $payload

  header_base64=$(printf %s "$header" | base64_urlencode)
  payload_base64=$(printf %s "$payload" | base64_urlencode)
  signed_content="${header_base64}.${payload_base64}"
  echo $signed_content
  signature=$(printf %s "$signed_content" | openssl dgst -binary -sha256 -hmac "$PRIVATE_KEY" | base64_urlencode)

  log "generated JWT token. expires in $expire_seconds seconds -->\\n"
  printf '%s' "${signed_content}.${signature}"
}

base64_urlencode() { base64 | sed s/\+/-/ | sed -E s/=+$//; }
readonly __entry=$(basename "$0")
log(){ echo -e "$__entry: $*" >&2; }
die(){ log "$*"; exit 1; }
main "$@"
