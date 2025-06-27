class ExportData:
    def __init__(self, start="", end="", name="Session0", content=None, tagged=0):
        # ADD DEFAULT ARGUMENT CHECKING TO ENSURE ALL VARIABLES HAVE BEEN INITIALISED
        if content is None: content = []
        self.startStamp = start
        self.endStamp = end
        self.name = name
        self.content = content
        self.tagged = tagged

    def html(self, exportPath):
        main = f"<!DOCTYPE html> \
                <html lang=\"en\"> \
                <head>\
                    <meta charset=\"UTF-8\"> \
                    <title>{self.name}</title> \
                </head> \
                <body> \
                    <div class=\"stamp\"> \
                        <p>Start:</p> \
                        <span>{self.startStamp}</span> \
                    </div> \
                    <div class=\"stamp\"> \
                        <p>End:</p> \
                        <span>{self.endStamp}</span> \
                    </div> \
                    <div class=\"logs\">{"<br>".join(self.content)}</div> \
                </body> \
                </html>"  # Template String for html export

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
