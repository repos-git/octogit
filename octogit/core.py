"""
octogit

This file contains stuff for github api
"""

import sys
import shlex
import urllib
import subprocess


import simplejson
from clint.textui import colored, puts, indent
from git import Repo


ISSUES_ENDPOINT = 'https://api.github.com/repos/%s/%s/issues'
SINGLE_ISSUE_ENDPOINT = 'https://api.github.com/repos/%s/%s/issues/%s'


def get_repository():
    get_top_level_repo = 'git rev-parse --show-toplevel'
    args = shlex.split(get_top_level_repo)

    work_path = subprocess.Popen(args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

    stdout, sterr = work_path.communicate()

    if stdout:
        return Repo(stdout.rstrip('\n'))
    else:
        puts(colored.red('Not a git repository')) 
        sys.exit(0)

def get_single_issue(user, repo, number):
    url = SINGLE_ISSUE_ENDPOINT % (user, repo, number)
    print url
    import pdb; pdb.set_trace()
    connect = urllib.urlopen(url)
    json_data = simplejson.load(connect)
    issue_info = '    '.join((
            '{0}'.format(colored.green(json_data['number'])),
            '{0}'.format(colored.red(json_data['user']['login'])),
            '{0}'.format(json_data['title']),
            '{0}'.format(json_data['body'])
            ))
    puts(issue_info)

def get_issues(user, repo):
    url = ISSUES_ENDPOINT % (user, repo)
    print url 
    connect = urllib.urlopen(url)
    json_data = simplejson.load(connect)
    try:
        json_data['message']
        puts(colored.cyan('Yay! No issues yet...'))
        return
    except:
        pass
    if len(json_data) == 0 :
        puts(colored.cyan('Yay! No issues yet...'))
        return
    puts('Issues: ')
    for i in json_data:
        issue_info = '    '.join((
                '{0}'.format(colored.yellow(i['number'])),
                '{0}'.format(colored.yellow(i['user']['login'])),
                '{0}'.format(i['title'])
                ))
        puts(issue_info)