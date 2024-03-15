#!/bin/bash

cd src
celery -A tasks worker --loglevel=info
