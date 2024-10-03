#!/usr/bin/python3

import socket as s
import numpy as np 
import serial
import time

import logging
from logging.handlers import RotatingFileHandler

# Version 16

#ToDo's
# - figure out why raspi shake sends nothing to localhost ip
# - write a funktion to calculate the rasam value and put
#   all the neccesary variables in a class

# code can run on windows/linux for testing purposes
# choose which OS this code needs to run on with setting ACTIVE_OS
# configurable for testing purposes: for example to disable serial communication to
# avoid errors while on an testing rig
WINDOWS = 0
LINUX = 1
ACTIVE_OS = LINUX

MITTELUNGSZEIT = 2

class runtimesystem:
    name = ""
    serial_baudrate = 0
    serial_port = ""
    udp_ip_adress = ""
    udp_port_no = 0
    serial_coms_enabled = False
    debug_file_path = ""

SystemList = [runtimesystem(), runtimesystem()]

if ACTIVE_OS == WINDOWS:
    SystemList[WINDOWS].serial_baudrate = 9600
    SystemList[WINDOWS].serial_port = "COM0"
    SystemList[WINDOWS].udp_ip_adress = "127.0.0.1"
    SystemList[WINDOWS].udp_port_no = 8888
    SystemList[WINDOWS].serial_coms_enabled = False
    SystemList[WINDOWS].debug_file_path = "debug_file.txt"


if ACTIVE_OS == LINUX:
    # ip adress of the pi can change, need to get it from the
    # txt file in the OS path
    #hostipF = "/opt/settings/sys/ip.txt"
    #file = open(hostipF, 'r')
    #host = file.read().strip()
    #file.close()

    # pi only sends out the udp data to one of the physikal connection points ...
    # not possible to pipe data to localhost 127.0.0.1 for some reason
    SystemList[LINUX].serial_baudrate = 115200
    SystemList[LINUX].serial_port = "/dev/my_serial"
    SystemList[LINUX].udp_ip_adress = "172.17.0.2" # find it out with linux command "hostname -I"
    SystemList[LINUX].udp_port_no = 8888
    SystemList[LINUX].serial_coms_enabled = True
    SystemList[LINUX].debug_file_path = "/home/myshake/script/debug_log.txt"

# logger configuration
# saves file "debug_log.txt" in the same folder as the script
logger = logging.getLogger("Auswerteskript")
logger.setLevel(logging.DEBUG)

handler = RotatingFileHandler(SystemList[ACTIVE_OS].debug_file_path, maxBytes=5*1024*1024, backupCount=0)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# UDP-Connection
print("trying to start upd-connection")
logger.info("trying to start upd-connection")

sock = s.socket(s.AF_INET, s.SOCK_DGRAM)
sock.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)

# Funktion kümmert sich um die Ausgabe in:
# - Debugfile
# - Terminal
# - Seriellen Port
def print_HDF_output(timestamp,final_RSAM_value):
    message = 'HDF' + ';' + str(timestamp) + ';' + str(int(final_RSAM_value)) + '\n'

    if ACTIVE_OS == WINDOWS:                    # nur auf Windows auf Terminal ausgeben, blockiert sonst Linux SSH Terminal komplett
        print(message)

    logger.info(message)                        # in debug file Werte reinschreiben

    if SystemList[ACTIVE_OS].serial_coms_enabled:
        try:
            serial_port.write(message.encode())
        except:
            logger.critical("Serial Port not availible")


def print_EHZ_output(timestamp,final_RSAM_value):
    message = 'EHZ' + ';' + str(timestamp) + ';' + str(int(final_RSAM_value)) + '\n'

    if ACTIVE_OS == WINDOWS:                    # nur auf Windows auf Terminal ausgeben, blockiert sonst Linux SSH Terminal komplett
        print(message)

    logger.info(message)

    if SystemList[ACTIVE_OS].serial_coms_enabled:
        try:
            serial_port.write(message.encode())
        except:
            logger.critical("Serial Port not availible")


# checks if network port is ready
# nececcary because on the raspy it takes a few seconds to initialise the socket,
# will fail otherwise and script would be terminated with automatic start on boot
def UDP_portUsable():
    try:
       sock.bind((SystemList[ACTIVE_OS].udp_ip_adress, SystemList[ACTIVE_OS].udp_port_no))
       return True
    except:
       return False
    
while UDP_portUsable() == False:
    logger.critical("Network not yet ready, waiting ...")
    time.sleep(5)

