import copy
import operator
from argumentation import Argument
from collections import defaultdict

# Contains algorithms to evaluate an argument framework i.e a debate
class Analyser:

    # constructor stores all the arguments in the framework and initiliases variables
    def __init__(self,arguments):
        self.size = len(arguments) #No. of arguments
        self.args = arguments # contains list of arguments as argument objects
        self.framework = defaultdict(list) #contains list: key(argument index) -> value(list of argument indexes that is attacked by key argument)
        self.time = 0
        self.allSccs = [] #contained as lists of arguments
        self.condensationGraph = defaultdict(list) #contains key value pairs (scc index (child) -> list of scc indexes (parent))
        self.sccLevels = defaultdict(int) #contains key value pairs (scc index -> assigned level)

    # function to add an edge to framework
    def addAttack(self, arg1, arg2):
        arg1.attack(arg2)
        u = self.args.index(arg1)
        v = self.args.index(arg2)
        self.framework[u].append(v)

    # finds an argument with a specific id in the list of arguments
    def findForAttack(self, value):
        return next((arg for arg in self.args if arg.id == value), None)

    # represents the argument framework
    def printFramework(self):
        print "framework size: ", len(self.framework)
        for arg in self.framework:
            for attack in self.framework[arg]:
                print self.args[arg], "attacks ", self.args[attack]

    # print methods
    def printSCCs(self): print self.allSccs
    def returnSCCs(self): return self.allSccs

    # ---
    # calculateSCCs & identifySCCs//
    # these methods were inspired by an example implementation of Tarjan' Algorithm
    # the Algorithm was modified to support Arguments and uses their ids
    # the example was found at https://www.geeksforgeeks.org/tarjan-algorithm-find-strongly-connected-components/
    # ---

    #The function to do DFS traversal. It uses recursive SCCUtil()
    def calculateSCCs(self):
        # Mark all the size as not visited and initialize parent and visited, and ap(articulation point) arrays
        discovery = [-1] * (self.size)
        low = [-1] * (self.size)
        member = [False] * (self.size)
        # Call the recursive helper function to find articulation points in DFS tree rooted with vertex 'i'
        for i in range(self.size):
            if discovery[i] == -1:
                self.identifySCCs(i, low, discovery, member, [])

    def identifySCCs(self, nextArg, low, discovery, member, stack):
        # Initialize discovery time and low value
        discovery[nextArg] = self.time
        low[nextArg] = self.time
        self.time += 1
        member[nextArg] = True
        stack.append(nextArg)

        # Go through all size adjacent to this
        for arg in self.framework[nextArg]:
            # If v is not visited yet, then recur for it
            if discovery[arg] == -1 :
                self.identifySCCs(arg, low, discovery, member, stack)
                # Check if the subtree rooted with v has a connection to one of the ancestors of u
                # Case 1 (per above discussion on discovery and Low value)
                low[nextArg] = min(low[nextArg], low[arg])
            elif member[arg] == True:
                # Update low value of 'u' only if 'v' is still in stack (i.e. it's a back edge, not cross edge).
                # Case 2 (per above discussion on discovery and Low value)
                low[nextArg] = min(low[nextArg], discovery[arg])
        # head node found, pop the stack and print an SCC
        argOfSCC = -1 #To store stack extracted size
        if low[nextArg] == discovery[nextArg]:
            scc = []
            while argOfSCC != nextArg:
                argOfSCC = stack.pop()
                scc.append(self.args[argOfSCC])
                member[argOfSCC] = False
            self.allSccs.append(scc)

    # checks if an scc is trivial
    def isTrivial(self, scc):
        for arg in scc:
            for alt in scc:
                if arg.attacks(alt): return False
        return True

    # ensures that all scc levels are found at stored for use in evaluation
    def findAllSCCLevels(self):
        for scc in self.allSccs:
            if self.allSccs.index(scc) not in self.sccLevels: self.findSCCLevel(scc)

    # called by findAllSCCLevels:
    # recursive method to assign a level to an scc
    # if an scc has no parents - it is level 0
    # else if the scc has parents and is not trivial - its level is the max level of its parents' levels + 1
    # else (trival scc with parents) - its level is the max level of its parents' levels (+ 1 if the parent with the max level is not trivial)
    def findSCCLevel(self, scc):
        level = 0
        if len(self.condensationGraph[self.allSccs.index(scc)]) is 0:
            self.sccLevels[self.allSccs.index(scc)] = level
        elif not self.isTrivial(scc):
            parents = self.condensationGraph[self.allSccs.index(scc)]
            maxParentLevel = 0
            for parent in parents:
                if parent not in self.sccLevels:
                    self.findSCCLevel(self.allSccs[parent])
                parentLevel = self.sccLevels[parent]
                if parentLevel > maxParentLevel: maxParentLevel = parentLevel
            level = maxParentLevel + 1
            self.sccLevels[self.allSccs.index(scc)] = level
        else:
            parents = self.condensationGraph[self.allSccs.index(scc)]
            maxParentLevel = 0
            maxParent = parents[0]
            for parent in parents:
                if parent not in self.sccLevels:
                    self.findSCCLevel(self.allSccs[parent])
                parentLevel = self.sccLevels[parent]
                if parentLevel > maxParentLevel:
                    maxParentLevel = parentLevel
                    maxParent = parent
            level = maxParentLevel
            if not self.isTrivial(self.allSccs[maxParent]): level += 1
            self.sccLevels[self.allSccs.index(scc)] = level

    # represents the scc levels
    def printSCCLevels(self):
        print self.sccLevels
        print ""

    # builds a condensation graph of the sccs in the argument framework
    def buildCondensationGraph(self):
        for scc in self.allSccs:
            for arg in scc:
                for alt in self.allSccs:
                    for oth in alt:
                        if arg is not oth and scc is not alt and arg.attacks(oth):
                            self.condensationGraph[self.allSccs.index(alt)].append(self.allSccs.index(scc))

    # recursive backup method to calculate extensions
    # iterates through an argument to calculate if it can be accepted, based on the calculated acceptances of its attackers
    # if an argument is not attacked, it is accepted
    def backtrack(self, arg):
        if len(arg.attacked) == 0:
            return (arg, True)
        else:
            x = []
            for attacker in arg.attacked:
                y = self.backtrack(attacker)
                x.append(y)
            for elem in x:
                if elem[1] == True:
                    return (arg, False)
            return (arg, True)

    # algorithm to calculate the preferred extensions via scc decomposition or a backup method
    def calculatePreferredExtensions(self):
        currentLevel = 0
        try:
            higherLevel = self.sccLevels[max(self.sccLevels, key = self.sccLevels.get)]
        except:
            higherLevel = 0

        preferredExtensions = []
        arguments = []

        # if the highest level of scc is 0, resort to backup method - won't be able to decompose sccs any further
        if higherLevel == 0:
            possibles = []
            for arg in self.args:
                if arg.isLeading:
                    possibles.append(self.backtrack(arg))
            # uses the accepted arguments to create one large extension - based on leading arguments
            ext = []
            for set in possibles:
                if set[1] == True:
                    ext.append(set[0])
            preferredExtensions.append(ext)

        # scc decomposition to calculate partial extensions
        else:
            currentSccs = [scc for scc in self.sccLevels.keys() if self.sccLevels[scc] is currentLevel]
            # adds accepted arguments from level 0 sccs to a partial extension
            # arguments are accepted if they are admissible, conflict free, don't attack each other in sets
            for i in range(len(currentSccs)):
                for arg in self.allSccs[currentSccs[i]]:
                    for j in range(i + 1, len(currentSccs)):
                        for othArg in self.allSccs[currentSccs[j]]:
                            if arg.isConflictFree(othArg) and not arg.attacksSelf() and not othArg.attacksSelf():
                                preferredExtensions.append([arg, othArg])

            # adds none self attacking arguments as partial extension if not already added
            if len(preferredExtensions) is 0:
                for scc in currentSccs:
                    for arg in self.allSccs[scc]:
                        if not arg.attacksSelf(): preferredExtensions.append([arg])

            # ensure that all arguments in extensions are defended by that extension
            newE = []
            for ext in preferredExtensions:
                for arg in ext:
                    if arg.isDefendedBy(ext):
                        newE.append(ext)
                        break
            preferredExtensions = newE

            # iterates through each level
            while currentLevel < higherLevel:
                currentLevel += 1
                currentSccs = [scc for scc in self.sccLevels.keys() if currentLevel is self.sccLevels[scc]]

                arguments = []
                for scc in currentSccs:
                    for arg in self.allSccs[scc]: arguments.append(arg)

                extensions = []
                for arg in arguments:
                    if not arg.attacksSelf(): extensions.append(arg)
                # uses the accepted arguments of higher levels and check if they are defended by an existing partial extension
                # if defended they can be added to the partial extension
                potentialExtensions = []
                for ext in preferredExtensions:
                    for arg in extensions:
                        if arg.isDefendedBy(ext):
                            ext.append(arg)
                            potentialExtensions.append(ext)

                flatten = set(map(tuple,potentialExtensions))
                potentialExtensions = map(list,flatten)
        # after the final level, the remaining partial extensions become preferred
        return preferredExtensions

    # calculates a score for each argument in the preferred extensions
    # based on how many times it is accepted in each extension
    # the higher the score, the better the argument
    # returns the best arguments
    def calculateAcceptances(self):
        exts = self.calculatePreferredExtensions()
        scepticalMark = len(exts)
        argumentCount = defaultdict(list)
        for ext in exts:
            for arg in ext:
                if arg in argumentCount:
                    argumentCount[arg] += 1
                else:
                    argumentCount[arg] = 1
        sortedArgs = sorted(argumentCount, key=argumentCount.get, reverse=True)
        return sortedArgs

    # same as calculateAcceptances, but used returns the arguments with scores - used to calculate best side
    def calculateDecision(self):
        exts = self.calculatePreferredExtensions()
        scepticalMark = len(exts)
        argumentCount = defaultdict(list)
        for ext in exts:
            for arg in ext:
                if arg in argumentCount:
                    argumentCount[arg] += 1
                else:
                    argumentCount[arg] = 1
        return argumentCount
