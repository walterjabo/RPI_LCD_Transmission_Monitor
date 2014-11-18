#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime
import transmissionrpc

lcd = Adafruit_CharLCD()

cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"

lcd.begin(16, 2)


def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output


tc = transmissionrpc.Client(address="localhost", port=9091, user='transmission', password='transmission')
torrent_name = tc.get_torrents()[0].name;
torrent_index = 0

str_torrent_index = str(torrent_index + 1)


texto_corredizo = torrent_name
texto_largo = texto_corredizo
i = 0
while 1:

	lcd.setCursor(0,1)
	percent = tc.get_torrents()[0].percentDone * 100;
	lcd.message(str(percent)+ ' %');
	sleep(1)

	k = 0
	while (k < 4):
		if len(texto_largo) < 16:
			texto_largo = texto_largo + '...' + texto_corredizo
		
		message_texto = (str_torrent_index + ':' + texto_largo)[:16]
		lcd.setCursor(0,0)
		lcd.message(message_texto)
		sleep(0.25)
		texto_largo = texto_largo[1:]
		i = i + 1
		k = k + 1
