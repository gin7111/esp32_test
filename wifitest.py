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
import utime
import socket

# wlan = network.WLAN(network.STA_IF)
# wlan.active(True)
# wlan.connect('YCKZ', 'qmhdwifi')

# wlan.isconnected()

def espwifi():
    apessid = 'ESPap'
    appassword = 'espdwifi'
    #默认ip = ('192.168.4.1', '255.255.255.0', '192.168.4.1', '0.0.0.0')
    
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=apessid,password=appassword)
    ap.active(True)
    #ap.ifconfig(('192.168.4.1','255.255.255.0','192.168.4.1','0.0.0.0'))
    print('热点已开启，', apessid, '：', appassword)
    print('本机ip地址：', ap.ifconfig())
    return ap

def start_udp():
    udp_port = 7788
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('0.0.0.0', udp_port))
    print('UDP已建立，端口：', udp_port)
    return udp_socket


def main():
    ap = espwifi()
    #apip = ap.ifconfig()[0]
    utime.sleep(1)
    udp_socket = start_udp()#要使用变量赋值函数的方法调用函数返回的信息
    #while ap.isconnected() == False:
        #udp_socket.sendto(apip.encode("utf-8"), ('255.255.255.255', 9999))

    done = False

    while done == False:
        recv_data, sender_info = udp_socket.recvfrom(1024)
        recv_data_str = recv_data.decode('utf-8')
        print(sender_info, '发送：', recv_data_str)


if __name__ == '__main__':
    main()
