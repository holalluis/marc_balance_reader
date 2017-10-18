#!/usr/bin/env python
# -*- coding: utf-8 -*-
import balance_reader as b

''' CONFIG LECTURA BALANÇA '''

port="/dev/ttyUSB0"    # per linux/mac
port="COM4"            # per windows
comanda='w'            # comanda enviada a la balança
espera=1               # lectura cada x segons
max_lectures=3         # num max de lectures abans de crear el csv
filename="results.csv" # nom arxiu csv

#llegeix balança
b.balance_reader(port, comanda, espera, max_lectures, filename)

