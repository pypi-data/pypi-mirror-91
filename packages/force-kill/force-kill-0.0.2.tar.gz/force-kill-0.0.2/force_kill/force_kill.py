import os
import signal
import sys


def setup_handler(pid):
    assert pid > 0

    def kill(s, frame):
        os.kill(pid, signal.SIGKILL)
        sys.exit(1)

    signal.signal(signal.SIGINT, kill)
    signal.signal(signal.SIGTERM, kill)
    signal.signal(signal.SIGHUP, kill)
    signal.signal(signal.SIGQUIT, kill)


class ForceKill(object):

    def __enter__(self):
        pid = os.fork()
        if pid > 0:
            setup_handler(pid)
            os.wait()
        else:
            return None

    def __exit__(self, exc_type, exc_value, traceback):
        pass
