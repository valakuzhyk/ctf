import sys
def _l(idx, s):
    return s[idx:] + s[:idx]
s = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz_{}"
t = [[_l((i+j) % len(s), s) for j in range(len(s))] for i in range(len(s))]



def main(p, k1, k2):
    i1 = 0
    i2 = 0
    c = ""
    for a in p:
        c += t[s.find(a)][s.find(k1[i1])][s.find(k2[i2])]
        i1 = (i1 + 1) % len(k1)
        i2 = (i2 + 1) % len(k2)
    return c


def findVal(lists, goalChar):
    return lists[0].find(goalChar)



knownString = "SECCON{**************************} **************"

def invMain(c):
    i1 = 0
    i2 = 0
    i = 0
    jVals = [0] * 7
    decodedString = ""
    for b in c:
        if knownString[i] != "*":
            a = knownString[i]
            listOfStrings = t[s.find(a)]
            jVals[i%7] = findVal(listOfStrings, b)
            print jVals[i%7]
            print " We know that inputing " + a + " in the " +str(i) + "spot results in " + t[s.find(a)][jVals[i%7]][0]
        j = -1
        if (i%14) >= 7:
            j = jVals[14 - (i%14)-1]
        else:
            j = jVals[i%14]
            
        string = t[j][0]
        print "encoded: " + t[s.find(a)][j][0]
        print "decoded: " + s[string.find(b)]
        decodedString += s[string.find(b)]
        i = i + 1
    print decodedString

if len(sys.argv[2]) != 14:
    print "Length isn't 14. Try again"
    quit()
c = main(sys.argv[1], sys.argv[2], sys.argv[2][::-1])
print "encoded value is " + c
print invMain("POR4dnyTLHBfwbxAAZhe}}ocZR3Cxcftw9")



