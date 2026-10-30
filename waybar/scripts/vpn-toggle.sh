#!/bin/bash

VPN="VPN-W"

if nmcli -t -f NAME connection show --active | grep -Fxq "$VPN"; then
    nmcli connection down "$VPN"
else
    nmcli connection up "$VPN"
fi
