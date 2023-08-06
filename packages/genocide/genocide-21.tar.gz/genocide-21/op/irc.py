# OP - Object Programming (irc.py)
#
# this file is placed in the public domain

"internet relay chat (irc)"

# imports

import os
import queue
import socket
import textwrap
import time
import threading
import _thread

import op
from op.dbs import last
from op.hdl import Event, Handler, cmd
from op.prs import parse
from op.thr import launch
from op.usr import Users
from op.utl import locked

# defines

def __dir__():
    return ("Cfg", "DCC", "Event", "IRC", "init")

def init(hdl):
    "create a irc bot and return it"
    i = IRC()
    i.clone(hdl)
    if op.debug:
        fmt = op.format(i.cfg, op.keys(i.cfg), ("username", "realname"))
        if fmt:
            print(fmt)
    return launch(i.start)

# locks

saylock = _thread.allocate_lock()

# classes

class Cfg(op.Cfg):

    "configuration object"

    channel = "#objectprogramming"
    nick = "opd"
    server = "localhost"
    username = "opd"
    realname = "Object Programming (OP)"

    def __init__(self):
        super().__init__()
        self.channel = Cfg.channel
        self.nick = Cfg.nick
        self.realname = Cfg.realname
        self.server = Cfg.server
        self.username = Cfg.username

class Event(Event):

    "irc event"

class TextWrap(textwrap.TextWrapper):

    "text wrapper"

    def __init__(self):
        super().__init__()
        self.break_long_words = False
        self.drop_whitespace = False
        self.fix_sentence_endings = True
        self.replace_whitespace = True
        self.tabsize = 4
        self.width = 450

