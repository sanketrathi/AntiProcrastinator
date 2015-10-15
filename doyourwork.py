#!/usr/bin/env python
import sys
import argparse
import subprocess
import time


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(description='Protects you from procrastinating.')
    parser.add_argument('--workspace', help='Workspace where you are working', default='1')
    parser.add_argument('--time', help='Time you are allowed to stay outside workspace, in seconds', type=int, default=60)
    parser.add_argument('--sleep', help='Sleep time between workspace checking, in seconds', type=int, default=10)

    args = parser.parse_args()
    watch_workspace = args.workspace
    allowed_tp_time = args.time
    sleep_time = args.sleep
    time_since_last_change = 0

    print 'Watching workspace - {watch_workspace} with buffer time - {allowed_tp_time}.'.format(
        watch_workspace=watch_workspace, allowed_tp_time=allowed_tp_time
    )

    cmd = ['xprop', '-root', '-notype', '_NET_CURRENT_DESKTOP']
    while True:
        x = subprocess.check_output(cmd).strip('\n').split(' = ')[-1]
        if x is not watch_workspace:
            time_since_last_change += sleep_time
        else:
            time_since_last_change = 0
        if time_since_last_change >= allowed_tp_time:
            subprocess.call(['notify-send', 'FUCKING GET BACK TO WORK!'])
            time_since_last_change = 0
        time.sleep(sleep_time)

if __name__ == '__main__':
    exit(main())
