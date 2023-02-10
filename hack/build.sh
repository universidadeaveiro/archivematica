#!/bin/bash
# @Author: Eduardo Santos
# @Date:   2022-03-28 19:37:55
# @Last Modified by:   Eduardo Santos
# @Last Modified time: 2023-02-10 11:22:56

while getopts 'as:' OPTION; do
  case "$OPTION" in
    a)
        printf "Building all images...\n"

        for folder in ./dockerfiles/*; do
          printf "Running build.sh on $folder...\n\n"
          
          cd "$folder" && chmod +x build.sh && ./build.sh
          PREVIOUS_COMMAND_STATUS="$?"

          if [ "$PREVIOUS_COMMAND_STATUS" == "1" ]; then
            printf "\nAn error occurred. Exiting..."
            exit 1
          else
            printf "\nDone!"
          fi
          
            cd ../..
        done
        ;;
    s)
        svalue="$OPTARG"
        printf "The service provided is: $svalue\n"
        
        printf "\nRunning build.sh...\n\n"
        cd "./dockerfiles/$svalue" && chmod +x build.sh && ./build.sh

        PREVIOUS_COMMAND_STATUS="$?"

        if [ "$PREVIOUS_COMMAND_STATUS" == "1" ]; then
          printf "\nAn error occurred. Exiting..."
          exit 1
        else
          printf "\nDone!"
          exit 0
        fi

        ;;
    ?)
        printf "script usage: $(basename \$0) [-l] [-h] [-a somevalue]" >&2
        exit 1
        ;;
  esac
done
shift "$(($OPTIND -1))"