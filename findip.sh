#!/bin/bash
echo "My ifconfig info is:" > interface.txt
ifconfig >> interface.txt
echo "Curl found this external IP:" >> interface.txt
curl ifconfig.me
