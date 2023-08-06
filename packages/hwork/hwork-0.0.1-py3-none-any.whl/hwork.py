import sys
sys.dont_write_bytecode = True


def say_hello(name=None):
    if name is None:
        return "Hello, World!"
    else:
        return f"Hello, {name}!"

