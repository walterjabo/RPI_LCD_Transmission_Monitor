#!/usr/bin/python

from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime
import transmissionrpc
import threading
import math

lcd = Adafruit_CharLCD()
lcd.begin(16, 2)

bloqueo = 0
torrent_index = 0
torrent_name = ""

def usarLCD():
	global bloqueo
	if bloqueo == 1:
		while bloqueo != 0:
			sleep(0.001)
	bloqueo = 1

def desbloquearLCD():
	global bloqueo
	bloqueo = 0

def workerCorrerTexto(lcd):

	global torrent_index
	global torrent_name

	old_index = 0
	texto_largo = torrent_name

	while 1:
		if old_index != torrent_index:
			texto_largo = torrent_name
			old_index = torrent_index

		prefix = str(torrent_index + 1)+':'

		if len(texto_largo) < 16:
			texto_largo = texto_largo + '...' + torrent_name
		
		message_texto = (prefix + texto_largo)[:16]

		usarLCD()
		lcd.setCursor(0,0)
		lcd.message(message_texto)
		desbloquearLCD()

		sleep(0.25)
		texto_largo = texto_largo[1:]

def workerMostrarPorcentaje(lcd):

	global torrent_index
	global torrent_name

	kind_info = 0
	while 1:
		torrent_list = tc.get_torrents()
		torrent_length = len(torrent_list)
		torrent = torrent_list[torrent_index]
		torrent_name = torrent.name
		percent = torrent.percentDone * 100;
		downRate = torrent.rateDownload;

		velocidadKBs = math.fsum([downRate / 1024])

		sizeDownloaded = math.fsum([torrent.downloadedEver/1024.0/1024.0])
		unidadesDownloaded = 'MB'
		if sizeDownloaded > 1024:
			sizeDownloaded = math.fsum([sizeDownloaded / 1024.0])
			unidadesDownloaded = 'GB'

		sizeWhenDone = math.fsum([torrent.sizeWhenDone/1024.0/1024.0])
		unidadesWhenDone = 'MB'
		if sizeWhenDone > 1024:
			sizeWhenDone = math.fsum([sizeWhenDone / 1024.0])
			unidadesWhenDone = 'GB'

		mensaje = ''
		if kind_info == 0:
			mensaje = str(round(percent, 2))+ '% ' + str(round(velocidadKBs, 2)) + 'kB/s                '
			kind_info = 1
		elif kind_info == 1:
			mensaje = str(round(sizeDownloaded, 2)) + unidadesDownloaded + ' / ' + str(round(sizeWhenDone, 2)) + unidadesWhenDone + '                '
			kind_info = 2
		elif kind_info == 2:
			mensaje = (int(round(percent/100*16)) * '#')+'                  '
			kind_info = 0
		else:
			mensaje = "NOTHING"
			kind_info = 0

		usarLCD()
		lcd.setCursor(0,1)
		lcd.message(mensaje[:16]);
		desbloquearLCD()

		sleep(3)

		if kind_info == 0:
			if torrent_index < torrent_length - 1:
				torrent_index = torrent_index + 1
			else:
				torrent_index = 0
			torrent_name = torrent_list[torrent_index].name


tc = transmissionrpc.Client(address="localhost", port=9091, user='transmission', password='transmission')

threads = list()
t1 = threading.Thread(target=workerCorrerTexto, args=(lcd,))
threads.append(t1)

t2 = threading.Thread(target=workerMostrarPorcentaje, args=(lcd,))
threads.append(t2)

t2.start()
t1.start()