class IRC(Handler):

    "irc bot"

    def __init__(self):
        super().__init__()
        self._buffer = []
        self._connected = threading.Event()
        self._joined = threading.Event()
        self._outqueue = queue.Queue()
        self._sock = None
        self._fsock = None
        self._trc = ""
        self.cc = "!"
        self.cfg = Cfg()
        self.cmds = op.Object()
        self.channels = []
        self.register("cmd", cmd)
        self.register("ERROR", self.ERROR)
        self.register("LOG", self.LOG)
        self.register("NOTICE", self.NOTICE)
        self.register("PRIVMSG", self.PRIVMSG)
        self.register("QUIT", self.QUIT)
        self.register("366", self.JOINED)
        self.speed = "slow"
        self.state = op.Object()
        self.state.needconnect = False
        self.state.error = ""
        self.state.last = 0
        self.state.lastline = ""
        self.state.nrconnect = 0
        self.state.nrerror = 0
        self.state.nrsend = 0
        self.state.pongcheck = False
        self.threaded = False
        self.verbose = False
        self.users = Users()

    def _connect(self, server):
        "connect (blocking) to irc server"
        oldsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        oldsock.setblocking(1)
        oldsock.settimeout(5.0)
        try:
            oldsock.connect((server, 6667))
        except (OSError, ConnectionError):
            time.sleep(2.0)
            try:
                oldsock.connect((server, 6667))
            except (OSError, ConnectionError):
                self._connected.set()
                return False
        oldsock.setblocking(1)
        oldsock.settimeout(1200.0)
        self._sock = oldsock
        self._fsock = self._sock.makefile("r")
        fileno = self._sock.fileno()
        os.set_inheritable(fileno, os.O_RDWR)
        self._connected.set()
        return True

    def _parsing(self, txt):
        "into an event"
        rawstr = str(txt)
        rawstr = rawstr.replace("\u0001", "")
        rawstr = rawstr.replace("\001", "")
        o = Event()
        o.rawstr = rawstr
        o.orig = repr(self)
        o.command = ""
        o.arguments = []
        arguments = rawstr.split()
        if arguments:
            o.origin = arguments[0]
        else:
            o.origin = self.cfg.server
        if o.origin.startswith(":"):
            o.origin = o.origin[1:]
            if len(arguments) > 1:
                o.command = arguments[1]
                o.type = o.command
            if len(arguments) > 2:
                txtlist = []
                adding = False
                for arg in arguments[2:]:
                    if arg.count(":") <= 1 and arg.startswith(":"):
                        adding = True
                        txtlist.append(arg[1:])
                        continue
                    if adding:
                        txtlist.append(arg)
                    else:
                        o.arguments.append(arg)
                o.txt = " ".join(txtlist)
        else:
            o.command = o.origin
            o.origin = self.cfg.server
        try:
            o.nick, o.origin = o.origin.split("!")
        except ValueError:
            o.nick = ""
        target = ""
        if o.arguments:
            target = o.arguments[-1]
        if target.startswith("#"):
            o.channel = target
        else:
            o.channel = o.nick
        if not o.txt:
            if rawstr[0] == ":":
                rawstr = rawstr[1:]
            o.txt = rawstr.split(":", 1)[-1]
        if not o.txt and len(arguments) == 1:
            o.txt = arguments[1]
        spl = o.txt.split()
        if len(spl) > 1:
            o.args = spl[1:]
        return o

    @locked(saylock)
    def _say(self, channel, txt):
        "on a channel"
        wrapper = TextWrap()
        txt = str(txt).replace("\n", "")
        for t in wrapper.wrap(txt):
            if not t:
                continue
            self.command("PRIVMSG", channel, t)
            if (time.time() - self.state.last) < 4.0:
                time.sleep(4.0)
            self.state.last = time.time()

    def _some(self):
        "blocking read"
        inbytes = self._sock.recv(512)
        txt = str(inbytes, "utf-8")
        if txt == "":
            raise ConnectionResetError
        self.state.lastline += txt
        splitted = self.state.lastline.split("\r\n")
        for s in splitted[:-1]:
            self._buffer.append(s)
        self.state.lastline = splitted[-1]

    def announce(self, txt):
        "annouce text"
        for channel in self.channels:
            self.say(channel, txt)

    def command(self, cmd, *args):
        "send a command"
        if not args:
            self.raw(cmd)
            return
        if len(args) == 1:
            self.raw("%s %s" % (cmd.upper(), args[0]))
            return
        if len(args) == 2:
            self.raw("%s %s :%s" % (cmd.upper(), args[0], " ".join(args[1:])))
            return
        if len(args) >= 3:
            self.raw("%s %s %s :%s" % (cmd.upper(), args[0], args[1], " ".join(args[2:])))
            return

    def connect(self, server, nick):
        "connect to server"
        nr = 0
        while not self.stopped:
            self.state.nrconnect += 1
            if self._connect(server):
                break
            time.sleep(10.0)
            nr += 1
        else:
            self._connected.set()
        self._connected.wait()
        self.logon(server, nick)

    def handle(self, event):
        "invoke callback"
        if event.command in self.cbs:
            self.cbs[event.command](event)

    def doconnect(self):
        "start input/output tasks"
        assert self.cfg.server
        assert self.cfg.nick
        super().start()
        self.connect(self.cfg.server, self.cfg.nick)
        launch(self.input)
        launch(self.output)

    def input(self):
        "loop for input"
        while not self.stopped:
            try:
                e = self.poll()
            except (OSError, ConnectionResetError, socket.timeout) as ex:
                e = Event()
                e.error = str(ex)
                self.ERROR(e)
                break
            if not e:
                break
            if not e.orig:
                e.orig = repr(self)
            self.handle(e)

    def joinall(self):
        "all channels"
        for channel in self.channels:
            self.command("JOIN", channel)

    def logon(self, server, nick):
        "do logon handshake"
        self._connected.wait()
        assert self.cfg.username
        assert self.cfg.realname
        self.raw("NICK %s" % nick)
        self.raw("USER %s %s %s :%s" % (self.cfg.username, server, server, self.cfg.realname))

    def output(self):
        "loop for output"
        while 1:
            channel, txt = self._outqueue.get()
            if channel is None:
                break
            if txt:
                time.sleep(0.001)
                self._say(channel, txt)

    def poll(self):
        "block on socket"
        self._connected.wait()
        if not self._buffer:
            self._some()
        if not self._buffer:
            return self._parsing("")
        e = self._parsing(self._buffer.pop(0))
        if op.debug and e.rawstr:
            print(e.rawstr.rstrip())
        cmd = e.command
        if cmd == "PING":
            self.state.pongcheck = True
            self.command("PONG", e.txt or "")
        elif cmd == "PONG":
            self.state.pongcheck = False
        if cmd == "001":
            self.state.needconnect = False
            if "servermodes" in dir(self.cfg):
                self.raw("MODE %s %s" % (self.cfg.nick, self.cfg.servermodes))
            self.joinall()
        elif cmd == "366":
            self._joined.set()
        elif cmd == "433":
            nick = self.cfg.nick + "_"
            self.cfg.nick = nick
            self.raw("NICK %s" % self.cfg.nick or "operbot")
        return e

    def raw(self, txt):
        "send on raw socket"
        txt = txt.rstrip()
        if not txt.endswith("\r\n"):
            txt += "\r\n"
        txt = txt[:512]
        txt = bytes(txt, "utf-8")
        self._connected.wait()
        try:
            self._sock.send(txt)
        except (OSError, ConnectionResetError) as ex:
            e = Event()
            e.error = str(ex)
            self.LOG(e)
            self._connected.clear()
        self.state.last = time.time()
        self.state.nrsend += 1

    def say(self, channel, txt):
        "forward to output loop"
        self._outqueue.put_nowait((channel, txt))

    def start(self, cfg=None):
        "connect to server"
        if cfg is not None:
            op.update(self.cfg, cfg)
        else:
            last(self.cfg)
        assert self.cfg.channel
        assert self.cfg.server
        self.channels.append(self.cfg.channel)
        self._joined.clear()
        launch(self.doconnect)
        self._joined.wait()

    def stop(self):
        "flush queues and shutdown sockets"
        super().stop()
        self._outqueue.put((None, None))
        try:
            self._sock.shutdown(2)
        except OSError:
            pass

    def ERROR(self, event):
        "do stop/start on error"
        self.state.nrerror += 1
        self.state.error = event.error
        self._connected.clear()
        self.stop()
        self.start()

    def JOINED(self, event):
        "has joined all channels"
        self._joined.set()

    def LOG(self, event):
        "log to console, override this"

    def NOTICE(self, event):
        "respond with version of the bot"
        from op import __version__
        if event.txt.startswith("VERSION"):
            txt = "\001VERSION %s %s - %s\001" % ("OP", __version__, "Object Programming")
            self.command("NOTICE", event.channel, txt)

    def PRIVMSG(self, event):
        "forward dcc chat and check for commands"
        if event.txt.startswith("DCC CHAT"):
            if not self.users.allowed(event.origin, "USER"):
                return
            try:
                dcc = DCC()
                dcc.encoding = "utf-8"
                dcc.clone(self)
                launch(dcc.connect, event)
                return
            except ConnectionError as ex:
                return
        if event.txt and event.txt[0] == self.cc:
            if not self.users.allowed(event.origin, "USER"):
                return
            event.type = "cmd"
            event.txt = event.txt[1:]
            super().dispatch(event)

    def QUIT(self, event):
        "stop if self"
        if self.cfg.server in event.orig:
            self.stop()

