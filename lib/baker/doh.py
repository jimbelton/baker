import json
import os
import sys

from options import fatal

dirPathToDoh = {}

class Doh:
    def __init__(self, dirPath):
        """
        Read a doh file into the cache
        """
        if dirPath in dirPathToDoh:
            fatal("doh for directory %s has already been constructed" % dirPath)

        self.filePath = os.path.join(dirPath, "baker.doh")

        if os.path.isfile(self.filePath):
            with open(self.filePath) as input:
                contents = input.read()

            try:
                self.properties = json.loads(contents)
            except ValueError:
                fatal("Can't understand contents of %s:\n'%s'" % (self.filePath, contents))

        else:
            self.properties = {}

        self.dirty            = False
        dirPathToDoh[dirPath] = self

    @classmethod
    def fromDirPath(clazz, dirPath):
        """
        Get or construct doh object for a directory path
        """

        try:
            return dirPathToDoh[dirPath]
        except KeyError:
            return clazz(dirPath)

    def getProperty(self, name, default=None):
        if name in self.properties:
            return self.properties[name]

        return default

    def setProperty(self, name, value):
        self.properties[name] = value
        self.dirty            = True

    def flushIfDirty(self):
        if self.dirty:
            with open(self.filePath, "w") as output:
                json.dump(self.properties, output, sort_keys=True, indent=4, separators=(',', ': '))
                output.write("\n")

            self.dirty = False
