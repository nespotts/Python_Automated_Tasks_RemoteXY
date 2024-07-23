import psutil
import time

def get_cpu_temp():
    temp = psutil.sensors_temperatures()['cpu_thermal'][0].current
    return temp

while True:
	print(f"The CPU Temperature is {get_cpu_temp()} C")
	time.sleep(0.1)
