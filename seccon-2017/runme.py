import sys
sys.setrecursionlimit(99999)
memoize = {}

def f(n):
    if n in memoize:
        return memoize[n]
    if n < 2:
        return n
    returnVal = f(n-2) + f(n-1)
    memoize[n] = returnVal
    return returnVal
print "SECCON{" + str(f(11011))[:32] + "}"

