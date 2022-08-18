from machine import Pin
led = Pin(2, Pin.OUT) #使用ESP32-DEVKITV1开发板，板载led连接引脚为GPIO2
led.value(1) #原代码使用的是led.on()但这里发现不能识别on这个函数，故采用value赋值控制电平
#led.on()