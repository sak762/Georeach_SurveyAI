#!/bin/bash
sudo docker image prune -f
sudo docker build -t surveyai .
sudo docker-compose up -ds