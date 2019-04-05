import sys
import json
from collections import defaultdict
from argumentation import Argument
from analyser import Analyser

arguments = defaultdict(list)

i = 1

while i < len(sys.argv):
    obj = json.loads(sys.argv[i])
    arguments[Argument(obj["id"], obj["isLeading"])] = obj["attacks"]
    i += 1

eval = Analyser(list(arguments.keys()))
for arg in arguments:
    if len(arguments[arg]) != 0:
        for attack in arguments[arg]:
            eval.addAttack(arg, eval.findForAttack(attack))

eval.calculateSCCs()
eval.buildCondensationGraph()
eval.findAllSCCLevels()
rankedArguments = eval.calculateAcceptances()
print next((arg.id for arg in rankedArguments if arg.isLeading == True), None)

# print len(sys.argv)
# the result is a Python dictionary:
# print y["age"]
