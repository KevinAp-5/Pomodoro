from os import path
from sys import platform

def whereami(index=1) -> str:
    """Return the path of where the python script is running in"""
    try:
        if platform == 'win32':
            return "\\".join(path.realpath(__file__).split('\\')[:-index])
        else:
            return '/'.join(path.realpath(__file__).split('/')[:-index])
    except Exception:
        raise


if __name__ == '__main__':
    print(whereami(1))
