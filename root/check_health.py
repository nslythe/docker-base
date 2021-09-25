import os
import sys

pipe_runner_name = "/pipe-runner"
pipe_watch_name = "/pipe-watch"

check_command = "check"
ok_result = "ok"
not_ok_result = "not_ok"

def main():
    try:
        os.mkfifo(pipe_watch_name)
    except:
        pass

    with open(pipe_runner_name, "w") as fifo:
        fifo.write(check_command)

    with open(pipe_watch_name, "r") as fifo:
        result = fifo.read()
        return result == ok_result

if __name__ == "__main__":
    if main():
        sys.exit(0)
    else:
        sys.exit (1)
