# 17-06-25: Finished MVP Setup with start end and add functionality.
# 19-06-25: Added tag features, improved error handling
# 28-06-25: Added basic html export functionality
# 01-07-25: Improved html export with f-string, implemented help, remove and delete commands
# TODO: Improve error checking, Improve html styling
# IMP: !Refactor spaghetti code from 19-06 (tag feature)!
import sys
import json

import errors
import utils
import exporter

from utils import *
from datetime import datetime

default_config = {
    "exportFormat": ".html",
    "debug": True,  # REMOVE BEFORE SHIPPING TO PROD
    "theme": "light"
}


# init
def init():
    """
    init: Initializes Devlog to use in current working directory.
    Arguments: None
    """

    os.chdir(cwd)
    if os.path.exists(f"{cwd}\\.devlog"):
        print("Devlog has already been initialized here!")
        return

    os.mkdir("./.devlog")
    os.chdir("./.devlog")
    os.mkdir("Sessions")
    os.chdir("Sessions")
    os.mkdir("Exported")
    os.mkdir(".txt")
    with open(f"{cwd}\\.devlog\\config.json", "w") as c:
        json.dump(default_config, c)

    print("Devlog has been initialized. Use \"devlog start\" to create a new session")


# start
def start():
    """
    start: Starts a new Devlog session.
    Arguments: None
    """

    session_path = f"{cwd}\\.devlog\\session.json"
    if os.path.exists(session_path):
        print("Session already started")
        return None

    session = {
        "start": datetime.now().__str__(),
        "cwd": cwd,
        "logfile": cwd + "\\.devlog\\log.tmp",
        "branch": utils.getGitBranch(cwd)
    }

    with open(session_path, "w") as f:
        json.dump(session, f)

    with open(session["logfile"], "w") as _:
        pass

    print("Started a new session!")
    return session


# end
def end():
    """
    end: Ends the current session and exports to configured file format.
    Arguments: None
    """
    if not os.path.exists(f"{cwd}\\.devlog\\session.json"):
        raise errors.CommandError("No session in progress! Start a new session with \"devlog start\".")

    with open(f"{cwd}\\.devlog\\session.json", 'r') as j:
        session = json.load(j)

    with open(session['logfile'], 'r') as logfile:
        logs = logfile.readlines()

    with open(f"{cwd}\\.devlog\\config.json", 'r') as cf:
        config_data = json.load(cf)

    logs = list(map(lambda x: x.replace("\n", ""), logs))
    logs = [e for e in logs if e != ""]

    taggedEntries = 0
    for log in logs:
        if "@" in log:
            taggedEntries += 1

    startStamp = session["start"][:-7]
    endStamp = datetime.now().__str__()[:-7]

    newFilePath = cwd + "\\.devlog\\Sessions\\Exported\\"
    txtPath = cwd + "\\.devlog\\Sessions\\.txt\\"
    filename = getUniqueName("Session", newFilePath, config_data['exportFormat'])

    exp = exporter.ExportData(start=startStamp, end=endStamp, name=filename, content=logs, tagged=taggedEntries,
                              branch=session["branch"], theme=config_data['theme'])

    match config_data["exportFormat"]:
        case ".html":
            res = exp.html(newFilePath)
        case ".md":
            res = exp.markdown(newFilePath)
        case _:
            res = -1

    # write to txt for grep
    with open(txtPath + getUniqueName("Session", txtPath, ".txt"), "w") as t:
        t.writelines("\n".join(logs))

    if res == 0:
        print("Session file exported to:", newFilePath + filename)
    os.remove(session['logfile'])
    os.remove(f"{cwd}\\.devlog\\session.json")


# add
def add(args: list[str]):
    """
    add: Adds a new log to the current Devlog session.
    Arguments: <Input> (-t / --tag)
    """
    session_path = f"{cwd}\\.devlog\\session.json"
    if not os.path.exists(session_path):
        print("Session does not exist", file=sys.stderr)
        return

    with open(session_path, 'r') as j:
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

    nowStamp = datetime.now().strftime("%H:%M:%S")
    with open(session['logfile'], 'w') as logfile:
        lines = [x for x in lines if x != "\n"]
        newLine = f"{tag}\n{line}\t{inputStr}\t{nowStamp}\n"
        lines.append(removeNewLine(newLine))
        logfile.writelines(lines)


# config
def config(args: list[str]):
    """
    config: Displays current Devlog configuration. Allows user to change config variables.
    Arguments: (Variable) (New Value)
    """
    with open(f"{cwd}\\.devlog\\config.json", "r") as c:
        cf = json.load(c)

    if not args:
        print("Config:", cf)
        return

    found = False
    for i, arg in enumerate(args):
        if arg in cf:
            found = True
            cf[arg] = args[i + 1]
            print(f"Changed {arg} to {args[i + 1]}")

    if not found: print("No such argument exists!")

    with open(f"{cwd}\\.devlog\\config.json", "w") as c:
        json.dump(cf, c)


