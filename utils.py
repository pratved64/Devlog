import os


def toMarkdown(fileStr: str) -> str:
    fileStr = fileStr.replace('\n', "  \n")
    fileStr = fileStr.replace('\t', "    ")
    return fileStr


def getUniqueName(filename: str, directory: str) -> str:
    counter = 0
    path = directory + filename
    if not os.path.exists(path + str(counter) + ".md"):
        return filename + str(counter) + ".md"

    while os.path.exists(path + str(counter) + ".md"):
        counter += 1
    return filename + str(counter) + ".md"

def removeNewLine(s: str) -> str:
    if s[0] == "\n": return s[1:]
    else: return s
