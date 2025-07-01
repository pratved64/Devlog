import os
import subprocess


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


def getGitBranch(cwd: str) -> str:
    os.chdir(cwd)
    try:
        result = subprocess.run(['git', 'status'],
                                check=True,
                                capture_output=True,
                                text=True)
        data = result.stdout
    except subprocess.CalledProcessError as e:
        data = ""
        print(e)

    branch = "NONE FOUND"
    for i, word in enumerate(data.split()):
        if word == 'branch':
            branch = data.split()[i + 1]

    return branch

if __name__ == "__main__":
    cwd = os.getcwd()
    try:
        subprocess.run(['rmdir', f"{cwd}\\.devlog", '/s', '/q'], check=False, shell=True, text=True)
    except subprocess.CalledProcessError as e:
        print(e)