import socket
import threading
import os
f= "utf-8"
# references:
# https://realpython.com/python-sockets/#background
# Multithreaded Client Server in Python -https://www.youtube.com/watch?v=xceTFWy_eag

def chat_server(iface:str, port:int, use_udp:bool) -> None:
    # handles multithreading
    def multiplethreads(connectobj,add,c, getadd): 
        print(f"connection {c} from {getadd}")
        
        # runs until a 'goodbye' or 'exit' is encountered
        while True:
            t_message = connectobj.recv(256).decode(f)
            print(f"got message from {getadd}")
            if t_message == "hello\n": 
                connectobj.send("world\n".encode(f))
            elif t_message == "goodbye\n":
                connectobj.send("farewell\n".encode(f))
                break
            elif t_message== "exit\n":
                connectobj.send("ok\n".encode(f))
                t_sock.close()
                os._exit(0)
            else:
                t_message = t_message+"\n"
                connectobj.send(t_message.encode(f))
                
        
        
        connectobj.close()
        
   # UDP SERVER
    if use_udp ==True:
        udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # converts hostname to IP address and returns a list
        udp_add=socket.getaddrinfo(iface, port)
        
        u_ip= udp_add[0]
        # the (IP adress, port) is the last element of the list[][]
        udp_sock.bind(u_ip[4])
        print("Hello, I am a server")
        # runs until a 'goodbye' or 'exit' is encountered
        while True:
            u_message, udp_addr = udp_sock.recvfrom(256)
            print(f"got message from {udp_addr}")
            u_message = u_message.decode(f)
            if u_message == "hello\n":
                udp_sock.sendto("world\n".encode(f), udp_addr)
            elif u_message == "goodbye\n":
                udp_sock.sendto("farewell\n".encode(f), udp_addr)
            elif u_message == "exit\n":
                udp_sock.sendto("ok\n".encode(f), udp_addr)
                break
            else:
                u_message = u_message+"\n"
                udp_sock.sendto(u_message.encode(f), udp_addr)
        udp_sock.close()

    # TCP SERVER
    else:
        
        t_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_add = socket.getaddrinfo(iface, port)
        t_ip = tcp_add[0]
     
    
        
        t_sock.bind(t_ip[4]) 
        
        t_sock.listen()

        
        print("Hello, I am a server")
        # to keep count of the number of connections for a server
        c = -1

        while True:
            sockobj, address = t_sock.accept()
            c += 1
            thread = threading.Thread(target = multiplethreads,args=(sockobj, address,c,t_ip[4]))
            thread.start()
    

    


def chat_client(host:str, port:int, use_udp:bool) -> None:

   # UDP CLIENT
    if use_udp ==True:
        u_add=socket.getaddrinfo(host, port)
        ua= u_add[0]
        ip_port = ua[4]
        udp_client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        print("Hello, I am a client")
        while True:
            udp_msg = input("")
            # appending a "\n" because the if condition in the  server checks for "hello\n"
            udp_msg = udp_msg +"\n"
            udp_client.sendto(udp_msg.encode(),ip_port)
        
            P_msg,a = udp_client.recvfrom(256)
            servermsg = P_msg.decode(f)
            print(servermsg)
            if servermsg == "farewell\n":
                break
            if servermsg == "ok\n":
                break
        # the client closes if either a  farewell or ok is returned from the server
        udp_client.close()
    
    # TCP CLIENT
    else:
        tadd=socket.getaddrinfo(host, port)
        ta= tadd[0]
        ip_port = ta[4]
        tcp_client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        tcp_client.connect(ip_port)
        
        print("Hello, I am a client")
        
        while True:
            t_msg = input("")
            t_msg = t_msg + "\n"
            tcp_client.send(t_msg.encode(f))
        
            P_msg = tcp_client.recv(256).decode(f)
            print(P_msg)
            if P_msg == "farewell\n":
                break
            if P_msg == "ok\n":
                break
        tcp_client.close()


                