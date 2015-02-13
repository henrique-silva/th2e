from TH2E import TH2E
import time

dev = TH2E('10.0.18.210',10001)

txt = open('th2e_sens.txt','w')
txt.write('Time\tTemperature\tHumidity\tDew Point\n')
txt.close()
while True:
    txt = open('th2e_sens.txt','a')
    tstamp = time.time()
    temp, hum, dew = dev.read_all()
    print(str(tstamp)+'\t'+str(temp)+'\t'+str(hum)+'\t'+str(dew))
    txt.write(str(tstamp)+'\t'+str(temp)+'\t'+str(hum)+'\t'+str(dew)+'\n')
    txt.close()
    time.sleep(1)
