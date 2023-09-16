#!/bin/bash

if [ "$#" -ne 5 ]; then
    echo "Usage: $0 <local_folder> <remote_user> <remote_password> <remote_host> <remote_folder>"
    exit 1
fi

local_folder="$1"
remote_user="$2"
remote_password="$3"
remote_host="$4"
remote_folder="$5"

# Use lftp to synchronize the folders
lftp -e "mirror -R --delete --verbose \"$local_folder\" \"$remote_folder\"; quit" -u "$remote_user","$remote_password" sftp://$remote_host
