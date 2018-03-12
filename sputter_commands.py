# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 15:09:43 2018

@author: Victor Rogalev
"""

import serial.tools.list_ports
import io

def set_remote (command, com_name):

    """ Open COM-port and send/read the command"""
    ser = serial.Serial(com_name,                   
                         baudrate=1200,
                         bytesize=serial.EIGHTBITS,
                         parity=serial.PARITY_NONE,
                         stopbits=serial.STOPBITS_ONE,
                         timeout=0.1)
    
    ser_io = io.TextIOWrapper(io.BufferedRWPair(ser, ser, 1),  
                               newline = '\r',
                               line_buffering = True)
    
    """Write a command(s) to pressure controller and read the reply """
    ser_io.write(command+"\r")
    read_str = ser_io.readline()   
    ser.close()
    return read_str