class DCC(Handler):

    "direct client to client (dcc)"

    def __init__(self):
        super().__init__()
        self._connected = threading.Event()
        self._sock = None
        self._fsock = None
        self.encoding = "utf-8"
        self.origin = ""

    def raw(self, txt):
        "send text on the dcc socket"
        self._fsock.write(str(txt).rstrip())
        self._fsock.write("\n")
        self._fsock.flush()

    def announce(self, txt):
        "annouce to dcc console, overload this"

    def connect(self, event):
        "connect to offering socket"
        arguments = event.txt.split()
        addr = arguments[3]
        port = arguments[4]
        port = int(port)
        if ':' in addr:
            s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((addr, port))
        s.setblocking(1)
        #os.set_inheritable(s.fileno(), os.O_RDWR)
        self._sock = s
        self._fsock = self._sock.makefile("rw")
        self.raw('Welcome to Object Programming %s' % op.__version__)
        self.origin = event.origin
        launch(self.input)
        super().start()
        self._connected.set()

    def input(self):
        "loop for input"
        while 1:
            try:
                e = self.poll()
            except EOFError:
                break
            self.put(e)

    def poll(self):
        "poll (blocking) for input and create an event for it"
        self._connected.wait()
        e = Event()
        e.type = "cmd"
        txt = self._fsock.readline()
        txt = txt.rstrip()
        parse(e, txt)
        e._sock = self._sock
        e._fsock = self._fsock
        e.channel = self.origin
        e.origin = self.origin or "root@dcc"
        e.orig = repr(self)
        return e

    def say(self, channel, txt):
        "skip channel and print on socket"
        self.raw(txt)
