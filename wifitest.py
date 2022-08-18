## 官方示例
# import network

# wlan = network.WLAN(network.STA_IF) # create station interface
# wlan.active(True)       # activate the interface
# wlan.scan()             # scan for access points
# wlan.isconnected()      # check if the station is connected to an AP
# wlan.connect('essid', 'password') # connect to an AP
# wlan.config('mac')      # get the interface's MAC address
# wlan.ifconfig()         # get the interface's IP/netmask/gw/DNS addresses

import network
import time

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('YCKZ', 'qmhdwifi')

wlan.isconnected()
