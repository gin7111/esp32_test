#esp32连接wifi，获得ip地址
#创建UDP socket
#接收UDP数据
#根据收到的数据控制led亮灭
#在VScode中用RT-Thread Micropython插件时会出现代码内的中文字符乱码的问题，疑似是插件的编码标准设定问题。之后使用Thonny做调试，这里做编写



import socket
import time 
import network
import machine



def do_connect():#连接WiFi网络并返回本设备IP地址
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('gin71', 'qmhdwifi')
        i = 1
        while not wlan.isconnected():
            print("正在连接...{}".format(i))
            i += 1
            time.sleep(1)
    print('network config:', wlan.ifconfig())


def start_udp():
    # 2. 启动网络功能（UDP）

    # 2.1. 创建udp套接字
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 2.2. 绑定本地信息
    udp_socket.bind(("0.0.0.0", 7788)) #0，0，0，0的IP地址意思是接收所有来自本机的IP通讯

    return udp_socket


def main():
    # 1. 链接wifi
    do_connect()
    # 2. 创建UDP
    udp_socket = start_udp()
    # 3. 创建灯对象
    led = machine.Pin(2, machine.Pin.OUT)
    # 4. 接收网络数据
    while True:
        recv_data, sender_info = udp_socket.recvfrom(1024)
        print("{}发送{}".format(sender_info, recv_data))
        recv_data_str = recv_data.decode("utf-8")
        try:
            print(recv_data_str)
        except Exception as ret:
            print("error:", ret)
        
        # 5. 处理接收的数据
        if recv_data_str == "light on":
            print("这里是要灯亮的代码...")
            led.value(1)
        elif recv_data_str == "light off":
            print("这里是要灯灭的代码...")
            led.value(0)   


if __name__ == "__main__":
    main()
