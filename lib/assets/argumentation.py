import copy

# Represents an argument
class Argument(object):

    # constructor for an Argument
    # requires:
        # id - provided by argument created in rails app
        # lead - whether or not he argument is leading
    # also initiliases lists of arguments this argument attacks, and arguments that attack this argument
    def __init__(self, id, lead):
        self.id = id
        self.attacksArgument = []
        self.attacked = []
        self.isLeading = lead

    # accessor for id
    def define(self, id):
        self.id = id

    # adds the argument this argument attacks
    # also adds this argument to the attacked list of the other argument
    def attack(self, otherArgument):
        self.attacksArgument.append(otherArgument)
        otherArgument.attackedBy(self)

    # sets this argument to be attacked by other argument
    def attackedBy(self, otherArgument):
        self.attacked.append(otherArgument)

    # checks id this argument attacks another argument
    def attacks(self, otherArgument):
        return otherArgument in self.attacksArgument

    # checks that two arguments don't attack each other
    def isConflictFree(self, other):
        return other not in self.attacksArgument and self not in other.attacksArgument

    # checks if argument attacks itself - unlikely
    def attacksSelf(self):
        return not self.isConflictFree(self)

    # checks if an argument is defended by a set of other arguments
    # an argument is defended if every argument that attacks it, is attacked by at least one of the other arguments
    def isDefendedBy(self, otherArguments):
        isAttackedBy = copy.copy(self.attacked)
        for arg in otherArguments:
            for attacker in isAttackedBy:
                if arg.attacks(attacker): isAttackedBy.remove(attacker)
            if len(isAttackedBy) is 0: return True
        for attack in self.attacksArgument:
            if attack in isAttackedBy: isAttackedBy.remove(attack)
        if len(isAttackedBy) is 0:
            return True
        else:
            return False

    # override to string
    def __str__(self):
        output = str(self.id)
        return output
