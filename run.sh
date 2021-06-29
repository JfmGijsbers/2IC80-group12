#!/bin/bash
echo Please enter the IP of the victim
read target_ip
echo Please enter the IP of the gateway
read gateway_ip
echo 'Please enter your own IP (optional, will be calculated if empty)'
read local_ip
echo 'Please enter the interface (optional, default is enp0s3)'
read interface
echo $local_ip
if ( "$local_ip"); then
  echo "$local_ip"
else
  echo "Local IP not set"
fi