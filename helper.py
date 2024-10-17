#!/usr/bin/python3
import configparser
import os.path
import sys
import serial
import time

from myLogger import logger

def calcMean(x):
    """takes integer array as input and calculated mean value"""
    i = 0
    for item in x:
        i = i+item

    mean = i / len(x)
    return(mean)

def calcSubtraction(x,offset):
    """takes ingeger array as input and subtracts a value from every element"""
    x = list(x)
    for item in range(len(x)):
        x[item] = x[item] - offset
    return x

def calcAbs(x):
    for item in range(len(x)):
        x[item] = abs(x[item])
    return x

# RSAM calculation:
# calculate offet and substract it from all the values in the array
# take the absolut values from this and then build the mean again
def calcRSAMvalue_withoutNumpy(measurement_values):
    if len(measurement_values) == 0:
        return 0
    offset = calcMean(measurement_values)
    foo = calcSubtraction(measurement_values, offset)
    foo = calcAbs(foo)
    rsam = calcMean(foo)
    return rsam


class serialCommsManager:
     
    serial_baudrate = 0
    serial_port = ""
    serial_coms_enabled = False
    serialObject = 0

    def __init__(self,serial_baudrate,serial_port,serial_coms_enabled):
         self.serial_baudrate = serial_baudrate
         self.serial_port = serial_port
         self.serial_coms_enabled = serial_coms_enabled
         
    def reconnectSerial(self):
        try:
            logger.info("Tryping to reconnect to serial port "+self.serial_port + " ...")
            self.serialObject = serial.Serial(self.serial_port, self.serial_baudrate)
        except:
            logger.warning("Serial port could not be connected!")
            time.sleep(1)
            self.reconnectSerial()

    def connectSerial(self):
        if self.serial_coms_enabled == True:
            try:
                logger.info("Serial port enabled, trying to connect ...")
                self.serialObject = serial.Serial(self.serial_port, self.serial_baudrate)
            except:
                logger.warning("Serial port could not be connected!")
                self.reconnectSerial()

    def sendSerial(self,message):
        if self.serial_coms_enabled == True:
            try:
                self.serialObject.write(message.encode())
            except:
                logger.warning("Serial port could not be connected!")
                self.reconnectSerial()


class configFileManager:
    os_name = ""
    serial_baudrate = 0
    serial_port = ""
    udp_ip_adress = ""
    udp_port_no = 0
    serial_coms_enabled = False
    file_logger_debug_level = ""
    terminal_logger_debug_level = ""

    CONFIG_FILE_PATH = ""

    def __init__(self,config_file_name):
        # when the script is executed automatically on boot, linux needs an absolute
        # path to the config file
        self.CONFIG_FILE_PATH = os.path.dirname(__file__)+"/"+config_file_name
        

    # creates new config file with default values
    def __create_config(self):
        logger.info("Configfile does not exist, creating file in working directory ...")

        config = configparser.ConfigParser()

        # Add sections and key-value pairs
        config['General'] = {
            'os_name': 'Test'}

        config['Serial_Communication'] = {
            'baudrate': '9600',
            'port': 'COM0',
            'enabled': False}
        
        config['UDP_Communication'] = {
            'ip_adress': "127.0.0.1",
            'port_numnber': 8888}
        
        config['Logging'] = {
            'file_logger_debug_level': 'info',
            'terminal_logger_debug_level': 'info'}

        # Write the configuration to a file
        try:
            with open(self.CONFIG_FILE_PATH, 'w') as configfile:
                config.write(configfile)
        except:
            logger.info("Configfile could not be created!")
            logger.info('Linux needs absolute paths: -> "/home/myshake/script/debug_log.txt"')
            logger.info("If you run into trouble, copy the full filepath into the CONFIG_FILENAME variable in this script")
            logger.info("Terminating script ....")
            sys.exit()

        logger.info('Configfile "'+ self.CONFIG_FILE_PATH +'" has been created')
        logger.info("Script needs to be restarted bevore new settings are activated")
        logger.info("Terminating script ... goodbye!")
        sys.exit()

    # writes contents of the config file to object
    def __get_settings(self):
        config = configparser.ConfigParser()
        config.read(self.CONFIG_FILE_PATH)

        self.os_name = config.get('General','os_name')
        self.serial_baudrate = config.getint('Serial_Communication','baudrate')
        self.serial_port = config.get('Serial_Communication','port')
        self.serial_coms_enabled = config.getboolean('Serial_Communication','enabled')

        self.udp_ip_adress = config.get('UDP_Communication', 'ip_adress')
        self.udp_port_no = config.getint('UDP_Communication', 'port_numnber')

        self.file_logger_debug_level = config.get('Logging', 'file_logger_debug_level')
        self.terminal_logger_debug_level = config.get('Logging', 'terminal_logger_debug_level')

    # logger.infos all the availible public variable data for the communication
    def print_info(self):
        logger.info("------------ Settings ------------")
        logger.info("# Operatingsystem: "+self.os_name)
        logger.info("# Serial Communication:")
        logger.info("- Baudrate: "+str(self.serial_baudrate))
        logger.info("- Serialport: "+self.serial_port)
        logger.info("- enabled: "+str(self.serial_coms_enabled))
        logger.info("# UDP-Communication:")
        logger.info("- IP-Adress: "+self.udp_ip_adress)
        logger.info("- Portnumber: "+str(self.udp_port_no))
        logger.info("# Logging")
        logger.info("- file logger level: "+ self.file_logger_debug_level)
        logger.info("- terminal logger level: "+ self.terminal_logger_debug_level)
        logger.info("------------------------------------")

    # checks if config file exists and runs subroutines to either create new config file or to populate object
    def readFromConfigFile(self):
        logger.info("looking for config.ini file in "+self.CONFIG_FILE_PATH)
        if not os.path.isfile(self.CONFIG_FILE_PATH):
            configFileManager.__create_config()

        if os.path.isfile(self.CONFIG_FILE_PATH):
            logger.info("Configfile has been found, reading settings ...")
            try:
                configFileManager.__get_settings(self)
            except:
                logger.info("Failed to read configfile, delete file and restart script!")
                logger.info("Terminating script ... goodbye!")
                sys.exit()

      