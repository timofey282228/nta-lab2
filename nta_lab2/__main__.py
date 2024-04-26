import argparse
import os
import signal
import subprocess
import time
from datetime import datetime
from queue import Empty
from time import sleep

from ._task_interop import *
from .bruteforce import bruteforce
from .sph import silver_pohlig_hellman

GET_TASK_DELAY = 10 * 60
GET_SOLUTION_DELAY = 5 * 60


def watchdog(initial_delay, update_queue: Queue):
    log = logging.getLogger("WATCHDOG")
    log.debug("Watchdog %d starting", threading.get_ident())
    sleep(initial_delay)
    while True:
        try:
            d = update_queue.get_nowait()
            if d:
                log.debug("Resetting watchdog, delay: %d", d)
                sleep(d)
            else:
                log.debug("Watchdog %d exiting", threading.get_ident())
                break
        except Empty:
            log.error("Timed out")
            os.kill(os.getpid(), signal.SIGTERM)  # rude!


# simple one-shot watchdog interface
def wd(delay):
    wdq = Queue()
    wd = threading.Thread(target=watchdog, args=(delay, wdq))
    wd.daemon = True
    wd.start()
    return wdq


def benchmark(args):
    rc = 0
    try: rc = subprocess.run("docker --version", shell=True, capture_output = True).returncode
    except FileNotFoundError: rc = -1
    finally:
        if rc:
            logging.error("Can not run benchmark: docker not available")
            exit(3)

    algo = args.algo

    for l in range(args.l, args.L):
        print(f"Solving tasks of length {l}")
        t = start_task()
        set_length(l, t)
        wq, rq = Queue(), Queue()
        w = Writer(wq, t)
        r = Reader(rq, t)
        w.daemon = True
        r.daemon = True
        w.start()
        r.start()

        for tp in range(1, 3):

            # set up a watchdog
            wdq = wd(GET_TASK_DELAY)

            # get the task
            p = rq.get()

            print("Task type {}:\n a = {}; b = {}; p = {}.".format(tp, *p))
            wdq.put(None)  # wd ok

            # solve it
            wdq = wd(GET_SOLUTION_DELAY)

            # we'll measure execution time
            t = time.perf_counter_ns()
            x = algo(*p)
            t = time.perf_counter_ns() - t

            assert pow(p[0], x, p[2]) == p[1], "WRONG"
            wdq.put(None)  # wd ok
            print(" Solution: x = {}\n".format(x))

            # append stats
            if args.o:
                with open(args.o, "at") as f:
                    f.write("{},{},{},{},{},{},{}\n".format(tp, l, p[0], p[1], p[2], x, t))

            # send the solution
            wq.put(x)

            # exit watchdog
            wdq.put(None)

        # exit writer
        wq.put(None)
        w.join()


def solver(args):
    algo = args.algo
    p = (args.a, args.b, args.p)
    print(datetime.now())

    print("Solving a = {}; b = {}; p = {}".format(*p))
    x = algo(*p)
    print(f"x = {x}")
    assert pow(p[0], x, p[2]) == p[1], "WRONG"

    print(datetime.now())


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()

    argparser.add_argument(
        "-v", help="verbose (debug) output", action="store_true", dest="verbose"
    )

    algo_grp = argparser.add_mutually_exclusive_group(required=True)
    algo_grp.add_argument(
        "--bruteforce", action="store_const", const=bruteforce, dest="algo"
    )
    algo_grp.add_argument(
        "--sph", action="store_const", const=silver_pohlig_hellman, dest="algo"
    )

    subps = argparser.add_subparsers(dest="command")

    solver_parser = subps.add_parser(
        "solver", help="Run selected algorithm to solve one task"
    )
    solver_parser.add_argument_group("Task parameters")
    solver_parser.add_argument("a", type=int)
    solver_parser.add_argument("b", type=int)
    solver_parser.add_argument("p", type=int)

    benchmark_parser = subps.add_parser(
        "benchmark",
        help='Test the implementation with generated tasks (runs "docker run --rm -i salo1d/nta_cp2_helper:2.0" multiple times under the hood, so requires docker to be available in the execution environment)',
    )
    benchmark_parser.add_argument(
        "-l", help="minimum length", type=int, metavar="l", default=3
    )
    benchmark_parser.add_argument(
        "-L", help="maximum length", type=int, metavar="L", default=100
    )

    benchmark_parser.add_argument("-o", type=str, help="Path to CSV file for stats (will be appended)")

    args = argparser.parse_args()
    # print(args)
    # print(args.o)
    # exit(0)
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    try:
        match args.command:
            case "solver":
                solver(args)
            case "benchmark":
                benchmark(args)

    except KeyboardInterrupt:
        print("Exiting...")
        exit(1)
