import telnetlib

host = 'mathwhiz_c951d46fed68687ad93a84e702800b7a.quals.shallweplayaga.me'
port = 21249

t = ["ZERO","ONE","TWO","THREE","FOUR","FIVE","SIX","SEVEN","EIGHT","NINE","TEN"]

#host = 'localhost'
#port = 1234
tn = telnetlib.Telnet(host,port)
no = 0
while True:
 no = no + 1
 print "Round", no
 data = tn.read_until("=",1)
 print data

 data = data.upper()
 for a in range(0,10):
   data = data.replace(t[a],str(a))

 data = data.replace("[","(")
 data = data.replace("]",")")
 data = data.replace("{","(")
 data = data.replace("}",")")
 data = data.replace("^","**")
 ans = eval(data[:-2])
 print ans
 tn.write(str(ans) + "\n")
