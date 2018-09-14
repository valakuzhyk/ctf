import pwn

conn = pwn.ssh("lotto", "pwnable.kr", 2222, password="guest")
line = conn.recvline(timeout=1)
print line