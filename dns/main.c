#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>

/*
  Use the `getaddrinfo` and `inet_ntop` functions to convert a string host and
  integer port into a string dotted ip address and port.
 */

//referred to the linux manual page for the getaddrinfo and inet_ntop function definitions.
int getaddrinfo(const char *restrict host, const char *restrict port, const struct addrinfo *restrict hints, struct addrinfo **restrict res);
const char *inet_ntop(int af, const void *restrict src, char *restrict dst, socklen_t size);
int main(int argc, char *argv[])
{
  if (argc != 3)
  {
    printf("Invalid arguments - %s <host> <port>", argv[0]);
    return -1;
  }
  
  char *host = argv[1];
  long port = atoi(argv[2]);
  char service[200];
  char buffer1[INET_ADDRSTRLEN];// to store the IPv4 addresses
  char buffer2[INET6_ADDRSTRLEN];// to store the IPv6 addresses
  struct addrinfo hints;
  struct addrinfo *res;
  struct addrinfo *address;

  sprintf(service, "%ld", port);// to convert port from long to string
  memset(&hints, 0, sizeof(hints));
  //as specified in the assignment instructions.
  hints.ai_family = PF_UNSPEC;
  hints.ai_socktype = SOCK_STREAM;
  hints.ai_protocol = IPPROTO_TCP;
  hints.ai_flags = AI_PASSIVE;

  
  getaddrinfo(host, service, &hints, &res);
  
 
  //iterating over the linked list.
  address=res;
  while(address!=NULL)
  {
    char v4_Addr[10] = "IPv4";
    char v6_Addr[10] = "IPv6";
    //this block of code is taken from the assignment instruction page-https://github.iu.edu/SICE-Networks/Net-Fall22/wiki/03_DNS.
    void *raw_addr;
    //AF_INET indicates that the address is IPv4
    if (address->ai_family == AF_INET)
    {                                                             
      struct sockaddr_in *tmp = (struct sockaddr_in *)address->ai_addr; 
      raw_addr = &(tmp->sin_addr);                                
      inet_ntop(address->ai_family, raw_addr, buffer1, sizeof(buffer1));// calling the inet_ntop() to convert the numeric address to a string.
      
      strcat(v4_Addr," ");
      printf("%s", v4_Addr);
      printf("%s\n", buffer1);
      
    }
    else
    {                                                               
      struct sockaddr_in6 *tmp = (struct sockaddr_in6 *)address->ai_addr; 
      raw_addr = &(tmp->sin6_addr);                                
      inet_ntop(address->ai_family, raw_addr, buffer2, sizeof(buffer2));

      strcat(v6_Addr," ");
      printf("%s", v6_Addr);
      printf("%s\n", buffer2);
    }
  
  address = address->ai_next;

  }

  return 0;
}
