#!/usr/bin/expect

# Set the environment variable containing the password
set password $env(FTP_PASSWORD)
set server $env(SERVER)
set user $env(FTP_USER)



# Execute the SCP command with password handling
spawn  bash -c "scp -r site/* '$user'@$server:"
expect ".*password:"
send "$password\r"
expect eof