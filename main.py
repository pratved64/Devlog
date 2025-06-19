import sys
import json
from datetime import datetime
import argparse
from utils import *


# init
def init():
    cwd = os.getcwd()
    os.chdir(cwd)
    os.mkdir("./.devlog")
    os.chdir("./.devlog")
    os.mkdir("Sessions")
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

    startStamp = session["start"][:-7]
    endStamp = datetime.now().__str__()[:-7]

    mdstring += f'\nStart: <code>{startStamp}</code>\nEnd: <code>{endStamp}</code>\n'
    mdstring += f'\nEntries: <code>{len(logs)} </code>\n~~~\n'
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
def add(inputStr):
    cwd = os.getcwd()
    with open(cwd + "\\.devlog\\session.json", 'r') as j:
        session = json.load(j)

    with open(session['logfile'], 'a+') as logfile:
        logfile.seek(0)
        line = len(logfile.readlines())
        logfile.write(f"{line}\t{inputStr}\n")


if __name__ == "__main__":
    match sys.argv[1]:
        case "init": init()
        case "start": start()
        case "end": end()
        case "add": add(sys.argv[2])


# 17-06-25: Finished MVP Setup with start end and add functionality.
# TODO: Refactor code to dispatch using argparse. Expand features