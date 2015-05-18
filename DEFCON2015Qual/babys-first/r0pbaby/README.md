# r0pbaby
## Analysis and exploit
You can know the libc's base address, you can know the libc's system address and you can analyze libc's version by online database or something.
All you need is return to system with edi=libc's address of "/bin/sh". You can rewrite return address by sending "AAAAAAAA" +  return address. How easy! I read other writeups and all writeups used this approach. 
The binary is PIE, so using r0pbaby binary's gadget is just troublesome and needless. But my solution is not so smart. I did use the r0pbaby binary's gadget.

If PIE binary's address was leaked, you can tell the libc's address. This phenomenon is Known as "Offset2lib"(http://cybersecurity.upv.es/attacks/offset2lib/offset2lib.html).
And vice versa. You can tell the PIE binary's address when the libc's address was leaked.
So you can use binary's gadget just only you know the libc's address.

My solution is very, very roundabout as below:

    1. get libc's base address and libc's "system" and "read" address.
    2. use __libc_csu_init function to set $rdx,$rsi and dummy $rdi(pass to alarm)
    3. call alarm($rdi) to pass through call [r12+rbx*8]. $rdi, $rsi, $rdx are not changed.
    4. use binary's 0xf23 gadget(pop rdi;ret) to set $rdi=0
    5. call read(0, r0pbaby's writable address, 8) and read "/bin/sh\x00"
    6. set binary's 0xf23 gadget(pop rdi;ret) to set $rdi=address of "/bin/sh\x00"
    7. call system

Anyway, I solved this problem in this way.

https://github.com/Bono-iPad/CTF2015/blob/master/DEFCON2015Qual/babys-first/r0pbaby/r0pbaby.py
