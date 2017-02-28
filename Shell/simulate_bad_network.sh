#!/bin/bash

# http://www.howtogeek.com/177621/the-beginners-guide-to-iptabels-the-linux-firewall/

sleep 20
while true
do
iptables -A INPUT -s 10.0.0.134 -p tcp --dport 1666 -j DROP
iptables -L
sleep 320
iptables -F
iptables -L
sleep 320
done
