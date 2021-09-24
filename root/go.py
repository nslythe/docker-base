import subprocess
import time
import signal
import sys
import os

runner = None

description = [
    "https://github.com/nslythe",
]

def sig_handler(signum, frame):
    global runner
    print ("signal %s received" % signum)
    runner.stop()

signal.signal(signal.SIGINT, sig_handler)
signal.signal(signal.SIGTERM, sig_handler)
signal.signal(signal.SIGABRT, sig_handler)

def print_description(runner):
    print("=" * 80)
    for l in description:
        print (l)
    print ("=" * 80)
    for l in runner.description():
        print (l)
    print ("=" * 80)

def config_runner(runner):
    runner.config()

def run_runner(runner):
    code = runner.run()
    if code is None:
        code = -1
    print ("Application finished %s" % code)

def main():
    global runner
    if os.path.isfile("/run.py"):
        sys.path.append("/")
        import run
        runner = run.Run()
        print_description(runner)
        config_runner(runner)
        run_runner(runner)
    else:
        print ("/run.py is not present")

if __name__ == "__main__":
    main()

