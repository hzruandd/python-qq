from socket import *
server=socket(AF_INET, SOCK_DGRAM)
server.bind(('localhost',8888))
data, address = server.recvfrom(1024)
print data, ' ', address
server.sendto('Hi', address)
server.close()