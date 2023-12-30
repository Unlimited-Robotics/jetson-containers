#!/bin/bash

rsync \
    --checksum \
    --archive \
    --verbose \
    --delete \
    --exclude '.git/' \
    --exclude '.github/' \
    --exclude '.vscode/' \
    --exclude '.idea/' \
    --exclude '.gitignore/' \
    --exclude '__pycache__' \
    --exclude '.gitignore' \
    --exclude 'data/' \
    --exclude 'logs/' \
    $PWD $1:/home/gary/ur_dev/
