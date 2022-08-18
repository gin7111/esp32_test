from machine import Pin, PWM
import time
#----------------------
#example

#from machine import Pin, PWM

# pwm0 = PWM(Pin(0))         # create PWM object from a pin
# freq = pwm0.freq()         # get current frequency (default 5kHz)
# pwm0.freq(1000)            # set PWM frequency from 1Hz to 40MHz

# duty = pwm0.duty()         # get current duty cycle, range 0-1023 (default 512, 50%)
# pwm0.duty(256)             # set duty cycle from 0 to 1023 as a ratio duty/1023, (now 25%)
#------------------------------

led2 = PWM(Pin(2, Pin.OUT), freq=20000)
#led2.init()#初始化
#led2.freq(20000) #控制频率
#led2.duty() #控制占空比默认50%
# time.sleep(5)
# led2.deinit()#关闭PWM输出
#-----------------------------------

#下面的循环完成呼吸灯效果
# while True:
#     for i in range(0,1024):
#         led2.duty(i)
#         time.sleep_ms(1)

#     for i in range(1023,-1,-1):
#         led2.duty(i)
#         time.sleep_ms(1)

#下面的循环完成频率变化测试
led2.duty()
freq1 = 10_000
freq2 = 500_000

while True:
    for i in range(freq1,freq2,100):
        led2.freq(i)
        time.sleep_ms(5)

    for i in range(freq2,freq1,-100):
        led2.freq(i)
        time.sleep_ms(5)
