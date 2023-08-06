# OP - Object Programming (thr.py)
#
# this file is placed in the public domain

"threads (thr)"

# imports

import op
import queue
import threading

from op.utl import get_exception

# classes

class Thr(threading.Thread):

    "thread"

    def __init__(self, func, *args, name="noname", daemon=True):
        super().__init__(None, self.run, name, (), {}, daemon=daemon)
        self._name = name
        self._result = None
        self._queue = queue.Queue()
        self._queue.put((func, args))
        self.sleep = 0
        self.state = op.Object()

    def __iter__(self):
        return self

    def __next__(self):
        for k in dir(self):
            yield k

    def join(self, timeout=None):
        "join thread and return result"
        super().join(timeout)
        return self._result

    def run(self):
        "run thread"
        func, args = self._queue.get()
        target = None
        if args:
            target = op.Default(vars(args[0]))
        self.setName((target and target.txt and target.txt.split()[0]) or self._name)
        try:
            self._result = func(*args)
        except Exception as ex:
            print(get_exception())

    def wait(self, timeout=None):
        "wait for thread to finish"
        super().join(timeout)
        return self._result

# functions

def launch(func, *args, **kwargs):
    "run a function in a thread"
    name = kwargs.get("name", op.get_name(func))
    t = Thr(func, *args, name=name, daemon=True)
    t.start()
    return t
