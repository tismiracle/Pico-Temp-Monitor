import wmi
	
w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
sensors = w.Sensor()
cpu_temps = []
gpu_temp = 0
# f = open("logs.txt", "a")
for sensor in sensors:
	print(sensor)
	# f.writelines(str(sensor))
	if sensor.Name == "CPU Package" and sensor.SensorType == "Temperature":
		cpu_temps += [float(sensor.Value)]
	
	if sensor.Name == "GPU Core" and sensor.SensorType == "Temperature":
		gpu_temp += sensor.Value
	# if sensor.SensorType==u'Temperature' and not 'GPU' in sensor.Name:
	# 	cpu_temps += [float(sensor.Value)]
		
	# elif sensor.SensorType==u'Temperature' and 'GPU' in sensor.Name:
	# 	gpu_temp = sensor.Value
# f.close()

print(cpu_temps)
print("GPU: {}".format(gpu_temp))