host_msg = SystemList[ACTIVE_OS].udp_ip_adress + " " + str(SystemList[ACTIVE_OS].udp_port_no)
print(host_msg)
logger.info(host_msg)

# checks if given serial port is availible
def portIsUsable():
    try:
       ser = serial.Serial(SystemList[ACTIVE_OS].serial_port, SystemList[ACTIVE_OS].serial_baudrate)
       return True
    except:
       return False

# checks if serial communications should be enabled for given os
# opens port for serial communication accordingly
if SystemList[ACTIVE_OS].serial_coms_enabled:
    logger.info("Trying to connec to serial port")
    while portIsUsable() == False:
        #print("Serial Port not availible, retrying ...")
        logger.critical("Serial Port not availible, retrying ...")
        time.sleep(1)
    serial_port = serial.Serial(SystemList[ACTIVE_OS].serial_port, SystemList[ACTIVE_OS].serial_baudrate)


stream = []         # array holding all the single values from the data stream from the rapberry pi in an array
offset = 0          # calculated offset for the rsam value
rasam = 0           # calculated rsam value
timestamp = 0       # extracted timestamp from the raspberry shake data packet
message = ""        # serial message to be sent out
ehz_array = []      # calculate mean value of a few data packets
hdf_array = []      # calculate mean value of a few data packets

now_EHZ = 0             # Startzeitpunkt der Mittelung
now_HDF = 0

timestamp_EHZ = 0
timestamp_HDF = 0

print("server response in: DEBUGFILE")
logger.info("waiting for server to respond ...")

while 1:             
    data, addr = sock.recvfrom(1024)                        # warte bis Daten vom UDP-Port bereitgestellt werden
    s = data.decode('UTF-8').strip("'{}").split(', ')       # daten bereinigen und in array schreiben
    if 'EHZ' in s[0]:                                       # EHZ: 100 sample per second (E), high gain (H), single-component seismograph (Z) with 3 orthogonal channels of acceleration: EN[Z,N,E].
        timestamp_EHZ = s[1]
        for einzel_string in s[2:]:                         # jedenen einzelnen string ab dem 2. Element in einen Integer umwandeln
            stream = np.append(stream, int(einzel_string))

        # code zum generieren des RSAM:
        # calculate offet and substract it from all the values in the array
        # take the absolut values from this and then build the mean again
        offset = np.mean(stream)
        stream = np.subtract(offset, stream)
        stream = np.abs(stream)
        rasam = np.mean(stream)


        ehz_array = np.append(ehz_array,rasam)

        if float(timestamp_EHZ) > now_EHZ + MITTELUNGSZEIT:          # Wenn x Sekunden vergangen sind setze neuen Startzeitpunkt für Mittelung
            
            final_ehz_rsam_value = np.mean(ehz_array)        # alle gesammelten Messwerte in eingestellter Zeitspanne mitteln
            print_EHZ_output(now_EHZ,final_ehz_rsam_value)

            now_EHZ = float(timestamp_EHZ)
            ehz_array = []                                   # gespeicherte Messwerte löschen für nächsten Durchlauf


        stream = []                                         # reseting array
        
    if 'HDF' in s[0]:                                       # HDF: 100 sample per second (H), microbarometer (D), infrasound (F) monitor.
        timestamp_HDF = s[1]

        for einzel_string in s[2:]:                         # jedenen einzelnen string ab dem 2. Element in einen Integer umwandeln
            stream = np.append(stream, int(einzel_string))

        # code zum generieren des RSAM:
        # calculate offet and substract it from all the values in the array
        # take the absolut values from this and then build the mean again
        offset = np.mean(stream)
        stream = np.subtract(offset, stream)
        stream = np.abs(stream)
        rasam = np.mean(stream)

        hdf_array = np.append(hdf_array,rasam)

        if float(timestamp_HDF) > now_HDF + MITTELUNGSZEIT:          # Wenn x Sekunden vergangen sind setze neuen Startzeitpunkt für Mittelung
            
            final_hdf_rsam_value = np.mean(hdf_array)        # alle gesammelten Messwerte in eingestellter Zeitspanne mitteln
            print_HDF_output(now_HDF,final_hdf_rsam_value)

            now_HDF = float(timestamp_HDF)
            hdf_array = []                                   # gespeicherte Messwerte löschen für nächsten Durchlauf


        stream = []                                         # reseting array

