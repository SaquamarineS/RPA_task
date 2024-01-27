#!/bin/bash

IMAGE_NAME="rpa_task_image"

docker build -t $IMAGE_NAME .

EXAMPLE_FILE="example.csv"

docker run -v $EXAMPLE_FILE:/app/example.csv $IMAGE_NAME
