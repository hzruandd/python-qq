from socket import *

client=socket(AF_INET, SOCK_DGRAM)
client.settimeout(3)
client.sendto('Hello', ('61.144.238.145',8000))
try:
    data, address = client.recvfrom(1024)
except:
    print 'kk'
print data, ' ', address
client.close()
