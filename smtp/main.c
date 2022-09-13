#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int connect_smtp(const char *host, int port);
void send_smtp(int sock, const char *msg, char *resp, size_t len);
char *read_msg(char *file_path);

/*
  Use the provided 'connect_smtp' and 'send_smtp' functions
  to connect to the "lunar.open.sice.indian.edu" smtp relay
  and send the commands to write emails as described in the
  assignment wiki. 
 */
int main(int argc, char *argv[])
{
  if (argc != 3)
  {
    printf("Invalid arguments - %s <email-to> <email-filepath>", argv[0]);
    return -1;
  }

  char *rcpt = argv[1];
  char *filepath = argv[2];
 
  
  char response[4096];
  char sender[100] = "MAIL FROM:";
  char recipient[100] = "RCPT TO:";

  strcat(sender, rcpt);
  strcat(recipient, rcpt);
  strcat(sender, "\n");
  strcat(recipient, "\n");

 

  int sock = connect_smtp("lunar.open.sice.indiana.edu", 25);

  send_smtp(sock, "HELO iu.edu\n", response, 4096);
  printf("%s\n",response);
  send_smtp(sock, sender, response, 4096);
  printf("%s\n",response);
  send_smtp(sock, recipient, response, 4096);
  printf("%s\n",response);
  send_smtp(sock, "DATA\n", response, 4096);
  printf("%s\n",response);
  char *message = read_msg(filepath);

  if (message == NULL)
  {
     printf("Cannot open file\n");
     return 1;
   }
   else
   {
    
    strcat(message, " \r\n.\r\n");
    send_smtp(sock, message, response, 4096);
    printf("%s\n",response);
   }
   free(message);
 

  return 0;
  
}


char *read_msg(char *file_path)//reads the contents of a file into a string.
{
  char ch;
  FILE *ptr;

  ptr = fopen(file_path, "r");

 if (ptr == NULL) 
  {
  return NULL;
  }
   // move the pointer to the end of the file.
   fseek(ptr, 0, SEEK_END);
   // ftell gives us the current position of the file pointer which is used to find out the total number of characters in the file.
   int size = ftell(ptr); 
   //move the pointer back to the first character of the file
   fseek(ptr, 0, SEEK_SET);

  
  char *content = malloc(sizeof(char) * (size+1));

  int nxt_ch = 0;
  while ( (ch = fgetc(ptr)) != EOF)//reading each character till the end of file is reached.
   {
    content[nxt_ch] = ch;
    nxt_ch++;
  }
  content[nxt_ch] = '\0';
  fclose(ptr);
  return content;
 }
//Reference: Portfolio Courses-Read All File Contents Into A String.
//https://www.youtube.com/watch?v=CzAgM5bez-g.
