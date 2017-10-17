#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
	Script que:
			1. Crea una connexió serial amb la balança
			2. Envia una comanda cada x segons
			3. Rep la resposta
			4. Crea un CSV amb la resposta
				dd/mm/yyyy; hh:MM:ss; pes (g)
'''
print "+---------------------------+"
print "| BALANCE SERIAL CONNECTION |"
print "+---------------------------+"
import serial
import sys
import time

'''CONFIGURACIÓ LECTURA BALANÇA'''
comanda='w';    #comanda de la balança
espera=1;       #lectura cada 'espera' segons
max_lectures=3; #num max de lectures

'''CONFIGURACIÓ PORT SERIAL'''
ser=serial.Serial()
ser.port="/dev/ttyUSB0"
#ser.port="COM4"
ser.baudrate=9600
ser.bytesize=8
ser.parity=serial.PARITY_NONE
ser.stopbits=1
ser.xonxoff=False
ser.rtscts=False
ser.dsrdtr=False
ser.timeout=1
ser.open()
ser.flush()

'''MOSTRA CONFIGURACIÓ'''
print "Port:        ",ser.port
print "Comanda:     ",comanda
print "Lectura:      cada",espera,"segons"
print "Max lectures:",max_lectures
print
raw_input('Prem [Enter] per iniciar')

'''processa una resposta de la balança'''
def processa_resposta(resposta):
	resposta=['         0.2 g  \r\n', '         0.2 g  \r\n']; #exemple
	pes=resposta[0];
	pes=pes.replace(' ','').replace('g','').replace('\r','').replace('\n','');
	#date
	tm=time.localtime();
	yy=str(tm.tm_year);
	mm=str(tm.tm_mon);
	dd=str(tm.tm_mday); 
	hh=str(tm.tm_hour); 
	MM=str(tm.tm_min);  
	ss=str(tm.tm_sec);  
	if int(mm)<10: mm='0'+mm;
	if int(dd)<10: dd='0'+dd;
	if int(hh)<10: hh='0'+hh;
	if int(MM)<10: MM='0'+MM;
	if int(ss)<10: ss='0'+ss;
	return [dd+"/"+mm+"/"+yy,hh+":"+MM+":"+ss,pes];

#variable on es guardaran totes les dades
serie_temporal=[];

#comptador de lectures per parar el loop
comptador_lectures=0;

'''LOOP DE LECTURA'''
while True:
	ser.write(comanda);
	ser.flush();
	resposta=ser.readlines();
	fila=processa_resposta(resposta);
	print fila;
	serie_temporal.append(fila);
	comptador_lectures+=1;
	if comptador_lectures >= max_lectures: break;
	time.sleep(espera);


'''CREA UN FITXER CSV'''
def crea_csv():
	#open file: si file no existeix, es crea. si existeix, es sobreescriu
	filename="corba.csv"
	f=open(filename,'w'); #f és un handler

	#escriu coses a f
	f.write('Dia; Hora; Pes (g)\n');

	#recorre la serie temporal i escriu al fitxer
	for fila in serie_temporal: 
		f.write(fila[0]+";"+fila[1]+";"+fila[2]+"\r\n");

	#tanca el fitxer
	f.close();

#crida la funcio per crear csv
crea_csv()

