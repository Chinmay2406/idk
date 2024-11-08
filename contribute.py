#!/usr/bin/env python
import argparse
import os
from datetime import datetime, timedelta
from subprocess import Popen
import sys

def main(def_args=sys.argv[1:]):
    args = arguments(def_args)
    start_date = datetime(2024, 1, 1, 20, 0)  # Start in 2024
    curr_date = datetime.now()
    directory = 'repository-' + curr_date.strftime('%Y-%m-%d-%H-%M-%S')
    repository = args.repository
    user_name = args.user_name
    user_email = args.user_email
    if repository:
        start = repository.rfind('/') + 1
        end = repository.rfind('.')
        directory = repository[start:end]
    no_weekends = args.no_weekends
    days_before = args.days_before
    days_after = args.days_after
    if days_before < 0 or days_after < 0:
        sys.exit('days_before and days_after must not be negative')
    os.mkdir(directory)
    os.chdir(directory)
    run(['git', 'init', '-b', 'main'])

    if user_name:
        run(['git', 'config', 'user.name', user_name])
    if user_email:
        run(['git', 'config', 'user.email', user_email])

    for day in (start_date + timedelta(n) for n in range(days_before + days_after)):
        if (not no_weekends or day.weekday() < 5):
            for commit_time in (day + timedelta(minutes=m) for m in range(contributions_per_day(args))):
                contribute(commit_time)

    if repository:
        run(['git', 'remote', 'add', 'origin', repository])
        run(['git', 'branch', '-M', 'main'])
        run(['git', 'push', '-u', 'origin', 'main'])

    print('\nRepository generation completed successfully!')

def contribute(date):
    with open(os.path.join(os.getcwd(), 'README.md'), 'a') as file:
        file.write(message(date) + '\n\n')
    run(['git', 'add', '.'])
    run(['git', 'commit', '-m', '"%s"' % message(date), '--date', date.strftime('"%Y-%m-%d %H:%M:%S"')])

def run(commands):
    Popen(commands).wait()

def message(date):
    return date.strftime('Contribution: %Y-%m-%d %H:%M')

def contributions_per_day(args):
    return 50  # Fixed at 50 commits per day

def arguments(argsval):
    parser = argparse.ArgumentParser()
    parser.add_argument('-nw', '--no_weekends', action='store_true', default=False, help="Do not commit on weekends")
    parser.add_argument('-r', '--repository', type=str, required=False, help="Remote git repository link")
    parser.add_argument('-un', '--user_name', type=str, required=False, help="Overrides git user.name")
    parser.add_argument('-ue', '--user_email', type=str, required=False, help="Overrides git user.email")
    parser.add_argument('-db', '--days_before', type=int, default=365, required=False, help="Days before the start date")
    parser.add_argument('-da', '--days_after', type=int, default=0, required=False, help="Days after the start date")
    return parser.parse_args(argsval)

if __name__ == "__main__":
    main()
