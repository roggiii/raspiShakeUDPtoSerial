# Raspberryshake UDP-stream to serial connection
Takes the UDP datastream from the raspberry shake client and outputs it on a serial connection.
Helpful when the shake needs to be operated in remote areas where no internet connection is availible but the data should be analysed for threats.

# Useful stuff:
## Links:
- https://manual.raspberryshake.org/udp.html
- https://community.raspberryshake.org/c/tech-support/34

## Establish remote connection:
It is possible to edit the code remotly over ssh on the shake via [VS-Code](https://code.visualstudio.com/docs/remote/ssh).

When wanting to copy/delete files from shake use [WinSCP](https://winscp.net/eng/download.php).

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

## Setup serial port
Serial port needs to be configured so that the COM-port-number wont change on reboot. This is to be done with a u-dev-rule. [Source](https://unix.stackexchange.com/questions/66901/how-to-bind-usb-device-under-a-static-name)

1. find devices that report as usb-to-serial-adapters: `dmesg | grep tty`
   - take note of the name os your device, usually named something like **ttyUSBx** (x is a number)
2. list all the attribtes from the device: `udevadm info --name=/dev/ttyUSB0 --attribute-walk`
   - Every USB-device has attributes by which the operating system can differentiate between them
   - the goal ist to find an attribute that is unique to this device and map it permanently to a COM-port
   - these attributes work: `ATTRS{idProduct}=="0002"` `ATTRS{idVendor}=="1d6b"`
3. Create new rule file: `sudo nano /etc/udev/rules.d/99-usb-serial.rules` and put the choosen attributes as rules into it: `SUBSYSTEM=="tty", ATTRS{idVendor}=="1d6b", ATTRS{idProduct}=="0002", SYMLINK+="my_serial"`
   - now every usb-device with these attributes reports as com-port "my_serial"
4. Refrehs rules: `sudo udevadm trigger`
5. Verify rule change: `ls -l /dev/my_serial`
   - shows what tty number the syslink went to
6. Test rule change: `udevadm test -a -p  $(udevadm info -q path -n /dev/my_serial)`

## Set offline mode
Connect via ssh and enter the following command: `rsh-stand-alone ON` and confirm with `YES`

## Configure Shake to write logs to usb-drive
Follow instructions on [Raspberryshake.org](https://manual.raspberryshake.org/usbsds.html#usbsds)





