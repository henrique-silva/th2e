from spinel97 import Sensor
import struct

sensor_code = { 
    0x01 : "Temperature",
    0x02 : "Humidity",
    0x03 : "Dew Point",
}

ACK = {
    0x00 : "OK",
    0x01 : "Unknown error",
    0x02 : "Invalid instruction",
    0x03 : "Invalid instruction parameters",
    0x04 : "Permission denied", #write error, too low data, channel disabled, other requirements not met
    0x05 : "Device malfunction",
    0x06 : "Data not available",
    0x0d : "Digital input state change", #automatically sent message
    0x0e : "Continuous measurement", #automatically sent, repeatedly sending measured data
    0x0f : "Range overrun" #automatically sent
    }

class TH2E():
    def __init__(self,ip,port=10001):
        try:
            self.Sensor = Sensor(ip,port)
        except socket.error as err:
            print("Could not connect to the TH2E sensor, please verify the connection and try again")
            raise err

    def read_temp(self):
        data = self.Sensor.query(0x51, [0x00])
        raw = [data[x:x+4] for x in range(0,len(data),4)]
        readings = []
        for value in raw[:-1]:
            value = struct.unpack('>2BH', ''.join(value))
            if sensor_code[value[0]] == "Temperature":
                return (float(value[2])/10)
        raise ValueError("Temperature sensor couldn't be read, try again")

    def read_hum(self):
        data = self.Sensor.query(0x51, [0x00])
        raw = [data[x:x+4] for x in range(0,len(data),4)]
        readings = []
        for value in raw[:-1]:
            value = struct.unpack('>2BH', value)
            if sensor_code[value[0]] == "Humidity":
                return (float(value[2])/10)
        raise ValueError("Humidity sensor couldn't be read, try again")
        
    def read_dew(self):
        data = self.Sensor.query(0x51, [0x00])
        raw = [data[x:x+4] for x in range(0,len(data),4)]
        readings = []
        for value in raw[:-1]:
            value = struct.unpack('>2BH', value)
            if sensor_code[value[0]] == "Dew Point":
                return (float(value[2])/10)
        raise ValueError("Dew Point sensor couldn't be read, try again")

    def read_all(self):
        data = self.Sensor.query(0x51, [0x00])
        raw = [data[x:x+4] for x in range(0,len(data),4)]
        readings = []
        for value in raw[:-1]:
            value = struct.unpack('>2BH', value)
            readings.append(float(value[2])/10)
        return readings

    def reset(self):
        self.Sensor.instruct(0xE3,[])
