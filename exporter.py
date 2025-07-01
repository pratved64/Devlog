class ExportData:
    def __init__(self, start="", end="", name="Session0", content=None, tagged=0, branch=""):
        # ? ADD DEFAULT ARGUMENT CHECKING TO ENSURE ALL VARIABLES HAVE BEEN INITIALISED ?
        if content is None: content = []
        self.startStamp = start
        self.endStamp = end
        self.name = name
        self.content = content
        self.tagged = tagged
        self.branch = branch

    def html(self, exportPath):
        logs = []
        i = 0
        tag = None
        while i < len(self.content):
            line = self.content[i]
            if "@" in line:
                j = line.index("@")
                tag = f"&emsp;&emsp;&emsp;<tag>{line[j:]}</tag>"
            else:
                s = f"<counter>{line[0]}</counter> {line[1:]}{tag if tag is not None else ""}<br>"
                logs.append(s)
                tag = None
            i += 1

        main = f"""<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>{self.name.split(".")[0]}</title>
    <style>
        body {{
            font-family: monospace;
        }}

        code {{
            background-color: #aaaaaa;
            height: fit-content;
            margin-top: auto;
            margin-bottom: auto;
            padding: 5px;
            border-radius: 5px;
        }}

        .stamp {{
            display: flex;
            flex-direction: row;
            font-size: 20px;
        }}

        .logs {{
            font-size: 16px;
            background-color: #aaaaaa;
            margin-left: 2vw;
            margin-right: 2vw;
            padding: 1%;
            border-radius: 5px;
        }}

        .entry {{
            font-size: 20px;
        }}

        tag {{
            color: #eed34c;
        }}

        counter {{
            color: #777777;
        }}
    </style>
</head>
<body>
    <div class="stamp">
        <p>Start:&emsp;</p> <code>{self.startStamp}</code>
    </div>
    <div class="stamp">
        <p>End:&emsp;</p> <code>{self.endStamp}</code>
    </div>
    <div class="stamp">
        <p>Branch:&emsp;</p> <code>{self.branch}</code>
    </div>
    <div class="entry">Entries: {len(self.content) - self.tagged}</div> <br>
    <div class="logs">
        {"".join(logs)}
    </div>
</body>
</html>"""  # Template String for html export

        with open(exportPath + f"\\{self.name}", "w") as f:
            f.write(main)

    def markdown(self, exportPath):
        mdstring = ""
        mdstring += f'\nStart: <code>{self.startStamp}</code>\nEnd: <code>{self.endStamp}</code>\n'
        mdstring += f'\nEntries: <code>{len(self.content) - self.tagged} </code>\n~~~\n'
        mdstring += "".join(list(map(lambda x: x + "\n", self.content)))
        mdstring += "~~~"

        with open(exportPath + f"\\{self.name}", "w") as f:
            f.write(mdstring)