# status
def status():
    """
    status: Displays current Devlog session status.
    Arguments: None
    """
    if os.path.exists(f"{cwd}\\.devlog\\session.json"):
        with open(f"{cwd}\\.devlog\\session.json", 'r') as s:
            session = json.load(s)
        print("Session in progress. End current session with \"devlog end\"")
        # implement better way to display current session
        return
    elif os.path.exists(f"{cwd}\\.devlog"):
        print("No session is active. Begin a new session with \"devlog start\"")
    else:
        print("Devlog has not been initialized here! Use \"devlog init\" to get started.")


# clear
def clear():
    os.chdir(f"{cwd}\\.devlog\\Sessions\\.txt\\")
    for fname in os.listdir("."):
        if os.path.isfile(fname):
            os.remove(f".\\{fname}")

    os.chdir(f"{cwd}\\.devlog\\Sessions\\Exported\\")
    for fname in os.listdir("."):
        if os.path.isfile(fname):
            os.remove(f".\\{fname}")


# remove
def remove():
    """
    remove: Removes Devlog from current working directory.
    Arguments: None
    """
    if not os.path.exists(f"{cwd}\\.devlog"):
        print("Devlog has not been initialized here. Nothing to remove.")
        return

    try:
        subprocess.run(['rmdir', '/s', '/q', f"{cwd}\\.devlog"], check=True, shell=True, text=True)
    except subprocess.CalledProcessError as e:
        print(e)

    print(".devlog folder has been removed. To use devlog here, use \"devlog init\"")


# delete
def delete():
    """
    delete: Deletes ongoing devlog session
    Arguments: None
    """
    if not os.path.exists(f"{cwd}\\.devlog\\session.json"):
        print("No session is active. Begin a new session with \"devlog start\"")
        return

    os.remove(f"{cwd}\\.devlog\\session.json")
    print("Session was deleted. To start another use \"devlog start\"")


# help
def help(args: list[str]):
    """
    help: Displays valid commands. Displays further help for a specific command.
    Arguments: (Command)
    """
    if not args:
        print(help.__doc__)
        print("Commands:")
        print("\n".join(command_args.keys()))
        return
    if args[0] in command_args:
        docstr = command_args[args[0]].__doc__
        print(docstr)
    else:
        print("Unknown command. Use \"devlog help\" to see a list of valid commands")


# quick
def quick_test():
    i = 0
    p = f"{cwd}\\.devlog\\Sessions\\Session{i}.html"
    while os.path.exists(p):
        os.remove(p)
        i += 1
        p = f"{cwd}\\.devlog\\Sessions\\Session{i}.html"

    start()
    config(["debug", "False"])
    add(["Hello", "-t", "TODO"])
    add(["Hi there!"])
    end()


# grep
def grep(args: list[str]):
    """
    grep: Searches for specified item in Devlog sessions.
    Arguments: <Item> (-w / --where: [current, past, all])
    """
    item = args[0]  # what we are searching for
    search_loc = "all"
    for index, arg in enumerate(args[1:]):
        if arg == "-w" or arg == "--where":
            match args[index + 2]:
                case "c":
                    search_loc = "current"
                case "current":
                    search_loc = "current"
                case "p":
                    search_loc = "past"
                case "past":
                    search_loc = "past"
                case _:
                    print("Please specify valid location or argument blank!")  # IMPLEMENT CUSTOM ERROR FOR THIS

    print(f"Looking for {item} in {search_loc}")

    match search_loc:
        case "all":
            utils.search_current(cwd, item)
            utils.search_prev(cwd, item)
        case "past":
            utils.search_prev(cwd, item)
        case "current":
            utils.search_current(cwd, item)



command_args = {
    "init": init,
    "start": start,
    "end": end,
    "add": add,
    "config": config,
    "status": status,
    "delete": delete,
    "remove": remove,
    "help": help,
    "quick": quick_test,
    "grep": grep,
    "clear": clear,
}

if __name__ == "__main__":
    cwd = os.getcwd()

    command = sys.argv[1]
    try:
        if command in command_args:
            params = command_args[command].__code__.co_varnames[:command_args[command].__code__.co_argcount]
            if not params:
                command_args[command]()
            else:
                command_args[command](sys.argv[2:])
        else:
            print("Unknown command. Use \"devlog help\" to see a list of valid commands")
    except errors.DevlogError as e:
        print(e)


