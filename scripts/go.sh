#!/bin/bash

target=/root/fastapi

mkdir ${target}
git clone https://github.com/zion4dd/fastapi ${target}

nano ${target}/.env
cd ${target}/
echo "Fastapi app dir: ${target}"

read -p "run 'docker compose build' ? (y/n)" answer
if [ "$answer" == "y" ]; then
docker compose build
fi

read -p "run 'docker compose up -d' ? (y/n)" answer2
if [ "$answer2" == "y" ]; then
docker compose up -d
fi
