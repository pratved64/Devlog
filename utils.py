import os
import subprocess
import datetime


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
    if s[0] == "\n":
        return s[1:]
    else:
        return s


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
        # print(e)

    branch = "NONE FOUND"
    for i, word in enumerate(data.split()):
        if word == 'branch':
            branch = data.split()[i + 1]

    return branch


def search_current(cwd: str, item: str):
    print("\nCurrent Session:")
    if not os.path.exists(f"{cwd}\\.devlog\\session.json"):
        print("No session is active. Cannot parse.\n")
        return

    if "@" in item:
        tag = True
    else:
        tag = False

    with open(f"{cwd}\\.devlog\\log.tmp", "r") as c:
        current = c.readlines()

    for i, line in enumerate(current):
        if item in line:
            print(line.rstrip())
            if tag: print(current[i + 1])


def search_prev(cwd: str, item: str):
    print("\nPrevious Sessions:")
    if "@" in item:
        tag = True
    else:
        tag = False
    for filename in os.listdir(f"{cwd}\\.devlog\\Sessions\\.txt\\"):
        p = f"{cwd}\\.devlog\\Sessions\\.txt\\{filename}"
        with open(p, 'r') as f:
            content = f.readlines()

        for i, line in enumerate(content):
            # print(line)
            if item in line:
                l = f"{filename}\n{line.rstrip()}"
                print(l)
                if tag: print(content[i + 2])


def getFilesInRange(start, end, cwd):
    _start = datetime.datetime.strptime(start, "%Y-%m-%d")
    _end = datetime.datetime.strptime(end, "%Y-%m-%d")
    folder_path = f"{cwd}\\.devlog\\Sessions\\.txt\\"

    files = []

    for file in os.listdir(folder_path):
        fp = os.path.join(folder_path, file)
        if os.path.isfile(fp):
            last_write = datetime.datetime.fromtimestamp(os.path.getmtime(fp))
            if _start <= last_write < _end:
                files.append(fp)

    return files


def summariseFile(content, tags):
    for i, line in enumerate(content):
        if "@" in line:
            l = line.replace("@", " ").rstrip().strip()
            if l in tags:
                print(f"{content[i + 1].strip()}\t{l}")



if __name__ == "__main__":
    cwd = os.getcwd()
    try:
        subprocess.run(['rmdir', f"{cwd}\\.devlog", '/s', '/q'], check=False, shell=True, text=True)
    except subprocess.CalledProcessError as e:
        print(e)
