'''
For running program as sub-process and report its pattern extracted log lines to online processors.

Usage
-----
python main.py "sudo docker run -it bluekvirus/xmr-minergate" ".*: (?P<hashrate>.*) H/s.*"

@author Tim Lauv
@created 2017.11.30
'''

import subprocess
import sys
import re

def run(cmd="NOOP", 
        pattern=".*",
        reportTo="https://kafka.innobubble.com",
        token="ENV_VAR",
        topic="GENERAL"):
    '''
    Run the cmd, capture the output matched by pattern then report a topic to HQ using secret token
    '''
    cli = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    line = 'begin capturing...'
    target = re.compile(pattern)
    while line:
        line = str(cli.stdout.readline(), 'utf-8')
        mobj = target.match(line)
        if mobj:
            print(':spotted: ' + line, end="")
            capture = mobj.groupdict().items()
            print('::capture::' + str(capture), end='\r\n')
            #TBI gather additional system info (e.g hostname on Linux, Mac and Windows)
            #TBI send combined msg to HQ

if __name__ == '__main__':
    print('running pyscout as cli')
    run(*sys.argv[1:])
else:
    print('imported pyscout as module, use the run() function')
