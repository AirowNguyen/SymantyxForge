#!/usr/bin/env python3
import argparse
import inspect
import os
import sys
import threading
import time
from datetime import datetime
import psutil   # Windows-safe CPU timing

VERSION = "1.0.0"
LOGFILE = "copilot.log"

def get_cpu_times():
    p = psutil.Process(os.getpid())
    t = p.cpu_times()
    return t.user, t.system

PLACEHOLDERS = {
    "%c": lambda ctx: ctx.get("client", ""),
    "%d": lambda ctx: ctx.get("domain", ""),
    "%e": lambda ctx: ctx.get("event", ""),
    "%f": lambda ctx: ctx.get("function", ""),
    "%g": lambda ctx: ctx.get("generation", ""),
    "%i": lambda ctx: str(threading.get_ident()),
    "%l": lambda ctx: str(ctx.get("line", "")),
    "%m": lambda ctx: ctx.get("module", ""),
    "%n": lambda ctx: ctx.get("name", ""),
    "%p": lambda ctx: str(os.getpid()),
    "%r": lambda ctx: f"{get_cpu_times()[1]:.6f}",  # system CPU time
    "%t": lambda ctx: datetime.now().isoformat(),
    "%u": lambda ctx: f"{get_cpu_times()[0]:.6f}",  # user CPU time
    "%v": lambda ctx: VERSION,
    "%%": lambda ctx: "%",
    "\\n": lambda ctx: "\n",
    "\\r": lambda ctx: "\r",
}

def map_format(fmt: str, ctx: dict) -> str:
    out = fmt
    for key, fn in PLACEHOLDERS.items():
        out = out.replace(key, fn(ctx))
    return out

def log_event(fmt: str, **ctx):
    frame = inspect.stack()[1]
    ctx.setdefault("module", frame.frame.f_globals.get("__name__", ""))
    ctx.setdefault("function", frame.function)
    ctx.setdefault("line", frame.lineno)

    msg = map_format(fmt, ctx)

    with open(LOGFILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

    print(msg)

def main():
    parser = argparse.ArgumentParser(description="Universal Log Mapper")
    parser.add_argument("target", help="html, txt, app, etc.")
    parser.add_argument("-fmt", default="%t [%m:%l] %e", help="format string")
    parser.add_argument("-name", default="log", help="log name")
    args = parser.parse_args()

    ctx = {
        "client": "local",
        "domain": args.target,
        "event": "startup",
        "name": args.name,
        "generation": "0",
    }

    log_event(args.fmt, **ctx)

if __name__ == "__main__":
    main()
