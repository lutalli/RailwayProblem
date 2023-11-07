import itertools as it
import time, sys, getopt

LINE_BEGIN = '\r'
LINE_CLEAR = '\x1b[2K'

GATE_TYPE_T = 0
GATE_TYPE_C = 1
GATE_TYPE_L = 2
GATE_TYPE_R = 3
GATE_LABEL_T = 'T'
GATE_LABEL_C = 'C'
GATE_LABEL_DICT = {
    GATE_TYPE_T: GATE_LABEL_T,
    GATE_TYPE_C: GATE_LABEL_C
}

def GT(s):
    return (s, GATE_TYPE_T)

def GC(s):
    return (s, GATE_TYPE_C)

def GL(s):
    return (s, GATE_TYPE_L)

def GR(s):
    return (s, GATE_TYPE_R)

def degenerateGate(g):
    t = typeOfGate(g)
    if t == GATE_TYPE_C:
        return g
    return (switchOfGate(g), GATE_TYPE_T)

GTC = [GT, GC]
GTC2 = list(it.product(GTC, repeat=2))

def switchOfGate(g):
    return g[0]

def typeOfGate(g):
    return g[1]

def labelOfGate(g):
    return GATE_LABEL_DICT[typeOfGate(g)]

def reprOfGate(g):
    return f"{switchOfGate(g)}{labelOfGate(g)}"

def getAllGates(S):
    allGates = []
    for s in S:
        allGates.append(GT(s))
        allGates.append(GC(s))
    return allGates

def getAllLRCGates(S):
    allLRCGates = []
    for s in S:
        allLRCGates.append(GL(s))
        allLRCGates.append(GR(s))
        allLRCGates.append(GC(s))
    return allLRCGates

class ConnectionScheme:
    def __init__(self, rel):
        self.rel = rel
        self.mapping = dict(rel + [(g2, g1) for (g1, g2) in rel])

    def __eq__(self, other):
        return self.rel == other.rel

    def __str__(self):
        return "<" + " ".join([f"{reprOfGate(g1)}-{reprOfGate(g2)}" for (g1, g2) in self.rel]) + ">"

    def __getitem__(self, index):
        return list(self.rel)[index]

    def unique(self, g):
        return self.mapping[g]

    def connected(self, g1, g2):
        return ((g1, g2) in self.rel) or ((g2, g1) in self.rel)

class RailwaySystem:
    def __init__(self, S, scheme: ConnectionScheme):
        self.switches = S
        self.dimension = len(S)
        self.gates = getAllGates(S)
        self.scheme = scheme

    def __str__(self):
        return f"{str(self.scheme)}"

    def __repr__(self):
        return f"{str(self.scheme)}"

    def __eq__(self, other):
        return self.scheme == other.scheme

    def isConnected(self):
        for s1 in self.switches:
            for s2 in self.switches:
                if s1 != s2:
                    exists = False
                    for (X, Y) in GTC2:
                        if self.scheme.connected(X(s1), Y(s2)):
                            exists = True
                    if not exists:
                        return False
        return True

    def isIsomorphicTo(self, R):
        for perm in it.permutations(R.switches):
            mapping = dict(zip(self.switches, perm))
            holdsAll = True
            for (s1, s2) in it.product(self.switches, repeat=2):
                for (X, Y) in GTC2:
                    if self.scheme.connected(X(s1), Y(s2)):
                        if not R.scheme.connected(X(mapping[s1]), Y(mapping[s2])):
                            holdsAll = False
                            break
                if not holdsAll:
                    break
            if holdsAll:
                return True
        return False

def getAllPairings(S):
    # from https://stackoverflow.com/a/13020502/13002788
    N = len(S)
    choice_indices = it.product(*[range(k) for k in reversed(range(1, N, 2))])

    for choice in choice_indices:
        tmp = S[:]
        result = []
        for index in choice:
            result.append((tmp.pop(0), tmp.pop(index)))
        yield result

def getAllConnectedRailwaySystems(dim):
    S = list(range(dim))
    allLRCGates = getAllLRCGates(S)

    allLRCPairings = getAllPairings(allLRCGates)
    allConnectedRailwaySystems = []
    for LRCPairing in allLRCPairings:
        rel = list(set([(degenerateGate(g1), degenerateGate(g2)) for (g1, g2) in LRCPairing]))
        
        scheme = ConnectionScheme(rel)
        R = RailwaySystem(S, scheme)

        if not R.isConnected:
            break

        allConnectedRailwaySystems.append(R)   
    
    for R, _ in it.groupby(allConnectedRailwaySystems):
        yield R

def classifyRailwaySystems(dim):
    unclassified = list(getAllConnectedRailwaySystems(dim))
    la = len(unclassified)
    print(la)
    result = []
    equivalenceClassIndex = -1
    while len(unclassified) != 0:
        equivalenceClassIndex += 1
        print(f"Started collecting railway systems of class {equivalenceClassIndex}")
        equivalenceClass = [unclassified[0]]
        unclassified.pop(0)
        for i, R in enumerate(unclassified):
            if R.isIsomorphicTo(equivalenceClass[0]):
                lu = len(unclassified)
                print(f"{LINE_BEGIN + LINE_CLEAR}> {len(equivalenceClass)} railway systems of class {equivalenceClassIndex} found ({la - lu} / {la} = {round((la - lu) / la * 100, 3)}% of total has been classified)", end='')
                equivalenceClass.append(R)
                unclassified.pop(i)
        result.append(equivalenceClass)
        print(f"{LINE_BEGIN + LINE_CLEAR}Finished collecting {len(equivalenceClass)} railway systems of class {equivalenceClassIndex}!\n")

    return result

def runClassification(dim, savefile):
    assert dim % 2 == 0, "ERROR: Raiway system dimension must be a even number"
    print(f"Running classification of {dim}-dimensional railway systems")
    print()
    tA = time.time()
    result = classifyRailwaySystems(dim)
    tB = time.time()
    tDiff = round(tB - tA, 2)
    num = len(result)
    print("------------------------------\n")
    print(f"All done within {tDiff}s.")
    print()
    with open(savefile, "w") as file:
        file.write(f"Classification of {dim}-dimensional railway systems:\n\n")
        for i in range(num):
            cl = result[i]
            cll = len(result[i])
            file.write(f"\nCLASS {i} ({cll})\n")
            for j in range(cll):
                file.write(str(cl[j]))
                if j != cll - 1:
                    file.write(" ")
                else:
                    file.write("\n")
                
        file.write(f"\n\nNumber of different equivalence classes: {num}\n")
        file.write(f"\nTime consumed: {tDiff}s")
    print(f"Result saved to {savefile}!")

    print()

def main(argv):
    opts, _ = getopt.getopt(argv, "d:f:", ["dim=", "dimension=", "file="])
    dim = 2
    savefile = "./result"
    for opt, arg in opts:
        if opt in ("-d", "--dim", "--dimension"):
            dim = int(arg)
        elif opt in ("-f", "--file"):
            savefile = arg

    runClassification(dim, savefile)

if __name__ == "__main__":
    main(sys.argv[1:])

