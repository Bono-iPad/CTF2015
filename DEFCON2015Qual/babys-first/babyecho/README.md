# babyecho
## Problem
babyecho_eb11fdf6e40236b1a37b7974c53b6c3d.quals.shallweplayaga.me:3232
[Download](http://downloads.notmalware.ru/babyecho_eb11fdf6e40236b1a37b7974c53b6c3d)

## Analysis
To make a long story short, this is the binary that do like this:

    while(1){
    printf("Reading %d bytes\n",$esp+0x10)
    for(a=0;a<$esp+0x10;a++)read(0,$esp+0x1c+a,1)
    printf($esp+0x1c) # This printf return to $esp-0x4
    }

Yet another format string bug. You can get $esp+0x1c when you send "%5$x".
Just change the $esp+0x10 and write (padding + shellcode) to $esp+0x1c, rewrite the return address at $esp-0x4 and return to your shellcode.
Rewriting $esp-0x4 broke your shellcode on the stack if you don't add padding before the shellcode.
## Exploit
https://github.com/Bono-iPad/CTF2015/blob/master/DEFCON2015Qual/babys-first/babyecho/babyecho.py
