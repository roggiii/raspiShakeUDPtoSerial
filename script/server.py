#!/usr/bin/env python3

import socket as s
import serial
import time
import sys


from helper import configFileManager
from helper import serialCommsManager
from helper import calcRSAMvalue_withoutNumpy
from helper import calcMean
from myLogger import logger

#ToDo's
# - figure out why raspi shake sends nothing to localhost ip
# - write a funktion to calculate the rasam value and put
# -  all the neccesary variables in a class
# - logger needs to be made configurable from the file

# pi only sends out the udp data to one of the physikal connection points ...
# not possible to pipe data to localhost 127.0.0.1 for some reason

# code can run on windows/linux for testing purposes
# configurable for testing purposes: for example to disable serial communication to
# avoid errors while on an testing rig

# checks if network port is ready
# nececcary because on the raspy it takes a few seconds to initialise the socket,
# will fail otherwise and script would be terminated with automatic start on boot
def UDP_portUsable():
    try:
       sock.bind((system_info.udp_ip_adress, system_info.udp_port_no))
       return True
    except:
       return False
    
# Funktion kümmert sich um die Ausgabe in:
# - Debugfile
# - Terminal
# - Seriellen Port
def outputCalculatedValuesToSerial(timestamp,final_RSAM_value,type):
    message = type + ';' + str(timestamp) + ';' + str(int(final_RSAM_value)) + '\n'
    logger.info(message)
    serialManager.sendSerial(message)

# Starting point of script
logger.info("#------#------#------#------#------#------#------#------#------#------#------#------#------#------#------#------#------#")
logger.info("Starting script ...")

system_info = configFileManager("config.ini")
system_info.readFromConfigFile()
system_info.print_info()

serialManager = serialCommsManager(system_info.serial_baudrate, system_info.serial_port, system_info.serial_coms_enabled)
serialManager.connectSerial()

# UDP-Connection
logger.info("trying to start upd-connection")

sock = s.socket(s.AF_INET, s.SOCK_DGRAM)
sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)

while UDP_portUsable() == False:
    logger.warning("Networkcard not initialised, waiting ...")
    time.sleep(5)


stream = []         # array holding all the single values from the data stream from the rapberry pi in an array
offset = 0          # calculated offset for the rsam value
rasam = 0           # calculated rsam value
timestamp = 0       # extracted timestamp from the raspberry shake data packet
message = ""        # serial message to be sent out
ehz_array = []      # calculate mean value of a few data packets
hdf_array = []      # calculate mean value of a few data packets

now_EHZ = 0         # Startzeitpunkt der Mittelung
now_HDF = 0

timestamp_EHZ = 0
timestamp_HDF = 0

logger.warning("waiting for server to respond ...")

#################################### FOR DEBUG
#sys.exit()

while 1:             
    data, addr = sock.recvfrom(1024)                        # warte bis Daten vom UDP-Port bereitgestellt werden
    s = data.decode('UTF-8').strip("'{}").split(', ')       # daten bereinigen und in array schreiben
    if 'EHZ' in s[0]:                                       # EHZ: 100 sample per second (E), high gain (H), single-component seismograph (Z) with 3 orthogonal channels of acceleration: EN[Z,N,E].
        timestamp_EHZ = s[1]
        for einzel_string in s[2:]:                         # jedenen einzelnen string ab dem 2. Element in einen Integer umwandeln
            stream.append(int(einzel_string))

        rasam = calcRSAMvalue_withoutNumpy(stream)
        ehz_array.append(rasam)

        if float(timestamp_EHZ) > now_EHZ + system_info.communication_rate:          # Wenn x Sekunden vergangen sind setze neuen Startzeitpunkt für Mittelung
            
            final_ehz_rsam_value = calcMean(ehz_array)        # alle gesammelten Messwerte in eingestellter Zeitspanne mitteln
            outputCalculatedValuesToSerial(now_EHZ,final_ehz_rsam_value,'EHZ')

            now_EHZ = float(timestamp_EHZ)
            ehz_array = []                                   # gespeicherte Messwerte löschen für nächsten Durchlauf


        stream = []                                         # reseting array
        
    if 'HDF' in s[0]:                                       # HDF: 100 sample per second (H), microbarometer (D), infrasound (F) monitor.
        timestamp_HDF = s[1]

        for einzel_string in s[2:]:                         # jedenen einzelnen string ab dem 2. Element in einen Integer umwandeln
            stream.append(int(einzel_string))

        rasam = calcRSAMvalue_withoutNumpy(stream)    
        hdf_array.append(rasam)

        if float(timestamp_HDF) > now_HDF + system_info.communication_rate:          # Wenn x Sekunden vergangen sind setze neuen Startzeitpunkt für Mittelung
            
            final_hdf_rsam_value = calcMean(hdf_array)        # alle gesammelten Messwerte in eingestellter Zeitspanne mitteln
            outputCalculatedValuesToSerial(now_HDF,final_hdf_rsam_value,'HDF')

            now_HDF = float(timestamp_HDF)
            hdf_array = []                                   # gespeicherte Messwerte löschen für nächsten Durchlauf


        stream = []                                         # reseting array


