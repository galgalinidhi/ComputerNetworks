from typing import BinaryIO
import socket
import struct
initial_window_size = 3
pck_seq =0
pck_start = 0 
current_seq = 0
count_message = 0
packet_buffer =[]

# my previous submission on autograder did not have congestion control and comments.
def gbn_server(iface:str, port:int, fp:BinaryIO) -> None:
    global count_message
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
           
            # print("Sent ACK for",count_message)
            count_message += 1
            if u_message:
                #print(u_message)
                fp.write(u_message)
                #if the message received< 248 it's because it's the last message.
                if len(u_message) < 248 :
                    fp.close()
                    udp_sock.close()
                    break
               
                

def gbn_client(host:str, port:int, fp:BinaryIO) -> None:
    global initial_window_size, pck_seq, pck_start, current_seq, packet_buffer
    
    u_add=socket.getaddrinfo(host, port)
    ua= u_add[0]
    ip_port = ua[4]
    udp_client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    print("Hello, I am a client")
    
    #reading the file contents into packet_buffer[]  
    while True:
        
        #total packet size = 248 + 8(header)
        u_clientdata = fp.read(248)
        if not u_clientdata:
            break
        else:
            
            #print(len(u_clientdata))
            #https://docs.python.org/3/library/struct.html
            header= struct.pack("!II", pck_seq, len(u_clientdata))
            packet = header + u_clientdata
            packet_buffer.append(packet)
            pck_seq+=1
            
        
    pck_total = len(packet_buffer)
    #print("total packets", pck_total)
  
    window_size = initial_window_size
    while pck_start < pck_total:
        
        #check if current pack is within the window size
        while current_seq < pck_start + window_size:
            #print(window_size)  
            if current_seq<pck_total:
                udp_client.sendto(packet_buffer[current_seq],ip_port)
                #print("sent packet",current_seq)
                current_seq+=1
 

            #https://www.adamsmith.haus/python/answers/how-to-set-a-timeout-on-a-socket-receiving-data-in-python
                udp_client.settimeout(0.04)
                try:
                   
                    server_pack,udp_addr = udp_client.recvfrom(256)
                    server_header = server_pack[0:8]
                    server_message = server_pack[8:]
                    seq_recv, len_recv = struct.unpack("!II", server_header)
                    #receives the sequence number from server. both the numbers are same ACK is received for that sequence number
                   
                    #pck_start points to the packet currently waiting for acknowledgement.
                    if seq_recv == pck_start:
                      
                        # the pck_start is acknowledged so move pointer to the next packet.
                        pck_start+=1
                        # if the packets are successfully acknowledged,increase the window size by 1
                        window_size = window_size + 1
                        continue
                        
                        
                #if pck_start == current_seq:         
                except socket.timeout as e :
                    # acknowledgement is not received for pck_start.So,reset the current_seq number to pck_start for retransmission. 
                    current_seq = pck_start
                    # if acknowledgement is not received, set window_size to minimum.
                    window_size = min(initial_window_size, pck_total-pck_start)
                    continue
            else:
                break
                    
    fp.close()
    udp_client.close()
