import os
import functools
from main import *

def test(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Ran test {func.__name__}...", end="")
        result = func(*args, **kwargs)
        print("Ok") if result == 0 else print(f"Failed with status code {result}")
        return result
    return wrapper

@test
def test1():
    os.system("python main.py init")
    os.system("python main.py start")
    os.system("python main.py yo")
    os.system("python main.py this")
    os.system("python main.py is")
    os.system("python main.py rad")
    os.system("python main.py end")
    return 0 if os.path.exists(f"{os.getcwd()}\\.devlog\\Sessions\\Session0.md") else 1

if __name__ == '__main__':
    test1()