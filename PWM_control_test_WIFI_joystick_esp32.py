#!/usr/bin/python3
# _*_ coding=utf-8 _*_

# 连接wifi，创建UDP socket
# 接收UDP传输的手柄数据并储存
# 调用接收的键值数值，
# 数值在零漂范围内，则占空比保持为0%，控制电机静止。
# 数据超出零漂范围的，线性映射为PWM频率
# 数值为负数，从引脚15、5输出0，数值为正输出1
# GPIO15、5输出后，延时10μs，从引脚2、4输出特定频率的脉冲


import socket
import utime
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
            utime.sleep(1)
    print('已经连接到网络，本机ip地址为：', wlan.ifconfig())

#创建socket套接字
def start_udp():
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(('0.0.0.0', 7788))
    return udp_socket

#将手柄键值线性映射到频率区间，并转换为整型数据
def pwmfreqmap(data):
    freq1 = 100
    freq2 = 100000
    pwmfreq = abs(data)*(freq2-freq1)+freq1
    return int(pwmfreq)

#将手柄键值线性映射到占空比区间，并转换为整型数据
def pwmdutymap(data):
    duty1 = 0
    duty2 = 1023
    pwmduty = abs(data)*(duty2-duty1)+duty1
    return int(pwmduty)


#---------------------------------------------------------------------------
def main():

    do_connect()#连接WIFI

    udp_socket = start_udp()#创建socket套接字

    a = '轴向0'#要使用的值的字典键，使用多个数据就要添加多个判断
    b = '轴向1'

    zeroerror = 0.1#设定手柄摇杆零漂值

    pwmX = Pin(2, Pin.OUT)#设定GPIO2为X轴pwm输出引脚
    signX = Pin(15, Pin.OUT)#设定GPIO15为X轴方向信号引脚
    signX.value(0)

    pwmY = Pin(4, Pin.OUT)#设定GPIO4为Y轴pwm输出引脚
    signY = Pin(5, Pin.OUT)#设定GPIO5为Y轴方向信号引脚
    signY.value(0) 

    pwmXout = PWM(pwmX,freq=1,duty=0)#pwm频率设为最低的1，占空比0%用来控制电机静止
    pwmXout.init()#pwm初始化

    pwmYout = PWM(pwmY,freq=1,duty=0)#pwm频率设为最低的1，占空比0%用来控制电机静止
    pwmYout.init()#pwm初始化

    #循环主体--------------------------------------------------
    while True:
        recv_data, sender_info = udp_socket.recvfrom(1024)#创建套接字，数据容量设定为1024
        recv_data_str = recv_data.decode("utf-8")#将接收到数据用utf-8解码，bit数据变为str
        print(sender_info,'发送了',recv_data_str)
        if 'stop' in recv_data_str:#判断是否是停止指令：stop，是的话利用占空比为0控制电机停机
            pwmXout.freq(1)
            pwmXout.duty(0)

        elif '{' in recv_data_str:#判断是否是字典数据，这里用花括号做了判断条件
            recv_data_dict = eval(recv_data_str)#eval函数将字符串str当成有效的表达式来求值并返回计算结果。而ast组件下安全性更好,单micropython似乎没有这个库
            print('转为字典：', recv_data_dict)
            #------------------X轴------------------------------------
            if a in recv_data_dict:#判断字典内是否有想要的字典键，防止字典中没有想要的键值而程序出错
                axe0 = recv_data_dict[a]#从转换好的字典中找到axe0的值，是手柄左摇杆X方向的键值，浮点数据，范围-1~1
                print(axe0)
                if abs(axe0) <= zeroerror:#若摇杆数值在零漂范围内，则保持静止
                    pwmXout.freq(1)
                    pwmXout.duty(0)
                    signX.value(0)

                elif abs(axe0) > zeroerror:#若大于零漂值，则执行输出
                    if axe0 <= 0:#判断数值正负，正数赋高电平，其余低电平
                        dirX = 0
                    elif axe0 > 0:
                        dirX = 1                  
                    pwmXout.freq(pwmfreqmap(axe0))#将映射好的频率输出给pwm引脚控制脉冲频率
                    signX.value(dirX)#输出方向信号
                    utime.sleep_us(10)#延时要超过5μs,设定为10μs时实际延时50μs左右
                    pwmXout.duty(512)#开启pwm输出。

            #----------------------------Y轴---------------------------------
            if b in recv_data_dict:#判断字典内是否有想要的字典键，防止字典中没有想要的键值而程序出错
                axe1 = recv_data_dict[b]#从转换好的字典中找到axe1的值，是手柄左摇杆Y方向的键值，浮点数据，范围-1~1
                print(axe1)
                if abs(axe1) <= zeroerror:#若摇杆数值在零漂范围内，则保持静止
                    pwmYout.freq(1)
                    pwmYout.duty(0)
                    signY.value(0)

                elif abs(axe1) > zeroerror:#若大于零漂值，则执行输出
                    if axe1 <= 0:#判断数值正负，正数赋高电平，其余低电平
                        dirY = 0
                    elif axe1 > 0:
                        dirY = 1                  
                    pwmYout.freq(pwmfreqmap(axe1))#将映射好的频率输出给pwm引脚控制脉冲频率
                    signY.value(dirY)#输出方向信号
                    utime.sleep_us(10)#延时要超过5μs,设定为10μs时实际延时50μs左右
                    pwmYout.duty(512)#开启pwm输出。
        pass

if __name__ == "__main__":
    main()
