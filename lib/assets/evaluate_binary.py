import sys
import json
from collections import defaultdict
from argumentation import Argument
from analyser import Analyser

for_arguments = defaultdict(list)
against_arguments = defaultdict(list)

forArgs = sys.argv[1]
againstArgs = sys.argv[2]
i = 3

while i < len(sys.argv):
    obj = json.loads(sys.argv[i])
    if str(obj["id"]) in forArgs:
        for_arguments[Argument(obj["id"], obj["isLeading"])] = obj["attacks"]
    else:
        against_arguments[Argument(obj["id"], obj["isLeading"])] = obj["attacks"]
    i += 1

for_eval = Analyser(list(for_arguments.keys()))

for arg in for_arguments:
    if len(for_arguments[arg]) != 0:
        for attack in for_arguments[arg]:
            for_eval.addAttack(for_eval.findForAttack(attack), arg)

for_eval.calculateSCCs()
for_eval.buildCondensationGraph()
for_eval.findAllSCCLevels()
for_points = for_eval.calculateDecision()
for_count = 0
for arg in for_points:
    if arg.isLeading:
        for_count += for_points[arg]

against_eval = Analyser(list(against_arguments.keys()))

for arg in against_arguments:
    if len(against_arguments[arg]) != 0:
        for attack in against_arguments[arg]:
            against_eval.addAttack(against_eval.findForAttack(attack), arg)

against_eval.calculateSCCs()
against_eval.buildCondensationGraph()
against_eval.findAllSCCLevels()
against_points = against_eval.calculateDecision()
against_count = 0

for arg in against_points:
    if arg.isLeading:
        against_count += against_points[arg]

if for_count >= against_count:
    print 1
else:
    print 0

# print next((arg.id for arg in rankedArguments if arg.isLeading == True), None)
