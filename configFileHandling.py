#!/usr/bin/python3

import configparser
import os.path
import sys

FILENAME = 'config.ini'

def create_config():

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
        'debug': True,
        'log_level': 'info'}

    # Write the configuration to a file
    try:
        with open(FILENAME, 'w') as configfile:
            config.write(configfile)
    except:
        print("Configfile could not be created!")
        print("Terminating script ....")
        sys.exit()

    print('Configfile "'+ FILENAME +'" has been created')
    print("Script needs to be restarted bevore new settings are activated")
    print("Terminating script ... goodbye!")
    sys.exit()

def get_setting():
    config = configparser.ConfigParser()
    config.read(FILENAME)
    os = config.get('General','os_name')
    print("Operatingsystem: "+os)


if not os.path.isfile('config.ini'):
    create_config()

if os.path.isfile('config.ini'):
    print("Configfile hase been found, reading settings ...")
    try:
        get_setting()
    except:
        print("Configfile corrupted, please delete file and restart script!")
        print("Terminating script ... goodbye!")
        sys.exit()
