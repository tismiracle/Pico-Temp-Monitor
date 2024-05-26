import serial
import time
import psutil
import string
import subprocess

cpu_temps_list = []
cpu_core_names = []
app_dict = {}
# open a serial connection
def get_cpu_temps():
    cpu_temps_list.clear()
    cpu_core_names.clear()
    cpu_temp = psutil.sensors_temperatures()['k10temp']

    
    for temp_types in cpu_temp:
        for value, temps in enumerate(temp_types):
            #print(value, temps)
            #cpu_temps_list.append(temps)
            if value == 0:
                cpu_core_names.append(temps)
            if value == 1:
                cpu_temps_list.append(temps)
            if value >= 1:
                break
    #print(str(cpu_temps_list))
    return cpu_temps_list, cpu_core_names

def get_nvidia_temps():
    #gpu_temp = str(os.system('nvidia-smi -q -d temperature | grep -w "GPU Current Temp"'))
    import re
    gpu_temp = subprocess.getoutput("nvidia-smi -q -d temperature | grep -w 'GPU Current Temp'")
    gpu_name = subprocess.getoutput("nvidia-smi -L")
    match = re.search("NVIDIA*([^(])+", gpu_name)
    #print(match.group())
    gpu_name = match.group()

    gpu_temp = gpu_temp.split(":")
    gpu_temp_digits = ""
    #print(gpu_temp[1])
    for letter in gpu_temp[1]:
        #print(letter)
        if letter.isdigit():
            #print(letter)
            gpu_temp_digits += letter
    #print(int(gpu_temp_digits))
    return [gpu_temp_digits], [gpu_name] #return a list of temperatures and gpu names
        
def get_cpu_usage():
    #cpu_stats = psutil.cpu_stats()
    cpu_freq = psutil.cpu_freq().current
    #core_freq = psutil.cpu_freq(percpu=True)
    cpu_percent = psutil.cpu_percent()
    core_percent = psutil.cpu_percent(percpu=True)
    return cpu_percent, core_percent, cpu_freq



# s = serial.Serial("/dev/ttyACM0", 115200)
# s = serial.Serial("COM1", 115200)

# blink the led
# TCTL TCCD1 GPU
while True:
    #print(get_nvidia_temps())

    cpu_usage = get_cpu_usage()
    #print(cpu_usage)
    cpu_temps = get_cpu_temps()
    # gpu_temps = get_nvidia_temps()
    # print(gpu_temps)
    app_dict["cpu_temps"] = cpu_temps[0] # cpu temperature
    app_dict["cpu_names"] = cpu_temps[1] # cpu names [name of dies]
    # app_dict["gpu_temps"] = gpu_temps[0] # gpu temperature
    # app_dict["gpu_names"] = gpu_temps[1] # gpu names
    #app_dict["names"] =
    app_dict["cpu_usage"] = cpu_usage
    print(app_dict)
    #app_dict = str(app_dict)
    #temps[0].append(get_nvidia_temps())
    #temps[1].append("GPU1")
    #temps.append(get_nvidia_temps())
    #temps = str(temps)
    #print(temps)
    #temps = str(temps)
    #s.write(temps.encode('utf-8'))
    s.write(str(app_dict).encode('utf-8'))
    s.write(b'\n')
    time.sleep(1)
