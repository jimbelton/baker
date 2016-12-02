import os
import re

directories       = {}
fileToDirectories = {}
indexPat          = None

def findFileInDirectories(filePath):
    """
    Search for a file in the cache of directories, respecting its leading directory path if any
    """
    fileName = os.path.basename(filePath)
    filePath = os.path.dirname(filePath)
    fileDirs = fileToDirectories.get(fileName)

    # Not found or normal case (just a file name)
    if not fileDirs or filePath == "":
        return fileDirs

    # Absolute path
    if filePath[0] == '/':
        for fileDir in fileDirs:
            if fileDir.path == filePath:
                return [fileDir]

    matching = []
    filePath = "/" + filePath    # insure we match a full directory name at the beginning of the path

    for fileDir in fileDirs:
        if fileDir.path.endswith(filePath):
            matching.append(Directory.fromPath(fileDir.path[:-len(filePath)]))    # Need the directory that the filePath is under

    return matching if len(matching) > 0 else None

class Directory:
    def __init__(self, path):
        self.path         = path
        directories[path] = self

    def __repr__(self):
        return self.path

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
            return (self.files, self.subDirs)    # Return cached contents
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
