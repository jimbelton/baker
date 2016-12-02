import os
import re

directories       = {}
fileToDirectories = {}
indexPat          = None

def lengthOfCommonPrefix(left, right):
    maximum = len(left) if len(left) < len(right) else len(right)

    for i in range(0, maximum):
        if left[i] != right[i]:
            return i

    return maximum

def findFileInDirectories(filePath, closestToPath = None):
    """
    Search for a file in the cache of directories, respecting its leading directory path if any
    @param filePath      The path to the file to search for. This can be a filename, a relative path, or an absolute path
    @param closestToPath If specified and multiple directories, return only the one(s) with the largest common prefix with this path
    """

    if filePath[0] == '/':    # Absolute paths are a special case: just look
        if not os.path.is_file(filePath):
            return None

        return [Directory.fromPath(os.path.dirname(filePath))]

    fileName = os.path.basename(filePath)
    filePath = os.path.dirname(filePath)
    fileDirs = fileToDirectories.get(fileName)

    if not fileDirs:    # Not found
        return None

    if filePath != "":    # Relative paths must be verified
        matching = []
        filePath = "/" + filePath    # Match a full directory name at the beginning of the path

        for fileDir in fileDirs:
            if fileDir.path.endswith(filePath):
                matching.append(Directory.fromPath(fileDir.path[:-len(filePath)]))    # Need the directory that the filePath is under

        if len(matching) == 0:
            return None

        fileDirs = matching

    if len(fileDirs) == 1 or not closestToPath:
        return fileDirs

    # Find the closest match(es)

    longestCommonPath = 0
    matching          = []

    for fileDir in fileDirs:
        commonLen = lengthOfCommonPrefix(fileDir.path, closestToPath)

        if commonLen < longestCommonPath:
            continue

        if commonLen > longestCommonPath:
            matching          = []
            longestCommonPath = commonLen

        matching.append(fileDir)

    assert len(matching) > 0
    return matching

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

    def containsFile(self, fileName):
        return os.path.isfile(os.path.join(self.path, fileName))

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
