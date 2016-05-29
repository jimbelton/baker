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

    def has_key(self, key):
        return self.orderedDict.has_key(key)

    def __len__(self):
        return len(self.orderedDict)

    def remove(self, element):
        del self.orderedDict[element]

    def toList(self):
        return self.orderedDict.keys()
