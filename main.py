import sys
import json
from datetime import datetime
import argparse
from utils import *


default_config = {
    "ExportFormat": ".md"
}

# init
def init():
    cwd = os.getcwd()
    os.chdir(cwd)
    if os.path.exists(f"{cwd}\\.devlog"):
        print("Devlog has already been initialized here!")
        return

    os.mkdir("./.devlog")
    os.chdir("./.devlog")
    os.mkdir("Sessions")
    with open(f"{cwd}\\.devlog\\config.json", "w") as config:
        json.dump(default_config, config)

    print("Devlog has been initialized. Use \"start\" to create a new session")


# start
def start():
    if os.path.exists(f"{os.getcwd()}\\.devlog\\session.json"):
        print("Session already started")
        return None

    session = {
        "start": datetime.now().__str__(),
        "cwd": os.getcwd(),
        "logfile": os.getcwd() + "\\.devlog\\log.tmp"
    }
    with open(os.getcwd() + "\\.devlog\\session.json", "w") as f:
        json.dump(session, f)

    with open(session["logfile"], "w") as _:
        pass

    print("Started a new session!")
    return session


# end
def end():
    cwd = os.getcwd()
    mdstring = ""
    with open(cwd + "\\.devlog\\session.json", 'r') as j:
        session = json.load(j)

    with open(session['logfile'], 'r') as logfile:
        logs = logfile.readlines()

    logs = list(map(lambda x: x.replace("\n", ""), logs))
    logs = [e for e in logs if e != ""]

    taggedEntries = 0
    for log in logs:
        if "@" in log:
            taggedEntries += 1

    startStamp = session["start"][:-7]
    endStamp = datetime.now().__str__()[:-7]

    mdstring += f'\nStart: <code>{startStamp}</code>\nEnd: <code>{endStamp}</code>\n'
    mdstring += f'\nEntries: <code>{len(logs) - taggedEntries} </code>\n~~~\n'
    mdstring += "".join(list(map(lambda x: x + "\n", logs)))
    mdstring += "~~~"
    print("Session ended!")

    newFilePath = cwd + "\\.devlog\\Sessions\\"
    filename = getUniqueName("Session", newFilePath)
    newFilePath += filename
    with open(newFilePath, "x+") as markdownFile:
        markdownFile.write(toMarkdown(mdstring))

    os.remove(session['logfile'])
    os.remove(f"{os.getcwd()}\\.devlog\\session.json")


# add
def add(args: list[str]):
    cwd = os.getcwd()
    if not os.path.exists(f"{cwd}\\.devlog\\session.json"):
        print("Session does not exist", file=sys.stderr)
        return

    with open(cwd + "\\.devlog\\session.json", 'r') as j:
        session = json.load(j)

    tag = ""
    inputStr = args[0]
    for index, arg in enumerate(args[1:]):
        if arg == "--tag" or arg == "-t":
            tag = "@" + args[index + 2]  # why +2?

    with open(session['logfile'], "r") as logfile:
        lines = logfile.readlines()
        taggedEntries = 0
        for l in lines:
            taggedEntries += 1 if "@" in l else 0

        line = len(lines) - taggedEntries
        print(lines)

    with open(session['logfile'], 'w') as logfile:
        lines = [x for x in lines if x != "\n"]
        newLine = f"{tag}\n{line}\t{inputStr}\n"
        lines.append(removeNewLine(newLine)) # [1:] because \n was being added automatically!
        logfile.writelines(lines)


if __name__ == "__main__":
    match sys.argv[1]:
        case "init":
            init()
        case "start":
            start()
        case "end":
            end()
        case "add":
            add(sys.argv[2:])

# 17-06-25: Finished MVP Setup with start end and add functionality.
# 19-06-25: Added tag features, improved error handling
# TODO: Create parser class to improve dispatch and data sharing, refactor spaghetti code from 19-06 (tag feature), add functionality to export to html