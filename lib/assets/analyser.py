# -*- coding: utf-8 -*-
# Python program to find strongly connected components in a given directed framework using Tarjan's algorithm (single DFS)
# Complexity : O(V+E)
import copy
import operator
from argumentation import Argument
from collections import defaultdict

#This class represents an directed framework using adjacency list representation
class Analyser:

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

    def findForAttack(self, value):
        return next((arg for arg in self.args if arg.id == value), None)

    '''
        A recursive function that find finds and prints strongly connected components using DFS traversal
        nextArg         --> vertex to be visited next
        discovery[]          --> stores discovery times of visited size
        low[]           --> earliest visited vertex (the vertex with minimum discovery time) that can be reached from subtree rooted with current vertex
        stack           --> stores all the connected ancestors (could be part of SCC)
        member[]   --> bit/index array for faster check whether a node is in stack
    '''

    def printFramework(self):
        print "framework size: ", len(self.framework)
        for arg in self.framework:
            for attack in self.framework[arg]:
                print self.args[arg], "attacks ", self.args[attack]

    def printSCCs(self): print self.allSccs
    def returnSCCs(self): return self.allSccs

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
                # print self.args[argOfSCC]
                scc.append(self.args[argOfSCC])
                member[argOfSCC] = False
            # print""
            self.allSccs.append(scc)

    def isTrivial(self, scc):
        for arg in scc:
            for alt in scc:
                # print arg, alt
                # print self.args.index(arg), self.args.index(alt)
                # print self.framework[self.args.index(arg)]
                # print self.args.index(alt) in self.framework[self.args.index(arg)]
                if arg.attacks(alt): return False
        return True

    def findAllSCCLevels(self):
        for scc in self.allSccs:
            if self.allSccs.index(scc) not in self.sccLevels: self.findSCCLevel(scc)

        # TODO: can simplify easily - later
    def findSCCLevel(self, scc):
        level = 0
        if len(self.condensationGraph[self.allSccs.index(scc)]) is 0:
            # print self.allSccs.index(scc), "no parents"
            self.sccLevels[self.allSccs.index(scc)] = level
        elif not self.isTrivial(scc):
            # print self.allSccs.index(scc), "not trivial"
            parents = self.condensationGraph[self.allSccs.index(scc)]
            maxParentLevel = 0
            for parent in parents:
                if parent not in self.sccLevels:
                    self.findSCCLevel(self.allSccs[parent])
                parentLevel = self.sccLevels[parent]
                if parentLevel > maxParentLevel: maxParentLevel = parentLevel
            level = maxParentLevel + 1
            self.sccLevels[self.allSccs.index(scc)] = level
            #Max P in parents(C)
            #{level(P) + 1}
        else:
            # print self.allSccs.index(scc), "trivial"
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
            # print "maxParent", maxParent
            # print self.allSccs[maxParent]
            # print self.isTrivial(self.allSccs[maxParent])
            if not self.isTrivial(self.allSccs[maxParent]): level += 1
            self.sccLevels[self.allSccs.index(scc)] = level
            #Max P,Q in parents(C)
            #{level(P) + 1|P is non-trivial} ∪ {level(Q)|Q is trivial}
        # print self.sccLevels

    def printSCCLevels(self):
        print self.sccLevels
        print ""

    # needs to be made more efficient, maybe and python equivalent of continue?
    def buildCondensationGraph(self):
        for scc in self.allSccs:
            for arg in scc:
                for alt in self.allSccs:
                    for oth in alt:
                        if arg is not oth and scc is not alt and arg.attacks(oth):
                            # self.condensationGraph.append((alt, scc))
                            self.condensationGraph[self.allSccs.index(alt)].append(self.allSccs.index(scc))
        # print self.condensationGraph

    def calculatePreferredExtensions(self):
        currentLevel = 0
        try:
            higherLevel = self.sccLevels[max(self.sccLevels, key = self.sccLevels.get)]
        except:
            higherLevel = 0

        preferredExtensions = []
        currentSccs = [scc for scc in self.sccLevels.keys() if self.sccLevels[scc] is currentLevel]
        arguments = []

        for i in range(len(currentSccs)):
            for arg in self.allSccs[currentSccs[i]]:
                for j in range(i + 1, len(currentSccs)):
                    for othArg in self.allSccs[currentSccs[j]]:
                        if arg.isConflictFree(othArg) and not arg.attacksSelf() and not othArg.attacksSelf():
                            print arg, othArg
                            preferredExtensions.append([arg, othArg])

        if len(preferredExtensions) is 0:
            for scc in currentSccs:
                for arg in self.allSccs[scc]:
                    if not arg.attacksSelf(): preferredExtensions.append([arg])

        for ext in preferredExtensions:
            for arg in ext:
                if not arg.isDefendedBy(ext):
                    preferredExtensions.remove(ext)
                    break

        while currentLevel < higherLevel:
            currentLevel += 1
            currentSccs = [scc for scc in self.sccLevels.keys() if currentLevel is self.sccLevels[scc]]

            arguments = []
            for scc in currentSccs:
                for arg in self.allSccs[scc]: arguments.append(arg)

            extensions = []
            for arg in arguments:
                if not arg.attacksSelf(): extensions.append(arg)

            potentialExtensions = []
            for ext in preferredExtensions:
                for arg in extensions:
                    if arg.isDefendedBy(ext):
                        ext.append(arg)
                        potentialExtensions.append(ext)

            flatten = set(map(tuple,potentialExtensions))
            potentialExtensions = map(list,flatten)

        return preferredExtensions

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
        # for arg in sortedArgs: print arg, sortedArgs[sortedArgs.indexOf(arg)]
        # print sortedArgs
        return sortedArgs

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
