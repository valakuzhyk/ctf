from pwn import remote
import Queue

def printLines(lines):
    print "Printing lines:"
    for l in lines:
        print l

def TrimProblem(problemDef):
    # Remove nodes that don't do anything
    nodesToRemove = []
    for start, ends in problemDef["corridors"].iteritems():
        if len(ends) == 1:
            if start not in problemDef["keys"] and start != problemDef["SP"] and start != problemDef["EP"]:
                nodesToRemove.append(start)
    for node in nodesToRemove:
        print "removing node: " + node
        end = problemDef["corridors"].pop(node)
        problemDef["corridors"][end[0]].remove(node)
    if len(nodesToRemove) > 0:
        return TrimProblem(problemDef)
    return problemDef

def haveKey(heldKeys, door):
    for keySet in heldKeys:
        for key in keySet:
            if key.upper() == door:
                return True
    return False

def keysHad(heldKeys):
    allKeys = set()
    for keySet in heldKeys:
        for key in keySet:
            allKeys.add(key)
    return allKeys

def CanPassThrough(room, heldKeys, doors):
    #Does this room need a key
    if room not in doors:
        return True
    for door in doors[room]:
        # Do we have the key for this door
        if not haveKey(heldKeys, door):
            return False
    return True

def beenHereBefore(room, pathSoFar, keysSoFar):
    if room not in pathSoFar:
        return False
    # Even if you have been here before, have you added some keys to your belt.
    a = []
    idx = pathSoFar.index(room)
    for i in xrange(len(pathSoFar)-1, -1, -1):
        node = pathSoFar[i]
        if room == node:
            return True

        if len(keysSoFar[i]) != 0:
            return False
    print "I literally  have been here before " + str(room)
    print "Error in code" 
    exit()

def seenKeyBefore(key, keysSoFar):
    for keySet in keysSoFar:
        if key in keySet:
            return True
    return False

def FindPathTo(end, corridors, doors, pathSoFar, keysSoFar, keys, finishedNodes):
    if len(pathSoFar) > 200:
        print "Something bad happened"
        exit() 
    start = pathSoFar[-1]
    if start not in corridors:
        return None
    nextSteps = corridors[start]

    # Check whether being here allows us to pick up a key
    newKeys = []
    newKeysSoFar = keysSoFar + [[]]
    if start in keys:
        newKeys = keys[start]
        for key in newKeys:
            if not seenKeyBefore(key, keysSoFar):
                newKeysSoFar[-1] = keys[start]

    shortestPath = [0] * 100

    # TODO prefer going to a node that picks up a key over the shortest path.
    # if this approach doesn't already work.
    for step in nextSteps:
        if DEBUG:
            print "Printing state"
            print "  Looking at step " + step
            print "  I have already been to " + str(pathSoFar)
            print "  I have picked up keys " + str(newKeysSoFar)
        # Check if we can step here
        if not CanPassThrough(step, newKeysSoFar, doors):
            # print "    Can't pass"
            continue
        # if the node has already been seen in path and 
        # the keys held are the same, don't walk back here.
        if beenHereBefore(step, pathSoFar, newKeysSoFar):
            # print "    been here before"
            continue
        if step in finishedNodes and finishedNodes[step][0].issuperset(keysHad(newKeysSoFar)) and finishedNodes[step][1] < len(pathSoFar):
            # print "    finished node"
            continue

        if step == end:
            # print "    GOT TO THE END!!!"
            return pathSoFar + [step]

        stepPath = FindPathTo(end, corridors, doors, pathSoFar + [step], newKeysSoFar, keys, finishedNodes)
        if stepPath == None: # no path exists
            # print "    No path exists"
            continue
        if len(shortestPath) > len(stepPath): # this is a shorter path
            shortestPath = stepPath
    # After you have finished looking at a node, there is no point looking at it again until
    # you have gained another key
    finishedNodes[start] = (keysHad(newKeysSoFar), len(pathSoFar))
    if len(shortestPath) != 100:
        return shortestPath

def FindPathToBFS(end, corridors, doors, pathSoFar, keysSoFar, keys, finishedNodes):
    queue = Queue.Queue()
    queue.put((end, corridors, doors, pathSoFar, keysSoFar, keys, finishedNodes))
    while not queue.empty():
        (end, corridors, doors, pathSoFar, keysSoFar, keys, finishedNodes) = queue.get()
        # Since we removed end nodes, there should always be a place to go
        start = pathSoFar[-1]
        nextSteps = corridors[start]

        # Check whether being here allows us to pick up a key
        newKeysSoFar = keysSoFar + [[]]
        if start in keys:
            newKeys = keys[start]
            if not seenKeyBefore(newKeys[0], keysSoFar):
                    newKeysSoFar[-1] = keys[start]
        
        for step in nextSteps:
            # Pre process this step to ensure that it makes sense to go here
            if DEBUG:
                print "Printing state"
                print "  Looking at step " + step
                print "  I have already been to " + str(pathSoFar)
                print "  I have picked up keys " + str(newKeysSoFar)
            # Check if we can step here
            if not CanPassThrough(step, newKeysSoFar, doors):
                # print "    Can't pass"
                continue
            # if the node has already been seen in path and 
            # the keys held are the same, don't walk back here.
            if beenHereBefore(step, pathSoFar, newKeysSoFar):
                # print "    been here before"
                continue
            if step in finishedNodes and finishedNodes[step][0].issuperset(keysHad(newKeysSoFar)) and finishedNodes[step][1] < len(pathSoFar):
                # print "    finished node"
                continue
            if step == end:
                # print "    GOT TO THE END!!!"
                return pathSoFar + [step]

            # This is not the end, but we should investigate this path
            queue.put((end, corridors, doors, pathSoFar + [step], newKeysSoFar, keys, finishedNodes))
    return None



