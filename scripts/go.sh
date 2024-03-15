#!/bin/bash

target=/root/fastapi_app

mkdir ${target} ${target}/nginx
git clone https://github.com/zion4dd/fastapi ${target}/app
cp ${target}/app/nginx.conf ${target}/nginx/
nano ${target}/app/.env
cd ${target}/app

echo "Fastapi app dir: ${target}/app"

read -p "run 'docker compose build' ? (y/n)" answer
if [ "$answer" == "y" ]; then
docker compose build
fi

read -p "run 'docker compose up -d' ? (y/n)" answer2
if [ "$answer2" == "y" ]; then
docker compose up -d
fi
