from pwn import remote

def printLines(lines):
    print "Printing lines:"
    for l in lines:
        print l

def solveProblem1(input):
    lines = input.split(": ")
    input = lines[1]
    input = input.strip('[]')
    fields = input.split(", ", 2)
    newAlpha = fields[0]
    rot = int(fields[1])
    text = fields[2]
    plaintext = ""
    for c in text:
        plaintext = plaintext + convertChar(c, rot, newAlpha)
    print "this is the plaintext: " + plaintext
    return plaintext

def convertChar(c, r, newAlpha):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    idx = newAlpha.find(c)
    if idx == -1:
        return c
    return alphabet[(idx - r) % 26]

conn = remote('capoditutticapi01.3dsctf.org', 8001)
lines = conn.recvlines(10, timeout = 2)
printLines(lines)
conn.send('start')
lines = conn.recvlines(3, timeout = 1)
printLines(lines)
# someBytes = conn.recvn(20)

# print "Printing some bytes: " + someBytes
count = 0
while count < 9:
    print "Starting problem " + str(count)
    problem1 = lines[2]
    output = solveProblem1(problem1)
    conn.send(output)
    lines = conn.recvlines(3, timeout = 3)
    printLines(lines)
    count = count + 1
print "Starting final problem"
problem1 = lines[2]
output = solveProblem1(problem1)
conn.send(output)
conn.interactive()

