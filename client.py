import socket
import time

UDP_IP_ADDRESS = "127.0.0.1"
UDP_PORT_NO = 8888


clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

timestamp = 11111010.0

while 1:
    Message = "{'HDF', "+str(timestamp)+", 1000000, 100, 100, 100}"
    #Message = "{'HDF', "+str(timestamp)+", 7425, 7687, 7687, 7637, 7951, 7813, 7732, 7894, 8573, 8660, 8224, 8780, 8918, 8863, 8837, 8451, 8526, 8931, 9029, 9101, 9322, 9314, 8993, 8681, 8363}"
    
    clientSock.sendto(Message.encode('utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))
    print(Message)

    Message = "{'EHZ', "+str(timestamp)+", 100, 9, 4, 100}"
    clientSock.sendto(Message.encode('utf-8'), (UDP_IP_ADDRESS, UDP_PORT_NO))

    print(Message)
    timestamp = timestamp + 0.5
    time.sleep(0.1)