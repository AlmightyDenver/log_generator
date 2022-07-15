# -*- coding:utf-8 -*-

# [Log Generator]
# Author : DenverAlmighty
# Latest update : 2022.07.15
# Version : 0.6.1
# Generate avg 15 logs per second

import os
import csv
import json
import datetime
import random
import argparse
import socket
import time
from faker import Faker
import numpy

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

def dict2xml(dict_obj, line_padding=""):
    result_list = list()

    dict_obj_type = type(dict_obj)

    if dict_obj_type is list:
        for sub_elem in dict_obj:
            result_list.append(dict2xml(sub_elem, line_padding))
        return "".join(result_list)

    if dict_obj_type is dict:
        for tag_name in dict_obj:
            sub_obj = dict_obj[tag_name]
            result_list.append("%s<%s>" % (line_padding, tag_name))
            result_list.append(dict2xml(sub_obj, "" + line_padding))
            result_list.append("%s</%s>" % (line_padding, tag_name))

        return "".join(result_list)

    return "%s%s" % (line_padding, dict_obj)

# Create dictionary type log
def log_gen(time_loc, log_format, time_format, send_type):
    # create empty dictionary
    mylog = {}

    #make random data using faker
    faker = Faker()
    ip = faker.ipv4()
    referer = faker.uri()
    ualist = [faker.firefox, faker.chrome, faker.safari, faker.internet_explorer, faker.opera]

    # make time field like time_format
    time = datetime.datetime.now().strftime(time_format)

    # make random data using random
    log_format = [log_format][0]
    response=['200', '404', '500', '301']
    verb=['GET', 'POST', 'DELETE', 'PUT']
    resources=['/list', '/wp-content', '/wp-admin', '/explore', '/search/tag/list', '/app/main/posts',\
        '/posts/posts/explore', '/apps/cart.jsp?appID=']
    uri = random.choice(resources)
    if uri.find('apps')>0:
        uri += str(random.randint(1000, 10000))
    resp = numpy.random.choice(response,p=[0.9, 0.04, 0.02, 0.04])
    byt = int(random.gauss(5000, 50))
    useragent = numpy.random.choice(ualist,p=[0.5, 0.3, 0.1, 0.05, 0.05])()
    # Create events with more than 10000 characters
    if (send_type == 'none' and  numpy.random.choice([0,1], p=[0.95, 0.05])):
        # tenth = 'LOG_TEST message 10000 ABCDEFGHIJKLMNOPQRSTUBWXYZ ' * 200
        tenth = 'LOG_TEST message 10000 ABCDEFGHIJKLMNOPQRSTUBWXYZ ' 
    else:
        tenth= 'NULL'

    field_list = ['log_format', 'ip', 'referer', 'uri', 'resp', 'byt', 'useragent', 'tenth']

    # Place datetime field in time_loc order
    for i in range(len(field_list)):
        if i == time_loc:
            mylog['datetime'] = time
            mylog[field_list[i]] = locals()[field_list[i]]
        else:
            mylog[field_list[i]] = locals()[field_list[i]]
    # add datetime field at last
    if time_loc==-1:
        mylog['datetime'] = time
    # print(mylog)

    return mylog

# Convert log format as string
def convert_log(log_format, log_dict):
    message = ''
    if log_format == 'csv':
        message=str(list(log_dict.values())).strip('[]')
    elif log_format =='xml':
        message=dict2xml(log_dict)
        print(message)
    elif log_format == 'txt':
        message=str(log_dict).strip('{|}')
    elif log_format == 'json':
        message=str(log_dict)
    # print( message)
    return message

# Save Log
def save_log(log_format, filename, mylog):
    if log_format == 'csv':
        # header list
        header_list=list(mylog.keys())
        # if file not exist, create new file and save header before save row
        if os.path.isfile(filename):
            with open(filename, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=header_list)
                writer.writerow(mylog)
        # if file already exist, save only row not header.
        else:
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=header_list)
                writer.writeheader()
                writer.writerow(mylog)
    # Save as JSON
    elif log_format == 'json':
        with open(filename, 'a+') as f:
            json.dump(mylog, f)
    # Save as TXT
    elif log_format == 'txt':
        mylog=str(mylog).strip('{|}') + '\n'
        with open(filename, 'a+') as f:
            f.write(mylog)
    # Save as XML
    elif log_format == 'xml':
        # mylog=dicttoxml(mylog).decode() 
        # print(mylog)
        mylog=dict2xml(mylog)
        with open(filename, 'a+') as f:
            f.write(mylog)
            f.write('\n')


# Send Log 
def send_log(type, dest_ip, dest_port, log_format, mylog):
    # init socket
    sock = None
    # Set timeout
    timeout=5
    # Set dest address
    addr = (dest_ip, dest_port)
    # Message to send
    message = convert_log(log_format, mylog).encode()
    sent=0
    try:
        if type=='tcp':
            # create socket ?
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            # Connect
            sock.connect(addr)
            # Send Message
            sent = sock.sendall(message)
        elif type == 'udp':
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout)
            sent = sock.sendto(message, (dest_ip, dest_port))
    except Exception as e:   
        print('Exception : .', e)
    if sent ==0:
        raise RuntimeError("socket connection broken")
    print(sent)
    # Close socket
    sock.close()

def main():
    #argparse
    print('===== Log Generator Started =====')
    parser = argparse.ArgumentParser(description='Random Log Generator', add_help=True)
    parser.add_argument('--log_path', '-p', dest='log_path', help='default : /tmp/ (ex /my/path/)', default='/tmp/2')
    parser.add_argument('--log_format', '-l', dest='log_format', help='Select log format', choices=['csv','json', 'txt', 'xml'], default='csv')
    parser.add_argument('--time_format', '-tf', dest='time_format', help='Set time format 1 : %%Y-%%m-%%d %%H:%%M, \
        2 : %%Y/%%m/%%d %%H:%%M:%%S\n', choices=[1, 2], default=1, type=int)
    parser.add_argument('--time_location', '-t', dest='time_location', help='Setting the location of datetime(0~7). \
        -1 : the end of row', default=0, type=int)
    parser.add_argument('--send_type', '-s', dest='send_type', help='Send Log', choices=['none','tcp', 'udp'], default='none')
    parser.add_argument('--dest_ip', '-di', dest='dest_ip', help='Dest IP', default='172.20.1.35')
    parser.add_argument('--dest_port', '-dp', dest='dest_port', help='Dest PORT', default='10514', type=int)
    parser.add_argument('--sleep', '-slp', dest='sleep_time', help = 'Sleep time', default=0, type=int)
    args = parser.parse_args()

    log_path = args.log_path
    time_loc = args.time_location
    log_format = args.log_format
    dest_ip = args.dest_ip
    dest_port = args.dest_port
    send_type = args.send_type
    time_format = '%Y-%m-%d %H:%M:%S' if args.time_format == 1 else '%Y/%m/%d %H:%M:%S'
    sleep_time = args.sleep_time

    while True:
        # execute log_gen function
        mylog = log_gen(time_loc,log_format,time_format, send_type)
        # set file path + file name
        filename = log_path + datetime.datetime.today().strftime('%Y-%m-%d') + '_Log_Generator.' + log_format
        # Save as file
        if send_type == 'none':
            save_log(log_format, filename, mylog)
            
        # if send_type == tcp OR udp, Send log
        else:
            send_log(send_type, dest_ip, dest_port, log_format, mylog)
        # except Exception as e:   
        #     print('Exception : .', e)
        # Sleep
        time.sleep(sleep_time)


if __name__=='__main__':
    initPage()
    main()
