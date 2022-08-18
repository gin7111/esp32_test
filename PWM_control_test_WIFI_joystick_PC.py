#!/usr/bin/python3
# -*- coding=utf-8 -*- 


#将Xbox手柄和设备同时连接到电脑，使用程序接收手柄摇杆模拟量，
#再利用模拟量控制PWM频率，进而控制伺服电机运动和速度


import pygame
from pygame.locals import *
from socket import *
from time import ctime



#定义存放数据用的字典
#Joystick = {'LeftX':0.000, 'LeftY':0.000, 'RightX':0.000, 'RightY':0.000, 'Lefttrigger':0.000, 'Righttrigger':0.000, 'A':0, 'B':0, 'X':0, 'Y':0,'Leftshoulder':0, 'Rightershoulder':0, 'CrossX':0, 'CrossY':0}
JoyDict = { }

#定义用到的颜色
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

#设置窗口大小
size = [500, 1000]

#socket传输数据用的网络设置--------------------
host = ''#主机ip
port = 8082#主机端口
datasize = 1024
addr = (host, port)
recvip = '192.168.197.199'#接收ip
recvport = 7788#接收端口
recvddr = (recvip, recvport)

#用类简化显示的调用，记得要实例化---------------------------------------------
class textPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.SysFont("microsoftyaheiui", 15)#定义使用系统字体：微软雅黑，字号20

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height#输出文字，并换行
    
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):#产生宽度为10的缩进
        self.x += 10

    def unindent(self):#减少宽度为10的缩进
        self.x -= 10



def main():
    pygame.init()#初始化pygame

    done = False#用于控制循环开始和结束，赋值True之后结束main循环
    clock = pygame.time.Clock()#用于控制扫描频率
    
    screen = pygame.display.set_mode(size)#创建名为screen的surface对象
    #设置窗口标题
    pygame.display.set_caption("My Game")

    pygame.joystick.init()#初始化joystick模块

    TextPrint = textPrint()#实例化类，准备好打印

#--------------------主要执行内容-------------------------
    while done == False:
        for event in pygame.event.get(): # 事件监听，用于关闭
            if event.type == pygame.QUIT: # 点击窗口退出键时触发
                done=True # 改变标志退出循环

        #--------------------创建socket通讯套接字----------------------
        udp_socket = socket(AF_INET, SOCK_DGRAM)
        udp_socket.bind(addr)
        #--------------------扫描手柄并记录和显示----------------------
        screen.fill(WHITE)
        TextPrint.reset()#绘制白底窗口准备显示
        
        joystick_count = pygame.joystick.get_count()#获取手柄数量
        TextPrint.print( screen, "控制器数量: {}".format(joystick_count) )
        TextPrint.indent()
    
        for i in range(joystick_count):#开始扫描所有按键
            joystick = pygame.joystick.Joystick(i)#获取按键编号
            joystick.init()#初始化模块

            TextPrint.print(screen, "控制器 {}".format(i) )
            TextPrint.indent()

            #从controller/joystick系统中获取按键名称
            name = joystick.get_name()
            TextPrint.print(screen, "控制器名称: {}".format(name) )

            #获取摇杆数量，左右摇杆和肩键都是，其中摇杆一个方向上有一对axe，而一个肩键只有单个axe
            axes = joystick.get_numaxes()
            TextPrint.print(screen, "摇杆轴数量: {}".format(axes) )

            for i in range( axes ):
                axis = joystick.get_axis( i )
                JoyDict['轴向{}'.format(i)] = axis#键值写入字典，对应字典键为"轴向i"
                TextPrint.print(screen, "轴向 {} 值: {:>6.3f}".format(i, axis) )#右对齐，宽度为6，保留三位小数
            TextPrint.unindent()

            #按钮    
            buttons = joystick.get_numbuttons()
            TextPrint.print(screen, "按键数量: {}".format(buttons) )
            TextPrint.indent()

    
            for i in range( buttons ):
                button = joystick.get_button( i )
                JoyDict['按钮 {:>2}'.format(i)] = button#键值写入字典
                TextPrint.print(screen, "按钮 {:>2} 键值: {}".format(i,button) )#右对齐，宽度为2
            TextPrint.unindent()


            # 十字方向键返回的数值是一个数组，第一位为X轴，左-1右1，第二位Y轴上1下-1
            hats = joystick.get_numhats()
            TextPrint.print(screen, "十字键轴数量: {}".format(hats) )
            TextPrint.indent()

    
            for i in range( hats ):
                hat = joystick.get_hat( i )
                JoyDict['十字键 {}'.format(i)] = hat#键值写入字典，注意此时键值为数组
                TextPrint.print(screen, "十字键 {} 键值: {}".format(i, str(hat)) )
            TextPrint.unindent()
            TextPrint.unindent()#两次取消缩进回到左顶格

        TextPrint.print(screen, '储存数据：')#在窗口显示字典内容
        for joyname,joyvalue in JoyDict.items():
            joynameandvalue = joyname + ':' + str(joyvalue)
            TextPrint.print(screen, joynameandvalue)

        #将字典数据用utf-8编码发送给单片机----------------------------------
        udp_socket.sendto(str(JoyDict).encode("utf-8"), recvddr)

        #刷新显示内容
        pygame.display.flip()

        clock.tick(20)#不要超过每秒20

    udp_socket.close()#关闭socket通讯
    pygame.quit()#退出模块


        
if __name__ == '__main__':
    main()
