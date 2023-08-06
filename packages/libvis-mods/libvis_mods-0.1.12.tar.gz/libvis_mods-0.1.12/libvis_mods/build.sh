#!/bin/bash

: ${1?"Usage: $0 SOURCES_PATH"}

cd $1

if yarn -v; then
    echo "I [libvis-mods] build: Using yarn version: $(yarn -v)"
    yarn && yarn build
elif npm -v; then
    echo "I [libvis-mods] build: Using npm version: $(npm -v)"
    npm i && npm run build
else
    >&2 echo "E [libvis-mods] build: You don't have neither yarn nor npm installed."
fi

