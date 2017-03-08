from datetime import datetime
import time

###
# Kyle Beck, 2017-02-12
# This is a logger module that provides an interface for writing strings to a
# log queue that will be dumped to a file if the program ends execution.
###

log = []

outputDir = 'output/'

# Appends a message to the log. Automatically includes timestamp.
def write(msg):
    curTime = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    log.append('[' + curTime + ']:' + msg)

# Dumps the log to a txt document. Document will be timestamped.
def dump():
    fileName = ('Log_' + str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) +
                '.txt')
    with open(outputDir + fileName, 'w', encoding='utf-8') as f:
        for l in log:
            f.write(l + '\n')
