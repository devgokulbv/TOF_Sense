#coding: UTF-8
import RPi.GPIO as GPIO
import serial 
import time
import chardet
import sys
import statistics as sts
import math
from ast import literal_eval
import codecs
#the below array is 31 byte array
Hex_data=[0x54,0x20,0x00,0xff,0x00,0x00,0x00,0x00,0x00,0x08,0xff,0xff,0x00,0x10,0x0E,0x0f,0x0f,0x00,0x00,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff]
byte_array=[]
TOF_length = 16
TOF_length1=32
TOF_header=(87,0,255)
TOF_system_time = 0
TOF_distance = 0
TOF_status = 0
TOF_signal = 0
TOF_check = 0
TOF_baudrate =0
arr=[]
ser = serial.Serial('/dev/ttyS0',926100)
ser.flushInput()
#the below function adds the 31 byte array and appends 32nd byte
def verifyAddSum(data, len):
    #print(data)
    TOF_check = 0
    for  k in range(0,31):
        TOF_check += Hex_data[k]
    TOF_check=TOF_check%256
    #print(hex(TOF_check))
    Hex_data.append(TOF_check)
    
def verifyCheckSum(data, len):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
    print(data)
    TOF_check = 0
    for  k in range(0,len-1):
        TOF_check += data[k]
    TOF_check=TOF_check%256
    
    if(TOF_check == data[len-1]):
        #print("TOF data is ok!")
        return 1    
    else:
        #print("TOF data is error!")
        return 0  
verifyAddSum(Hex_data[0:TOF_length1],TOF_length1) #function called
string=''
bytestring =''
for i in range(0,32):
    byte_val=Hex_data[i].to_bytes(1, 'big')#convert int to byte value
    #print(byte_val)
    ser.write(byte_val)#we write the 32 byte values to sensor
temp=1
while temp<11:
    TOF_data=()
    time.sleep(0.05)
    if ser.inWaiting() >=32:
        for i in range(0,32):
            TOF_data=TOF_data+(ord(ser.read(1)),ord(ser.read(1)))
        #print(TOF_data)
        for j in range(0,32):
            if( (TOF_data[j]==TOF_header[0] and TOF_data[j+1]==TOF_header[1] and TOF_data[j+2]==TOF_header[2]) and (verifyCheckSum(TOF_data[j:TOF_length],TOF_length))):
                if(((TOF_data[j+12]) | (TOF_data[j+13]<<8) )==0):
                    print("Out of range!")
                else:
                    #print("TOF id is: "+ str(TOF_data[j+3]))
                

                    TOF_system_time = TOF_data[j+4] | TOF_data[j+5]<<8 | TOF_data[j+6]<<16 | TOF_data[j+7]<<24;
                    print("TOF system time is: "+str(TOF_system_time)+'ms')

                    TOF_distance = (TOF_data[j+8]) | (TOF_data[j+9]<<8) | (TOF_data[j+10]<<16);
                    print("TOF distance is: "+str(TOF_distance)+'mm')
                    arr.append(TOF_distance)

                    TOF_status = TOF_data[j+11];
                    #print("TOF status is: "+str(TOF_status))
                    TOF_signal = TOF_data[j+12] | TOF_data[j+13]<<8;
                    #print("TOF signal is: "+str(TOF_signal))
                    
                    temp+=1 
             
       
                break;
print("acutal distance+/-5mm: ",sts.mean(arr))          
     
    
        
    





