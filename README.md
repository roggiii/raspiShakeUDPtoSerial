# Raspberryshake UDP-stream to serial connection
Takes the UDP datastream from the raspberry shake client and outputs it on a serial connection.
Helpful when the shake needs to be operated in remote areas where no internet connection is availible but the data should be analysed for threads.

## server.py:
main script that takes udp output and pipes it to serial port

## client.py:
test script to simulate raspy shake on localport

### useful links:
- https://manual.raspberryshake.org/udp.html
- https://community.raspberryshake.org/c/tech-support/34
