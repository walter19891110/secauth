#!/bin/sh

cd $HOME/secauth
java -jar SMServer.jar&
python37 src/secauth.py&
