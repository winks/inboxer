#!/usr/bin/env bash

DIR=$(dirname $(readlink -f $0))
PY3="/home/USER/.virtualenvs/inboxer/bin/python3"

export USERNAME="inboxer@example.org"
export PASSWORD="example"
export HOSTNAME="mail.example.org"
export DIRECTORY="/home/USER/public_html"
export TARGET="DONE"
export FROM_EMAIL=$USERNAME
export BASE_URL="https://example.org/~USER/"

echo $DIR
$PY3 "${DIR}/inboxer.py"
