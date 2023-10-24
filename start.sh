#!/bin/bash

echo "========== SERVER DOWN =========="
ps -ef | grep manage.py | awk '{print $2}' | xargs kill -9

echo "========== DELETE nohup log =========="
rm nohup.out

echo "========== SERVER UP =========="
nohup python3 manage.py runserver 0.0.0.0:20009 &
