#include <stdio.h>
#include <string.h>

void send_http(char* host, char* msg, char* resp, size_t len);


/*
  Implement a program that takes a host, verb, and path and
  prints the contents of the response from the request
  represented by that request.
 */
int main(int argc, char* argv[]) {
  if (argc != 4) {
    printf("Invalid arguments - %s <host> <GET|POST> <path>\n", argv[0]);
    return -1;
  }
  char* host = argv[1];
  char* verb = argv[2];
  char* path = argv[3];
  char response[4096];
  char* space = " ";
  

strcat(verb,space);
strcat(verb,path);
strcat(verb,space);
strcat(verb,"HTTP/1.0\r\nHost: ");
strcat(verb,host);
strcat(verb,"\r\n\r\n");
// Concatenation of verb,path and a Host header(as suggested in the Canvas discussion)
 
//printf("%s\n", verb);
 send_http(host,verb,response,4096);
 printf("%s", response);
  return 0;
}
