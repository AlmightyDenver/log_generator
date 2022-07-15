# -*- coding:utf-8 -*-

# [Log Generator num multi ver.]
# Author : DenverAlmighty
# Latest update : 2022.07.15
# Version : 0.1.1
# Generate roughly 350,000 logs per second


import os
import datetime
import time
import multiprocessing

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
    my_list=['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10', 'p11', 'p12', 'p13', 'p14', 'p15', 'p16']
    pool=multiprocessing.Pool(processes=16)
    pool.map(main, my_list)
    pool.close()
    pool.join()