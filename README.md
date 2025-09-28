# Devlog

## Overview

This comprehensive CLI tool allows developers to streamline taking notes while creating, debugging and even learning.
Have you ever felt as if comments weren't enough information? Or have you been working on a large project, only to come
back the next day and be completely lost? If so, this is the tool for you. \
With Devlog you can:
- Record notes directly from your terminal
- Tag notes and filter them to label specific tasks
- Export notes by session to a customizable HTML/Markdown file

Detailed below is how exactly to install and use this tool, as well as future plans for features

## Installation
To install devlog, create a local git repository and clone this repository using the following commands

```bash
git init
git clone https://github.com/pratved64/Devlog.git
```

Once the repository has been cloned locally, you can run the python script `main.py` in your *working directory* to use the tool.
Optionally, you can save the path to the executable tool. You can find it in `~/builds/main.exe`. \
To save it in an environment variable, run the following commands on powershell:
```
$UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
$NewUserPath = "$UserPath;C:\Path\to\Devlog\Directory\builds\"
[Environment]::SetEnvironmentVariable("Path", $NewUserPath, "User")
```
Ensure to rename the executable file to your desired name, such as *devlog.exe* for clarity in terminal sessions.

## Documentation
### Basic Workflow
A typical Devlog session would look something like this:
1. Navigate to your project directory and initialise devlog. This only needs to be done once per project
```bash
devlog init
```
2. When you're ready to start working, create a new session with
```bash
devlog start
```
3. As you work, add notes, thoughts and logs with tags to categorize them
```bash
devlog add "Fixed validation logic" -t FIX
devlog add "Optimize database query" -t TODO
```
4. Once you're done, you can save and export your session's logs
```bash
devlog end
```

### Commands
`init` \
Initializes Devlog in the current working directory. This creates a .devlog folder containing necessary configuration data and session data
* Usage: `devlog init`

`start` \
Starts a new logging session. It records the current time and syncs with the current working git branch if found. A session must be activated to add logs
* Usage: `devlog start`

`end` \
Ends the current session. This command stops the timer, gathers all the added notes from the session and exports them to a single file (HTML/Markdown based on your config)
* Usage: `devlog end`

`add` \
Adds a new log entry to the current session. Ensure to enclose the input note within quotes
* Usage: `devlog add "<your log>"`
* Options: `-t`,`--tag <tagname>` Attaching a tag to your log entry, used for filtering and summaries

`status` \
Displays current status of a Devlog session within the working directory. It lets you know if a session is in progress or not
* Usage: `devlog status`

`config` \
Displays or modifies the config settings. Running it without any arguments will list the variables and values in the config file
* Usage: `devlog config [variable] [value]`

`grep` \
Searches through your logs for a specific keyword or phrase
* Usage: `devlog grep "<search term>"`
* Options: `-w`,`--where` Specifies where to search
  * `c` or `current` to search the active session
  * `p` or `past` to search all previous exported sessions
  * (default) searches everywhere

`summary` \
Provides a summary of logs from specified files or date ranges, filtering by tags
* Usage: `devlog summary [options]`
* Options:
  * `-f`,`--filename <filename>` generates a summary for a specific file
  * `-r`,`--range <start> <end>` generates a summary for all sessions within a date range

`help` \
Displays a list of valid commands or shows detailed information about usage of a specific command
* Usage: `devlog help [command]`
* If command is left blank, all valid commands are listed

`delete` \
Deletes the ongoing session **without saving or exporting** the added logs
* Usage: `devlog delete`

`clear` \
Permanently removes all previously exported session files from `.devlog/Sessions` directory
* Usage: `devlog clear`

`remove` \
Removes Devlog from the current working directory, deleting the `.devlog` folder and all its contents. This action is irreversible and will delete all configurations and logs for your project
* Usage: `devlog remove`

## Future Scope
This is a long-term, ongoing project that I plan on adding to. The key improvements and features that will be added are listed below
1. Full Export customizability via export template files
2. AI Generated summaries to extend functionality and create smarter commits
3. Port to VSCode extensions and further IDE integration

