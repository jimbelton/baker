import json
import os
import sys

from options import fatal

filePathToProperties = {}

class Properties:
    def __init__(self, filePath):
        """
        Read a Properties file into the cache
        """

        if filePath in filePathToProperties:
            fatal("Properties for file %s have already been read" % filePath)

        self.filePath = filePath

        if os.path.isfile(filePath):
            with open(filePath) as input:
                contents = input.read()

            try:
                self.properties = json.loads(contents)
            except ValueError:
                fatal("Can't understand contents of %s:\n'%s'" % (filePath, contents))

        else:
            self.properties = {}

        self.dirty                    = False
        filePathToProperties[filePath] = self

    @classmethod
    def fromFilePath(clazz, filePath):
        """
        Get or construct Properties object for a file path
        """
        try:
            return filePathToProperties[filePath]
        except KeyError:
            return clazz(filePath)

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
