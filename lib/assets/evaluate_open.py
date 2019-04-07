import sys
import json
from collections import defaultdict
from argumentation import Argument
from analyser import Analyser

# script used to calculate open debates

# initialses lists of arguments
arguments = defaultdict(list)

i = 1

# iterates through arguments passed to script and stores them as Arguments
# adds to the argument list
while i < len(sys.argv):
    obj = json.loads(sys.argv[i])
    arguments[Argument(obj["id"], obj["isLeading"])] = obj["attacks"]
    i += 1

# creates evaluator for the arguments
eval = Analyser(list(arguments.keys()))

# adds argument attacks to the evaluator
for arg in arguments:
    if len(arguments[arg]) != 0:
        for attack in arguments[arg]:
            eval.addAttack(eval.findForAttack(attack), arg)

# performs the evaluation on the argument framework and obtains the points
eval.calculateSCCs()
eval.buildCondensationGraph()
eval.findAllSCCLevels()
rankedArguments = eval.calculateAcceptances()

# returns value which is the id of the winning argument
# argument has to be leading
# value is passed back to rails application
print next((arg.id for arg in rankedArguments if arg.isLeading == True), None)
