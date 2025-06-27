import os


def toMarkdown(fileStr: str) -> str:
    fileStr = fileStr.replace('\n', "  \n")
    fileStr = fileStr.replace('\t', "    ")
    return fileStr


def getUniqueName(filename: str, directory: str, extension: str) -> str:
    counter = 0
    path = directory + filename
    if not os.path.exists(path + str(counter) + extension):
        return filename + str(counter) + extension

    while os.path.exists(path + str(counter) + extension):
        counter += 1
    return filename + str(counter) + extension

def removeNewLine(s: str) -> str:
    if s[0] == "\n": return s[1:]
    else: return s
