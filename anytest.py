#测试对空字典的循环写入--------------------------
# adict = {}
# for i in range(5):
#     adict['number{}'.format(i)] = i + 1

# print(adict)

# #测试微秒级延时-------------------------------------
# import utime


# time1 = utime.ticks_us()
# utime.sleep_us(10)
# time2 = utime.ticks_us()
# print('睡眠时间',time2-time1)#设定为10μs时实际延时50μs左右

#计数器测试------------------------------------------

# from machine import Timer, Pin, PWM
# import utime

# p_out = Pin(2, Pin.OUT)
# p_in = Pin(15)
# tim = Timer(2)

# pwm_freq = 1
# pwm_duty = 0

# pwmout = PWM(p_out, freq=pwm_freq, duty=pwm_duty)
# pwmout.init()

# tim.init(freq=10000)
# ch1 = tim.channel(1, Timer.ENC_A, pin=p_in)#只用PYB平台的Timer有channel模块，ESP平台无效
# utime.sleep(1)

# while True:
#     pwmout.duty(512)
#     utime.sleep(1)
#     print(tim.counter())

#Pin.IN配合pwm计数测试
import machine
from machine import Pin, PWM
import utime

done = False
pwmin = Pin(15,Pin.IN)#高电平为1，低电平为0，但悬空时为1
pwmout = Pin(2,Pin.OUT)
count = 0


pwm = PWM(pwmout,duty=0)
pwm.init()
pwm.freq(1)
pwm.duty(512)
t1 = utime.ticks_ms()
while done == False:
    print(pwmin.value())
    # if pwmin == 1:
    #     count += 1
    #     print(count)
        # if count == 10:
        #     pwmout.duty(0)
        #     done = True
        #     print('耗时', utime.ticks_ms()-t1)
