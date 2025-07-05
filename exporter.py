import os.path
import errors


class ExportData:
    def __init__(self, start="", end="", name="", content=None, tagged=-1, branch="", theme="", debug=False):
        if debug:
            def_vals = []
            if start == "": def_vals.append("start")
            if end == "": def_vals.append("end")
            if name == "": def_vals.append("name")
            if not content: def_vals.append("content")
            if tagged < 0: def_vals.append("tagged")
            if branch == "": def_vals.append("branch")
            if theme == "": def_vals.append("theme")
            if not def_vals:
                print("Warning: The following values have not been initialized:")
                print("\n".join(def_vals))

        self.startStamp = start
        self.endStamp = end
        self.name = name
        self.content = content
        self.tagged = tagged
        self.branch = branch
        self.theme = theme
        self.debug = debug

    def html(self, export_path):
        logs = []
        i = 0
        tag = None
        while i < len(self.content):
            line = self.content[i]
            if "@" in line:
                j = line.index("@")
                tag = f"&emsp;&emsp;&emsp;<tag>{line[j:]}</tag>"
            else:
                _, l, stamp = line[1:].split("\t")
                stamp = f"&emsp;&emsp;&emsp;<time>{stamp}</time>"
                l = f"&emsp;&emsp;&emsp;{l}"
                s = f"<counter>{line[0]}</counter> {stamp} {l} {tag if tag is not None else ""}<br>"
                logs.append(s)
                tag = None
            i += 1

        if self.debug:
            print(logs)
            return -1

        main = f"""<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>{self.name.split(".")[0]}</title>
    <style>
        :root {{ {self.get_theme()} }}
        
        body {{
            font-family: var(--font);
            background-color: var(--background);
            color: var(--body-text);
        }}

        code {{
            background-color: var(--block);
            height: fit-content;
            margin-top: auto;
            margin-bottom: auto;
            padding: 5px;
            border-radius: 5px;
            color: var(--block-text);
        }}
        
        time {{
            color: var(--block-text);
        }}

        .stamp {{
            display: flex;
            flex-direction: row;
            font-size: 20px;
        }}

        .logs {{
            font-size: 16px;
            background-color: var(--block);
            margin-left: 2vw;
            margin-right: 2vw;
            padding: 1%;
            border-radius: 5px;
            color: var(--block-text);
        }}

        .entry {{
            font-size: 20px;
            color: var(--body-text);
        }}

        tag {{
            color: var(--tag);
        }}

        counter {{
            color: var(--block-text);
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

        with open(export_path + f"\\{self.name}", "w") as f:
            f.write(main)
        return 0

    def markdown(self, export_path):
        mdstring = ""
        mdstring += f'\nStart: <code>{self.startStamp}</code>\nEnd: <code>{self.endStamp}</code>\n'
        mdstring += f'\nEntries: <code>{len(self.content) - self.tagged} </code>\n~~~\n'
        mdstring += "".join(list(map(lambda x: x + "\n", self.content)))
        mdstring += "~~~"

        if self.debug:
            print(mdstring)
            return -1

        with open(export_path + f"\\{self.name}", "w") as f:
            f.write(mdstring)

        return 0

    def get_theme(self) -> str:
        script_path = os.path.dirname(os.path.abspath(__file__))
        theme = []
        if not os.path.exists(f"{script_path}\\Themes\\{self.theme}.cfg"):
            raise errors.ThemeNotFoundError("Could not find specified theme. Please check its path and try again.")

        with open(f"{script_path}\\Themes\\{self.theme}.cfg", "r") as t:
            theme_data = t.readlines()

        for line in theme_data:
            var_name, value = line.split("=")
            var = f"--{var_name}: {value};"
            theme.append(var)

        return " ".join(theme)
