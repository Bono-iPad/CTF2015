import telnetlib
import commands
import struct

host = 'catwestern_631d7907670909fc4df2defc13f2057c.quals.shallweplayaga.me'
port = 9999

tn = telnetlib.Telnet(host,port)
s = tn.get_socket()
rawdata = ""
while True:
  q = s.recv(1)
  rawdata = rawdata + q
  if q == "\xc3":
    break

print rawdata

data = rawdata[ rawdata.find("About to send ")+14:rawdata.find(" bytes")]

asm = rawdata[rawdata.find(" bytes") + 9:]
print "%r" % asm
print len(asm)
print data

while len(asm) < int(data):
  q = s.recv(1)
  asm = asm + q
  rawdata = rawdata + q

print len(asm)
print data

buf = ""
for a in range(0,len(asm)):
  buf = buf + "\tnop\n"

buf = "\t.intel_syntax noprefix\n\t.globl _start\n_start:\n" + buf

open("test.s","w").write(buf)
print commands.getoutput("rm a.out;gcc -nostdlib test.s")

data = open("./a.out","r").read()

data = data[:0xd4] + asm + data[0xd4+len(asm):]
open("./a.out","w").write(data)

buf = ""
data = rawdata[rawdata.find("rax="):rawdata.find("****Send")-1]

buf = "b *0x4000d4\n"
buf = buf + "r\n"

for a in data.split("\n"):
  q = a.split("=")
  buf = buf + "set $%s=%s\n" % (q[0],q[1])

buf = buf + "c\ni r\nq\n"
open("test.cmd","w").write(buf)

data = commands.getoutput("gdb ./a.out --command test.cmd")
print data

data2 = data[ data.rfind("in ?? ()")+9:]
print "%r" % data2

data = rawdata[rawdata.find("rax="):rawdata.find("****Send")-1]
buf = ""
for a in data.split("\n"):
  q = a.split("=")
  x = data2[ data2.find(q[0]):]
  x = x.split("\t")[0]
  x = x[x.rfind(" ")+1:]
  print x
  buf = buf + "%s=%s\n" % (q[0],x)

print buf
tn.write(buf+"\n")
print tn.read_until("none",2)

