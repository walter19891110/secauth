#!/bin/sh

PIDS=$(ps ax | grep -i 'secauth' | grep -v grep | awk '{print $1}')
if [ -z "$PIDS" ]; then
  echo "No secauth to stop"
else
  kill -9 $PIDS
  echo "secauth stoped"
fi

PIDS=$(ps ax | grep -i 'SMServer' | grep java | grep -v grep | awk '{print $1}')
if [ -z "$PIDS" ]; then
  echo "No SMServer to stop"
else
  kill -9 $PIDS
  echo "SMServer stoped"
fi
