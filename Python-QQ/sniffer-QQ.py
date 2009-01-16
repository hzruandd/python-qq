import pcap ,struct 
pack=pcap.pcap() 
pack.setfilter('udp') 
for recv_time,recv_data in pack: 
   recv_len=len(recv_data) 
   if recv_len==55 and recv_data[42]==chr(02) and recv_data[54]==chr(03): 
           print struct.unpack('>I',recv_data[recv_len-6:recv_len-2])[0] 