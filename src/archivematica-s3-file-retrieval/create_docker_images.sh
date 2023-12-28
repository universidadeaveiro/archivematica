#!/bin/bash

declare -A FILES=( ["file-retrieval-api"]="./api" ["polling"]="./polling" ["mail-notification-api"]="./mail_notification_api")

for f in "${!FILES[@]}"
do
	echo "Removing previous version of image $f..."
    docker image rm --force IMAGE $f
    echo -e "Previous version removed!\n"

    echo "Creating new image $f..."
    cd ${FILES[$f]} ; docker build --tag $f . ; cd ..
    echo -e "Image created!\n"
done