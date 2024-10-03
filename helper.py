#!/usr/bin/python3
import configparser
import os.path
import sys


CONFIG_FILENAME = 'config.ini'

class runtimesystem:
    os_name = ""
    serial_baudrate = 0
    serial_port = ""
    udp_ip_adress = ""
    udp_port_no = 0
    serial_coms_enabled = False
    debug_file_path = "test2"
    file_logger_debug_level = ""
    terminal_logger_debug_level = ""

    # creates new config file with default values
    def __create_config():
        print("Configfile does not exist, creating file in working directory ...")

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
            'filepath': 'debug_file.txt',
            'file_logger_debug_level': 'info',
            'terminal_logger_debug_level': 'info'}

        # Write the configuration to a file
        try:
            with open(CONFIG_FILENAME, 'w') as configfile:
                config.write(configfile)
        except:
            print("Configfile could not be created!")
            print('Linux needs absolute paths: -> "/home/myshake/script/debug_log.txt"')
            print("If you run into trouble, copy the full filepath into the CONFIG_FILENAME variable in this script")
            print("Terminating script ....")
            sys.exit()

        print('Configfile "'+ CONFIG_FILENAME +'" has been created')
        print("Script needs to be restarted bevore new settings are activated")
        print("Terminating script ... goodbye!")
        sys.exit()

    # writes contents of the config file to object
    def __get_settings(self):
        config = configparser.ConfigParser()
        config.read(CONFIG_FILENAME)

        self.os_name = config.get('General','os_name')
        self.serial_baudrate = config.getint('Serial_Communication','baudrate')
        self.serial_port = config.get('Serial_Communication','port')
        self.serial_coms_enabled = config.getboolean('Serial_Communication','enabled')

        self.udp_ip_adress = config.get('UDP_Communication', 'ip_adress')
        self.udp_port_no = config.getint('UDP_Communication', 'port_numnber')

        self.debug_file_path = config.get('Logging', 'filepath')
        self.file_logger_debug_level = config.get('Logging', 'file_logger_debug_level')
        self.terminal_logger_debug_level = config.get('Logging', 'terminal_logger_debug_level')

    # prints all the availible public variable data for the communication
    def print_info(self):
        print("------------ Settings ------------")
        print("# Operatingsystem: "+self.os_name)
        print("# Serial Communication:")
        print("- Baudrate: "+str(self.serial_baudrate))
        print("- Serialport: "+self.serial_port)
        print("- enabled: "+str(self.serial_coms_enabled))
        print("# UDP-Communication:")
        print("- IP-Adress: "+self.udp_ip_adress)
        print("- Portnumber: "+str(self.udp_port_no))
        print("# Logging")
        print("- file path: "+ self.debug_file_path)
        print("- file logger level: "+ self.file_logger_debug_level)
        print("- terminal logger level: "+ self.terminal_logger_debug_level)
        print("------------------------------------")

    # checks if config file exists and runs subroutines to either create new config file or to populate object
    def readFromConfigFile(self):
        if not os.path.isfile(CONFIG_FILENAME):
            runtimesystem.__create_config()

        if os.path.isfile(CONFIG_FILENAME):
            print("Configfile has been found, reading settings ...")
            try:
                runtimesystem.__get_settings(self)
            except:
                print("Failed to read configfile, delete file and restart script!")
                print("Terminating script ... goodbye!")
                sys.exit()



                