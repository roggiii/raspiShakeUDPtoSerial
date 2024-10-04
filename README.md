# Raspberryshake UDP-stream to serial connection
Takes the UDP datastream from the raspberry shake client and outputs it on a serial connection.
Helpful when the shake needs to be operated in remote areas where no internet connection is availible but the data should be analysed for threats.

### useful links:
- https://manual.raspberryshake.org/udp.html
- https://community.raspberryshake.org/c/tech-support/34

# Commands
- watch script output: `tail -f ~/script/debug_log.txt`
- list all processes containing "python": `ps -ef | grep python`
- kill running script: `pkill -9 -f server.py`
- start script: `~/script/./server.py &`
- edit script: `nano ~/script/server.py`
- @reboot cronjob testen ohne Pi neuzustarten:
   `sudo rm /var/run/crond.reboot`
   `sudo service cron restart`

# Files
- **server.py** main programm loop
- **client.py** provides dummy shake data to configurable UDP port for testing purposes
- **config.ino** config file for the serial and udp communication parameters

# Setup
Description of the steps to take when to operate shake offline and analyse the data locally.
## Packages
1. Connect Pi to the internet.
   - Goto http://rs.local/ if you want to setup with wifi
3. update:
   - `sudo apt-get --allow-releaseinfo-change update`
   - `sudo apt-get update && apt-get upgrade`
4. Install Packages:
   --timeout 100 is neccecary when there is a bad internet connection
   - `sudo apt install python3-pip`
   - `pip3 install --upgrade pip --timeout 100`
   - `pip3 install cmake --timeout 100 --no-cache-dir`
   - `pip3 install numpy --timeout 100 --no-cache-dir`
   - `pip3 uninstall serial`
   - `pip3 install pyserial`
  5. Start script on reboot:
     - edit cronjob with the following command:
       `EDITOR=nano crontab -e`
     - paste and save this line into cronfile:
       `@reboot /usr/bin/python3 /home/myshake/script/./server.py`
  6. Set file permissions:
     - `chmod +x ~/script/server.py`
## Datacast and static IP
1. Goto http://rs.local/
2. Set Datacast and static IP to: ??



