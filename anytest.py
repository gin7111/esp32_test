#测试对空字典的循环写入--------------------------
# adict = {}
# for i in range(5):
#     adict['number{}'.format(i)] = i + 1

# print(adict)

#测试微秒级延时-------------------------------------
import utime


time1 = utime.ticks_us()
utime.sleep_us(10)
time2 = utime.ticks_us()
print('睡眠时间',time2-time1)#设定为10μs时实际延时50μs左右
