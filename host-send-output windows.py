import serial
import time
import wmi


cpu_temps = 0
cpu_load = 0
gpu_temps = 0
gpu_load = 0
# all_temps = {"cpu": cpu_temps, "gpu": gpu_temps}
all_temps = "null"
# f = open("logs.txt", "a")

# open a serial connection


# s = serial.Serial("/dev/ttyACM0", 115200)
s = serial.Serial("COM3", 115200)


# blink the led
# TCTL TCCD1 GPU
while True:
	w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
	sensors = w.Sensor()

	for sensor in sensors:
		if sensor.Name == "CPU Package" and sensor.SensorType == "Temperature":
			cpu_temps = int(sensor.Value)

		if sensor.Name == "CPU Total" and sensor.SensorType == "Load":
			cpu_load = int(sensor.Value)
			# all_temps["cpu"] = sensor.Value
		if sensor.Name == "GPU Core" and sensor.SensorType == "Temperature":
			gpu_temps = int(sensor.Value)

		if sensor.Name == "GPU Core" and sensor.SensorType == "Load":
			gpu_load = int(sensor.Value)
		
			# all_temps["gpu"] = sensor.Value

	print("Hello World")
	print(all_temps)
	all_temps = str(cpu_temps) + " " + str(cpu_load) + " " + str(gpu_temps) + " " + str(gpu_load) + "\n"
	splitted_temps = all_temps.split()
	print(splitted_temps)
	s.write(all_temps.encode("utf-8"))
	
	# s.write(str(all_temps).encode("utf-8"))
	# s.write(b"\n")
	time.sleep(1.5)

