#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime

lcd = Adafruit_CharLCD()

cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"

lcd.begin(16, 2)


def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

tiempo = datetime.now()
fecha = tiempo.strftime('%A %d de %B del %Y')
fecha_mostrar = fecha
i = 0
while 1:
	tiempo = datetime.now()
	lcd.setCursor(0,1)
	lcd.message(tiempo.strftime('%H:%M:%S %p'))

	k = 0
	while (k < 4):
		if len(fecha_mostrar) < 16:
			fecha_mostrar = fecha_mostrar + '...' + fecha
		fecha_mostrar = fecha_mostrar[1:]
		#print(i, fecha_mostrar, len(fecha_mostrar))
		lcd.setCursor(0,0)
		lcd.message(fecha_mostrar)
		sleep(0.25)
		i = i + 1
		k = k + 1