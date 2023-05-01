#!/bin/bash

# Load environment variables from file
source conf/dev/.env


PID=$(ps aux | grep 'uvicorn app:app' | grep -v grep | awk {'print $2'} | xargs)
if [ "$PID" != "" ]
then
sudo kill -9 $PID
fi



# Start your FastAPI application
uvicorn app:app --host=$HOST --port=$PORT
