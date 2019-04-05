import sys
import json
from collections import defaultdict
from argumentation import Argument
from analyser import Analyser

# script used to calculate binary debates

# initialses lists of arguments of both sides
for_arguments = defaultdict(list)
against_arguments = defaultdict(list)

# obtains argument lists passed to script
forArgs = sys.argv[1]
againstArgs = sys.argv[2]
i = 3

# iterates through arguments passed to script and stores them as Arguments
# adds to the for or against list
while i < len(sys.argv):
    obj = json.loads(sys.argv[i])
    if str(obj["id"]) in forArgs:
        for_arguments[Argument(obj["id"], obj["isLeading"])] = obj["attacks"]
    else:
        against_arguments[Argument(obj["id"], obj["isLeading"])] = obj["attacks"]
    i += 1

# creates evaluator for the for arguments
for_eval = Analyser(list(for_arguments.keys()))

# adds argument attacks to the evaluator
for arg in for_arguments:
    if len(for_arguments[arg]) != 0:
        for attack in for_arguments[arg]:
            for_eval.addAttack(for_eval.findForAttack(attack), arg)

# performs the evaluation on the for argument framework and obtains the points
for_eval.calculateSCCs()
for_eval.buildCondensationGraph()
for_eval.findAllSCCLevels()
for_points = for_eval.calculateDecision()

# calculates the overall points for all the leading for arguments
for_count = 0
for arg in for_points:
    if arg.isLeading:
        for_count += for_points[arg]

# creates evaluator for the against arguments
against_eval = Analyser(list(against_arguments.keys()))

# adds argument attacks to the evaluator
for arg in against_arguments:
    if len(against_arguments[arg]) != 0:
        for attack in against_arguments[arg]:
            against_eval.addAttack(against_eval.findForAttack(attack), arg)

# performs the evaluation on the against argument framework and obtains the points
against_eval.calculateSCCs()
against_eval.buildCondensationGraph()
against_eval.findAllSCCLevels()
against_points = against_eval.calculateDecision()

# calculates the overall points for all the leading against arguments
against_count = 0
for arg in against_points:
    if arg.isLeading:
        against_count += against_points[arg]

# returns value to represent a boolean to determine which side is winning
# 1 if for, 0 if against
# value is passed back to rails application
if for_count >= against_count:
    print 1
else:
    print 0
