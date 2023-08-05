import sys
from io import StringIO
from os import fdopen
from runpy import run_path
from subprocess import PIPE, STDOUT, run
from tempfile import mkdtemp, mkstemp
from traceback import format_exc
from types import SimpleNamespace


def wrap_handler(handler):
    def wrapped(ev, ctx):
        _run = ev.get('run')
        if _run:
            code, subprocess = _run.get('code'), _run.get('subprocess')
            if code:
                rsp = SimpleNamespace()
                rsp.returncode = 0
                rsp.stdout = sys.stderr = sys.stdout = StringIO()
                try:
                    # using run_path offers better traceback than just using `exec(code)`
                    fd, fp = mkstemp('.py', dir=mkdtemp())
                    with fdopen(fd, 'w') as f: f.write(code)
                    run_path(fp)
                except:
                    rsp.returncode = 1
                    rsp.stdout.write(format_exc())
                finally:
                    rsp.stdout = rsp.stdout.getvalue()

            else:
                rsp = run(subprocess, shell=True, stderr=STDOUT, stdout=PIPE, text=True)

            return rsp.returncode, rsp.stdout

        return handler(ev, ctx)

    return wrapped
