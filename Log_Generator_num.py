# -*- coding:utf-8 -*-

# [Log Generator num ver.]
# Author : DenverAlmighty
# Latest update : 2022.07.15
# Version : 0.1.1
# Generate roughly 9500 logs per second


import os
import datetime
import time

cnt = 0

def initPage():
    name = """
        _____                      _____                                                             
    __|_    |__ _____ ______   __|___  |__ ______ ____   _ ______ _____  ____    __   _____ _____   
    |    |      /     \   ___| |   ___|    |   ___|    \ | |   ___|     ||    \ _|  |_/     \     |  
    |    |_     |     |   |  | |   |  |    |   ___|     \| |   ___|     \|     \_    _|     |     \  
    |______|  __\_____/______| |______|  __|______|__/\____|______|__|\__\__|\__\|__| \_____/__|\__\ 
        |_____|                    |_____|                                                            
                                                                                                    
    """

    print(name)


def main(pnum):
    global cnt
    #argparse
    print('===== Log Generator Started =====')

    log_path = '/tmp/'

    while True:
        # execute log_gen function
        today = datetime.datetime.today()
        mylog = '%s %s %d \n' % (today.strftime('%Y-%m-%d %H:%M:%S:%f'), pnum, cnt) + '%s %s %d \n' % (today.strftime('%Y-%m-%d %H:%M:%S:%f'), pnum, cnt+1) + '%s %s %d \n' % (today.strftime('%Y-%m-%d %H:%M:%S:%f'), pnum, cnt+2) + '%s %s %d \n' % (today.strftime('%Y-%m-%d %H:%M:%S:%f'), pnum, cnt+3) + '%s %s %d \n' % (today.strftime('%Y-%m-%d %H:%M:%S:%f'), pnum, cnt+4) + '%s %s %d \n' % (today.strftime('%Y-%m-%d %H:%M:%S:%f'), pnum, cnt+5) + '%s %s %d \n' % (today.strftime('%Y-%m-%d %H:%M:%S:%f'), pnum, cnt+6) + '%s %s %d \n' % (today.strftime('%Y-%m-%d %H:%M:%S:%f'), pnum, cnt+7) + '%s %s %d \n' % (today.strftime('%Y-%m-%d %H:%M:%S:%f'), pnum, cnt+8) + '%s %s %d' % (today.strftime('%Y-%m-%d %H:%M:%S:%f'), pnum, cnt+9) 
        # set file path + file name
        filename = log_path + today.strftime('%Y-%m-%d') + '_Log_Generator.txt'
        # Save as file
        with open(filename, 'a+') as f:
            f.write(mylog)
        cnt += 10
        print(mylog)

if __name__=='__main__':
    initPage()
    start_time = time.time()
    # main('p0')
    try:
        main('p0')
    except :
        execute_time = round((time.time() - start_time), 2)
        print('==== Execute Time : %s seconds ====' % execute_time)
        print('==== Generated Log Count : %s ====' % cnt)
        print('==== %d per seconds' % round(cnt/execute_time, 3))
