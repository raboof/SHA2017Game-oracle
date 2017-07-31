#!/usr/bin/env python

import wifi
import socket
import subprocess
import re
import time

while True:
	seekers = filter(lambda cell: cell.ssid == 'OracleSeeker', wifi.Cell.all('wlan0'))

	if len(seekers) > 0:
		print('Found seeker', seekers[0])
		cell = seekers[0]
		scheme = wifi.Scheme.find('wlan0', 'seeker')
		# scheme.save()
		scheme.activate()
	
		p = subprocess.Popen('/usr/sbin/arping -c 1 -i wlan0 192.168.4.1', shell=True, stdout=subprocess.PIPE)
		output, errors = p.communicate()
		if output:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect(('192.168.4.1', 2017))
			mac = re.findall(r'from (.*) \(1', output)[0].replace('from ', '').replace(' \(1', '')  
			s.send(mac)
			s.close()
			print('sent', mac);
		else:
			print(errors)
	else:
		time.sleep(5)
