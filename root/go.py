import subprocess
import time
import signal
import sys
import os
import threading
import errno
import check_health

class BaseRunner(object):
    def __init__(self):
        pass

    def description(self):
        return [
        ]

    def config(self):
        pass

    def check(self):
        return True

    def run(self):
        return 0

    def stop(self):
        pass

class WatchDog(threading.Thread):
    def __init__(self, runner):
        threading.Thread.__init__(self)
        self.runner = runner
        self.stopping = False

    def stop(self):
        self.stopping = True

    def run(self):
        try:
            os.unlink(check_health.pipe_runner_name)
        except:
            pass
        os.mkfifo(check_health.pipe_runner_name)
        fifor = os.open(check_health.pipe_runner_name, os.O_RDONLY | os.O_NONBLOCK)

        while not self.stopping:
            time.sleep(0.5)
            try:
                request = os.read(fifor, 5)
            except OSError as err:
                if err.errno == errno.EAGAIN or err.errno == errno.EWOULDBLOCK:
                    request = None
                else:
                    raise

            if request is not None and len(request) == 5:
                if request.decode("ascii") == check_health.check_command:
                    health = check_health.not_ok_result
                    if self.runner.check():
                        health = check_health.ok_result
                    print ("Health check : %s" % health)
                    with open(check_health.pipe_watch_name, "w") as fifow:
                       fifow.write(health)

class PythonRunner(BaseRunner):
    def __init__(self):
        sys.path.append("/")
        import run
        self.runner = run.Runner()

    def description(self):
        return  [
            "PythonRunner",
        ]

    def config(self):
        self.runner.config()

    def check(self):
        return self.runner.check()

    def run(self):
        return self.runner.run()

    def stop(self):
        self.runner.stop()


class CmdRunner(BaseRunner):
    def __init__(self):
        pass

class RootRunner(object):
    def __init__(self):
        self.runner = None
        self.watchdog = None

    def stop(self):
        self.watchdog.stop()
        self.runner.stop()

    def run(self):
        self.init_runner()
        self.print_description()
        self.config_runner()
        self.go()

    def init_runner(self):
        if os.path.isfile("/run.py"):
            self.runner = PythonRunner()
        else:
             print ("/run.py is not present")
        self.watchdog = WatchDog(self.runner)

    def print_description(self):
        print("=" * 80)
        print ("https://github.com/nslythe")
        print ("=" * 80)
        for l in self.runner.description():
            print (l)
        print ("=" * 80)

    def config_runner(self):
        self.runner.config()

    def go(self):
        self.watchdog.start()
        code = self.runner.run()
        if code is None:
            code = -1
        print ("Application finished %s" % code)
        return code


if __name__ == "__main__":
    rootrunner = RootRunner()
    def sig_handler(signum, frame):
        print ("signal %s received" % signum)
        rootrunner.stop()

    def main():
        signal.signal(signal.SIGINT, sig_handler)
        signal.signal(signal.SIGTERM, sig_handler)
        signal.signal(signal.SIGABRT, sig_handler)
        rootrunner.run()

    sys.exit(main())

