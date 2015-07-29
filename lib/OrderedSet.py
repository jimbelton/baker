from collections import OrderedDict

class OrderedSet:
    def __init__(self, initialList = None):
        self.orderedDict = OrderedDict()

        if not initialList:
            return

        for element in initialList:
            self.orderedDict[element] = None

    def add(self, element):
        self.orderedDict[element] = None

    def __len__(self):
        return len(self.orderedDict)

    def toList(self):
        return self.orderedDict.keys()
