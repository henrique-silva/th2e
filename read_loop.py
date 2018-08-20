#!/usr/bin/python

import os
import sys
import time
from time import sleep
from TH2E import TH2E
import argparse
import socket

parser = argparse.ArgumentParser()
parser.add_argument('output', help='output file where the readings will be written')
parser.add_argument('delay', type=float, help='time between the readings in seconds', default=10)
parser.add_argument('-i','--ip', help='set sensor ip', default='10.2.117.254')
parser.add_argument('-u','--utc', help='Use UTC time as reference', action='store_true')
args = parser.parse_args()

abspath = os.path.abspath(args.output)
if not os.path.exists(os.path.dirname(abspath)):
    try:
        os.makedirs(os.path.dirname(abspath))
    except OSError as exc: # Guard against race condition
        if exc.errno != errno.EEXIST:
            raise

if args.utc:
    time_fmt = 'UTC+0'
else:
    time_fmt = 'UTC'+time.strftime('%Z', time.localtime(time.time()))

if os.path.isfile(abspath):
    f = open(abspath, 'a+')
else:
    f = open(abspath, 'w')
    f.write('Time [{}]\t\tTemperature\tHumidity\tDew Point\n'.format(time_fmt))

print('\nThe following sensors are being monitored, press ctrl-c to stop...')
print('Time [{}]\t\tTemperature\tHumidity\tDew Point\n'.format(time_fmt)),

while True:
    try:
        sensor = TH2E(args.ip)
        while True:
            try:
                if args.utc:
                    time_data = time.gmtime(time.time())
                else:
                    time_data = time.localtime(time.time())

                resp = sensor.read_all()
                if len(resp) == 3:
                    temp, hum, dew = resp
                    data_str = time.strftime('%Y/%m/%d %H:%M:%S', time_data)+'\t'+str(temp)+'\t\t'+str(hum)+'\t\t'+str(dew)+'\n'
                    print(data_str),
                    f.write(data_str)
                    sys.stdout.flush()
                    sleep(args.delay)
            except ValueError as e:
                print(e)
                pass
            except KeyboardInterrupt:
                raise
    except socket.error:
        #Wait some time before trying to connect again
        sleep(1)
        pass
    except KeyboardInterrupt:
        f.close()
        sensor.close()
        exit()
