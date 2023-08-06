#!/usr/bin/env bash

gunicorn app:app -b 0.0.0.0:8000  -w 7 -k uvicorn.workers.UvicornH11Worker