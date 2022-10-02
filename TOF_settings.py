import math
from ast import literal_eval
import codecs
Hex_data=[0xff,0xff,0x00,0xff,0x00,0x00,0x00,0x00,0x00,0x08,0xff,0xff,0x00,0x10,0x0E,0x0f,0x0f,0x00,0x00,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff]
TOF_length = 31
def verifyAddSum(data, len):
    #print(data)
    TOF_check = 0
    for  k in range(0,31):
        TOF_check += Hex_data[k]
    TOF_check=TOF_check%256
    print(hex(TOF_check))
    Hex_data.append(TOF_check)
verifyAddSum(Hex_data[0:TOF_length],TOF_length)
string=''
bytestring =''
for i in range(0,32):
    #print(hex(Hex_data[i]))
    hex_string = "{0:08b}".format(Hex_data[i])
    string += hex_string
    #print(hex_string)
    byte_value = str(Hex_data[i].to_bytes(1,'big'))
    bytestring += byte_value
print(Hex_data)
print(string)
print(bytestring)