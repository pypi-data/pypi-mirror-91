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
        mode, payload = ev.get('lambdaRun', ['', ''])

        if mode in ['py', 'python']:
            rsp = SimpleNamespace()
            rsp.returncode = 0
            rsp.stdout = sys.stderr = sys.stdout = StringIO()
            try:
                # using run_path offers better traceback than just using `exec(code)`
                fd, fp = mkstemp('.py', dir=mkdtemp())
                with fdopen(fd, 'w') as f:
                    f.write(payload)
                run_path(fp)
            except:
                rsp.returncode = 1
                rsp.stdout.write(format_exc())
            finally:
                rsp.stdout = rsp.stdout.getvalue()

        elif mode in ['sh', 'shell']:
            rsp = run(payload, shell=True, stderr=STDOUT, stdout=PIPE, text=True)

        if 'rsp' in locals():
            return rsp.returncode, rsp.stdout.strip()

        return handler(ev, ctx)

    return wrapped
