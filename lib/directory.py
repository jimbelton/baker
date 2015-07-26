import os
import re

directories       = {}
fileToDirectories = {}
indexPat          = None

class Directory:
    def __init__(self, path):
        self.path         = path
        directories[path] = self

    @classmethod
    def fromPath(clazz, path):
        """
        Construct or return a cached directory object for the path
        """

        try:
            return directories[path]
        except KeyError:
            return clazz(path)

    def getRelpath(self, start=os.curdir):
        return os.path.relpath(self.path, start)

    def getContents(self):
        """
        Get contents of directory, caching them, and map include/import file names back to directories
        @return an ordered pair of lists of files and subdirectories
        """

        try:
            return (self.files, self.subDirs)
        except AttributeError:
            self.files   = []
            self.subDirs = []

            for entry in os.listdir(self.path):
                entryPath = os.path.join(self.path, entry)

                if os.path.isdir(entryPath):
                    if entry == ".git":
                        continue

                    self.subDirs.append(entry)
                    continue

                if os.path.isfile(entryPath):
                    self.files.append(entry)

                    # If an index has been set, index files that we may need to search for (e.g. header files)

                    if indexPat and indexPat.match(entry):
                        if entry not in fileToDirectories:
                            fileToDirectories[entry] = [self]
                        else:
                            fileToDirectories[entry].append(self)

        return (self.files, self.subDirs)

    @classmethod
    def setIndexExp(clazz, regExp):
        """
        Set a regular expression for which all matching filenames will be indexed
        """
        global indexPat
        indexPat = re.compile(regExp)
