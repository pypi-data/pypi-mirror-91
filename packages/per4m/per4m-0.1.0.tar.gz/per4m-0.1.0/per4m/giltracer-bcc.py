import argparse
from pathlib import Path
import signal
import sys
import time

from bcc import BPF
import bcc

HERE = Path(__file__).parent
with open(HERE / 'giltracer-bcc.cpp') as f:
    code = f.read()

usage = """
"""

def signal_ignore(signal, frame):
    print()

def main(argv=sys.argv):
    parser = argparse.ArgumentParser(argv[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=usage)
    parser.add_argument('--verbose', '-v', action='count', default=1)
    parser.add_argument('--quiet', '-q', action='count', default=0)
    parser.add_argument('--pid', '-p', help="process id", type=int)

    args = parser.parse_args(argv[1:])
    verbose = args.verbose - args.quiet

    library = '/home/maartenbreddels/github/maartenbreddels/per4m/per4m/pytrace.cpython-37m-x86_64-linux-gnu.so'
    b = BPF(text=code)
    b.attach_uprobe(name=library, sym='pyprobe_function_entry', fn_name="function_entry", pid=args.pid)

    calls = b.get_table("calls")
    exiting = False
    print ("loop")
    done = False
    while not done:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt:
            # exiting = True
            done = True
            signal.signal(signal.SIGINT, signal_ignore)
            print("ok")
            for key, value in calls.items():
                print(key, value)

if __name__ == "__main__":
    main()