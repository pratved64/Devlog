from typing import Callable, Any, Dict, Optional
from dataclasses import dataclass


class Command:
    def __init__(self, name, dispatch):
        self.name: str = name
        self.dispatch: Callable = dispatch
        self.params: list[str] = []
        self.optional_params: set = set()

    def set_params(self, *p, optional: list[str] = None):
        params = list(p)
        self.params = params
        self.optional_params = set(optional)
        return self

    def invoke(self, args: list[Any]):
        kwargs = {}

        for i, param_name in enumerate(self.params):
            if i < len(args):
                kwargs[param_name] = args[i]
            elif param_name not in self.optional_params:
                raise ValueError(f"Missing required flag {param_name} for {self.name}")

        self.dispatch(**kwargs)


class Parser:
    '''def __init__(self, commands: list[str]):
        self.args: Dict[str, Argument] = {}
        self.commands = commands
        self.invoked_command: Optional[str] = None

    def add_argument(self, name: str, argtype: type, dispatch: Callable = None):
        is_flag = (argtype is bool)
        default_value = False if is_flag else None
        self.args[name] = Argument(value=default_value, is_flag=is_flag, dispatch=dispatch)

    def parse(self, sysargs: list[str]):
        i = 0
        while i < len(sysargs):
            arg = sysargs[i]
            if arg in self.args:
                if self.invoked_command is not None and arg in self.commands:
                    raise ValueError("Improper usage, found multiple commands!")
                if arg in self.commands:
                    self.invoked_command = arg
                argument = self.args[arg]
                if argument.is_flag:
                    argument.value = True
                else:
                    if i + 1 >= len(sysargs):
                        raise ValueError(f"Expected value after argument: {arg}")
                    argument.value = sysargs[i + 1]
                    i += 1  # Consume argument value
            i += 1  # Main loop increment

    def get_command(self) -> Optional[str]:
        return self.invoked_command

    def get(self, name):
        return self.args[name].value'''

    def __init__(self):
        self.commands: Dict[str, Command] = {}

    def command(self, name: str, dispatch: Callable) -> Command:
        cmd = Command(name, dispatch)
        self.commands[name] = cmd
        return cmd

    def parse(self, sysargs: list[str]):
        if not sysargs:
            raise ValueError("No arguments provided!")

        cmd_name = sysargs[0]
        command = self.commands.get(cmd_name)
        if not command:
            raise ValueError(f"Unknown command: {cmd_name}!")

        command.invoke(sysargs[1:])


def show(path, x=None):
    with open(path, 'r') as f:
        contents = f.readlines()
        print("".join(contents))
    if x is not None:
        print(x)


if __name__ == "__main__":
    parser = Parser()
    parser.command("read", show).set_params("path", "x", optional=["x"])
    parser.parse(["read", ".\\main.py"])
