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

SETTINGS="set net:timeout 2; set net:max-retries 2; set net:reconnect-interval-base 2; set ftp:ssl-force yes; set ftp:ssl-protect-data true; set sftp:auto-confirm yes; set ssl:verify-certificate no;"
# Use lftp to synchronize the folders
# https://stackoverflow.com/questions/49843692/continuous-deployment-using-lftp-gets-stuck-temporarily-after-about-10-files
# https://forum.gitlab.com/t/deploy-with-lftp-uploads-all-files-even-unchanged-ones/35439
output=$(lftp -p 22 -e "$SETTINGS; ls; mirror --delete -P 5 -R --verbose \"$local_folder\" \"$remote_folder\"; quit" -u "$remote_user","$remote_password" sftp://$remote_host 2>&1)
exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "Synchronization successful."
else
    echo "Synchronization attempt $i failed. Error message: $output"
fi
echo $output