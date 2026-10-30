#!/bin/bash

VPN="VPN-W"

if nmcli -t -f NAME connection show --active | grep -Fxq "$VPN"; then
#    echo "󰒃 VPN"
    echo '{"text":"󰒃 VPN", "class":"connected"}'
else
#    echo "󰒄"
    echo '{"text":"󰒄 VPN", "class":"disconnected"}'
fi
