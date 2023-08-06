#!/usr/bin/env bash

gunicorn main:app -b 0.0.0.0:8000  -w 7 -k uvicorn.workers.UvicornH11Worker