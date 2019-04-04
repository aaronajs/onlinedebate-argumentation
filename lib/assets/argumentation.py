import copy

class Argument(object):

    def __init__(self, id, lead):
        self.id = id
        self.attacksArgument = []
        self.attacked = []
        self.isLeading = lead

    def define(self, id):
        self.id = id

    def attack(self, otherArgument):
        self.attacksArgument.append(otherArgument)
        otherArgument.attackedBy(self)

    def attackedBy(self, otherArgument):
        self.attacked.append(otherArgument)

    def attacks(self, otherArgument):
        return otherArgument in self.attacksArgument

    def isConflictFree(self, other):
        return other not in self.attacksArgument and self not in other.attacksArgument

    def attacksSelf(self):
        return not self.isConflictFree(self)

    def isDefendedBy(self, otherArguments):
        isAttackedBy = copy.copy(self.attacked)
        for arg in otherArguments:
            for attacker in isAttackedBy:
                if arg.attacks(attacker): isAttackedBy.remove(attacker)
            if len(isAttackedBy) is 0: return True
        for attack in self.attacksArgument:
            if attack in isAttackedBy: isAttackedBy.remove(attack)

        # print isAttackedBy[0]
        if len(isAttackedBy) is 0:
            return True
        else:
            return False

    def __str__( self ):
        output = "Argument: " + str(self.id) #+ "\n leading: " + str(self.isLeading)
        # for att in self.attacked:
        #     output = output + att.id + " "
        return output
