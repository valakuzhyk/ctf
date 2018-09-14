vals = dict()

def paren(n):
    if n == 2 or n == 0:
        return 1
    if n in vals:
        return vals[n]

    sum = 0
    for i in range(0, n, 2):
        sum = sum + paren(n - 2 - i) * paren(i)
    sum = sum % 100
    vals[n] = sum
    return sum
print paren(6)
print paren(10)
paren(1000)
print 1000
paren(2000)
print 2000
paren(3000)
print 3000
paren(4000)
print 4000
paren(5000)
print 5000
paren(6000)
print 6000
paren(7000)
print 7000
paren(8000)
print 8000
paren(9000)
print paren(10000) % 1000