def SolveProblem(lines):
    problemDef = ParseProblem(lines)
    problemDef = TrimProblem(problemDef)
    # check if there is even a solution
    # path = FindPathToBFS(problemDef["EP"], problemDef["corridors"], [], [problemDef["SP"]], [], [], dict())
    # print path 
    # exit()
    path = FindPathToBFS(problemDef["EP"], problemDef["corridors"], problemDef["doors"], [problemDef["SP"]], [], problemDef["keys"], dict())

    print "Here is the path: " + str(path)
    if path == None:
        return -1
    return len(path) - 1

def ParseObjects(numObjs, lines):
    corridors = dict()
    for i in xrange(numObjs):
        fields = lines[i].split()
        start = fields[0]
        end = fields[1]
        if start not in corridors:
            corridors[start] = [end]
        else:
            corridors[start].append(end)
    return corridors

def ParseCorridors(numObjs, lines):
    corridors = dict()
    for i in xrange(numObjs):
        fields = lines[i].split()
        start = fields[0]
        end = fields[1]
        if start not in corridors:
            corridors[start] = [end]
        else:
            corridors[start].append(end)
        if end not in corridors:
            corridors[end] = [start]
        else:
            corridors[end].append(start)
    return corridors


def ParseProblem(lines):
    i = 0
    for l in lines:
        if "Challenge" in l:
            lines = lines[i+1:]
            break
        i = i + 1
    # First line contains nr, NC, NK, ND
    fields = lines[0].split()
    nr = int(fields[0])
    NC = int(fields[1])
    NK = int(fields[2])
    ND = int(fields[3])
    # Now for the start and end
    fields = lines[1].split()
    SP = fields[0]
    EP = fields[1]
    lines = lines[2:]

    # Next are NC lines for corridors
    corridors = ParseCorridors(NC, lines)
    lines = lines[NC:]
    # Next are locations of keys.
    keys = ParseObjects(NK, lines)
    lines = lines[NK:]
    # Finally are locations of doors.
    doors = ParseObjects(ND, lines)
    return {"SP": SP, "EP": EP, "corridors": corridors, "keys": keys, "doors": doors}

def main(): 
    conn = remote('maze01.3dsctf.org', 8002)
    conn.send('start\n')
    print "Sent start"
    while 1 ==1:
        try:
            lines = ["n", "n"]
            line = "n"
            while not (line == "" and len(lines[-2].split()) == 2):
                line = conn.recvline(keepends = False, timeout =1)
                lines.append(line)
                
            printLines(lines)
            print "Attempting..."
            answer = SolveProblem(lines)
            print "Sending answer: " + str(answer)
            conn.send(str(answer))
        except (EOFError, TypeError, ValueError) as e:
            print "Had a failure"
            print e.message
            print "Printed the failures" 
            printLines(lines)
            lines = conn.recvall()
            print lines
            exit()


DEBUG = False
if not DEBUG:
    main()
    exit()


string = """9 9 1 2
0 2
0 1
1 8
1 3
1 4
2 7
3 5
3 6
4 8
5 7
3 a
6 A
7 A
"""


# string = """38 58 7 11
# 20 23
# 0 36
# 0 30
# 1 17
# 1 34
# 1 14
# 1 33
# 2 16
# 2 24
# 3 34
# 3 19
# 3 13
# 4 36
# 4 11
# 4 28
# 4 29
# 4 7
# 5 28
# 6 36
# 6 20
# 7 25
# 7 28
# 8 17
# 8 14
# 9 26
# 9 29
# 10 17
# 11 12
# 12 17
# 12 30
# 13 27
# 13 25
# 13 35
# 14 19
# 14 24
# 14 27
# 15 18
# 16 24
# 16 26
# 17 18
# 18 30
# 19 24
# 19 35
# 19 29
# 21 26
# 22 24
# 23 37
# 24 35
# 24 31
# 25 33
# 25 26
# 25 31
# 26 37
# 27 35
# 27 37
# 28 32
# 28 34
# 28 29
# 30 31
# 34 e
# 36 g
# 8 f
# 2 b
# 16 c
# 27 a
# 31 d
# 32 F
# 33 A
# 4 G
# 37 G
# 9 F
# 10 E
# 11 A
# 19 D
# 21 B
# 25 F
# 5 C
# """

print SolveProblem(string.splitlines())
