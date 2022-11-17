from typing import BinaryIO
import socket
import struct
packet_size = 6
def stopandwait_server(iface:str, port:int, fp:BinaryIO) -> None:
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_add = socket.getaddrinfo(iface, port)
    u_ip = udp_add[0]
    udp_sock.bind(u_ip[4])
    # count_message keeps track of the number of messages received
    count_message = 0
    print("Hello, I am a server")
    while True:
        udp_pack,udp_addr = udp_sock.recvfrom(256)
        #the first 8 bytes has the header
        header = udp_pack[0:8]
        u_message = udp_pack[8:]
        seq_sent, len_sent = struct.unpack("!II", header)
        # if the message seq from client matches the message count of the server, it means there are no duplicates
        if  seq_sent == count_message:
            header= struct.pack("!II", count_message, len(u_message))
            packet = header + b''
            udp_sock.sendto(packet,udp_addr)
            # server_seq = str(count_message).encode('utf-8')
            # udp_sock.sendto(server_seq,u_ip[4]) 
            # print("Sent ACK for",count_message)
            count_message+=1
            if u_message:
                fp.write(u_message)
                
            else: #if server receives a 0-byte message
                fp.close()
                udp_sock.close()
                break
               

def stopandwait_client(host:str, port:int, fp:BinaryIO) -> None:
    seqnum =0
    u_add=socket.getaddrinfo(host, port)
    ua= u_add[0]
    ip_port = ua[4]
    udp_client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    print("Hello, I am a client")
    

    while True:
         #total packet size = 248 + 8(header)
        u_clientdata = fp.read(248)
        while True:
            #https://docs.python.org/3/library/struct.html
            header= struct.pack("!II", seqnum, len(u_clientdata))
            packet = header + u_clientdata
            udp_client.sendto(packet,ip_port)
            #considering 60ms because sending and receiving to and from client takes 25ms each.So the total time spent on packet transmission>=50ms

            #https://www.adamsmith.haus/python/answers/how-to-set-a-timeout-on-a-socket-receiving-data-in-python
            udp_client.settimeout(0.06)
            try:
                server_pack,udp_addr = udp_client.recvfrom(256)
                server_header = server_pack[0:8]
                server_message = server_pack[8:]
                seq_recv, len_recv = struct.unpack("!II", server_header)
                #receives the sequence number from server. both the numbers are same ACK is received for that sequence number
                # ack = udp_client.recvfrom(256)
                # recv_ack = ack.decode('utf-8')
                if seq_recv == seqnum:
                    seqnum+=1
                    
                    break
                
            except socket.timeout :
                continue
        
            
        
        if not u_clientdata: 
            break
        
        
                
    fp.close()
    udp_client.close()