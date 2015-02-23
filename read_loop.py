#!/usr/bin/python

import os
import sys
import time
from time import sleep
from TH2E import TH2E
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('output', help='output file where the readings will be written')
parser.add_argument('delay', type=float, help='time between the readings in seconds', default=10)
args = parser.parse_args()

sensor = TH2E('10.0.18.210')
abspath = os.path.abspath(args.output)
if os.path.exists(abspath):
    f = open(abspath, 'a')
else:
    f = open(abspath, 'w')
    f.write('Time\tTemperature\tHumidity\tDew Point\n')

last_read_time = time.time()
print('\tTemperature, Humidity and Dew point being monitored, press ctrl-c to stop...')

while True:
    temp, hum, dew = sensor.read_all()
    f.write(str(last_read_time)+'\t'+str(temp)+'\t'+str(hum)+'\t'+str(dew)+'\n')
    try:
        while time.time() - last_read_time < args.delay:
            sleep(1)
    except KeyboardInterrupt:
        break

    last_read_time = time.time()

    
