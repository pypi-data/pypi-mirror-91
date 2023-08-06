# OP - Object Programming (tbl.py)
#
# this file is placed in the public domain

"tables (tbl)"

import op

#:
names = op.Ol({
    "bus": ["op.hdl.Bus"],
    "cfg": ["op.udp.Cfg", "op.Cfg", "op.irc.Cfg", "op.rss.Cfg"],
    "command": ["op.hdl.Command"],
    "dcc": ["op.irc.DCC"],
    "default": ["op.Default"],
    "event": ["op.irc.Event", "op.hdl.Event"],
    "feed": ["op.rss.Feed"],
    "fetcher": ["op.rss.Fetcher"],
    "handler": ["op.hdl.Handler"],
    "irc": ["op.irc.IRC"],
    "log": ["op.cmd.Log"],
    "object": ["op.Object"],
    "ol": ["op.Ol"],
    "repeater": ["op.clk.Repeater"],
    "rss": ["op.rss.Rss"],
    "timer": ["op.clk.Timer"],
    "todo": ["op.cmd.Todo"],
    "udp": ["op.udp.UDP"],
    "user": ["op.usr.User"],
    "users": ["op.usr.Users"]
})
