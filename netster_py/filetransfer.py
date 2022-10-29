from typing import BinaryIO
import socket



def file_client(host:str, port:int, use_udp:bool, fp:BinaryIO) -> None:
       
        # reused code from Assignment 4
        # references:
        # https://realpython.com/read-write-files-python/
        #UDP Client
        if use_udp== True:
            u_add=socket.getaddrinfo(host, port)
            ua= u_add[0]
            ip_port = ua[4]
            udp_client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            print("Hello, I am a client")
            
            while True:
                u_clientdata = fp.read(256)
                udp_client.sendto(u_clientdata,ip_port)
                if not u_clientdata: 
                    break
                
            fp.close()
            udp_client.close()
          
        #TCP Client
        else:

            tadd=socket.getaddrinfo(host, port)
            ta= tadd[0]
            ip_port = ta[4]
            tcp_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            tcp_client.connect(ip_port)
            print("Hello, I am a client")

            t_clientdata = fp.read(256)
            while t_clientdata:
                tcp_client.send(t_clientdata)
                t_clientdata = fp.read(256)

        
            tcp_client.close()
            fp.close()
        

def file_server(iface:str, port:int, use_udp:bool, fp:BinaryIO) -> None:
     
     #UDP server
     if use_udp ==True:
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_add=socket.getaddrinfo(iface, port)
        u_ip= udp_add[0]
        udp_sock.bind(u_ip[4])
        print("Hello, I am a server")
        while True:
            u_message,udp_addr = udp_sock.recvfrom(256)
            if u_message:
                fp.write(u_message)
                
            else: #if server receives a 0-byte message
                fp.close()
                udp_sock.close()
                break
               
            
        
            
    #TCP server        
     else:

        t_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_add = socket.getaddrinfo(iface, port)
        t_ip = tcp_add[0]
        t_sock.bind(t_ip[4]) 
        t_sock.listen()
        print("Hello, I am a server")
        sockobj, address = t_sock.accept()
        while True:
          
            file_data = sockobj.recv(256)
            if file_data:
                fp.write(file_data)
                
            else:
               fp.close()
               sockobj.close()
               break
           
                    

          
       

