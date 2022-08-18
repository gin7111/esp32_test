#!/usr/bin/python3
# _*_ coding=utf-8 _*_

#连接wifi，创建UDP socket
#接收UDP传输的手柄数据并储存
#调用接收的键值数值，做平滑处理，映射为PWM频率
#从引脚2输出特定频率的脉冲


import socket
import time
import network
from machine import Pin,PWM


#连接WIFI，得到IP地址
def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('连接到网络：')
        wlan.connect('YCKZ', 'qmhdwifi')
        i = 1
        while not wlan.isconnected():
            print('正在连接，请稍后...{}'.format(i))
            i += 1
            time.sleep(1)
    print('已经连接到网络，本机ip地址为：', wlan.ifconfig())

#创建socket套接字
def start_udp():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('0.0.0.0', 7788))
    return udp_socket

#将手柄键值线性映射到频率区间，并转换为整型数据
def pwmfreqmap(data):
    freq1 = 100
    freq2 = 10000
    pwmfreq = (data-(-1))/2*(freq2-freq1)+freq1
    return int(pwmfreq)

#将手柄键值线性映射到占空比区间，并转换为整型数据
def pwmdutymap(data):
    duty1 = 0
    duty2 = 1023
    pwmduty = (data-(-1))/2*(duty2-duty1)+duty1
    return int(pwmduty)


#---------------------------------------------------------------------------
def main():

    do_connect()#连接WIFI

    udp_socket = start_udp()#创建socket套接字

    a = '轴向0'#要使用的值的字典键，使用多个数据就要添加多个判断

    #循环主体--------------------------------------------------
    while True:
        recv_data, sender_info = udp_socket.recvfrom(1024)#创建套接字，数据容量设定为1024
        recv_data_str = recv_data.decode("utf-8")#将接收到数据用utf-8解码，bit数据变为str
        
        if 'stop' in recv_data_str:#判断是否是停止指令：stop
            pwmout.deinit()

        elif '{' in recv_data_str:#判断是否是字典数据，这里用花括号做了判断条件
            recv_data_dict = eval(recv_data_str)#eval函数将字符串str当成有效的表达式来求值并返回计算结果。而ast组件下安全性更好,单micropython似乎没有这个库

            if a in recv_data_dict:#判断字典内是否有想要的字典键，防止字典中没有想要的键值而程序出错
                axe0 = recv_data_dict[a]#从转换好的字典中找到axe0的值，是手柄左摇杆X方向的键值，浮点数据，范围-1~1
                pwmout = PWM(Pin(2),freq=pwmfreqmap(axe0),duty=512)#开启pwm输出。将映射好的频率输出给pwm引脚控制脉冲频率
                # pwmout.freq(pwmfreqmap(axe0))
                # pwmout.duty(pwmdutymap(axe0))
        pass

if __name__ == "__main__":
    main()
