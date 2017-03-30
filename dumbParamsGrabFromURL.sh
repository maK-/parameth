#!/bin/sh

curl -s $1 --insecure | grep -e '<input' | grep -e 'name=' | awk -F 'name=' '{print $2}' | awk -F '"' {'print $2'} | sort | uniq
