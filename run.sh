#!/bin/bash
echo Please enter the IP of the victim
read target_ip
echo Please enter the IP of the gateway
read gateway_ip
echo 'Please enter your own IP (optional, will be calculated if empty)'
read local_ip
echo 'Please enter the interface (optional, default is enp0s3)'
read interface
echo $target_ip $gateway_ip $local_ip $interface
