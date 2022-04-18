# -*- coding:utf-8 -*-

# [Log Generator]
# Author : DenverAlmighty
# Notice : Use at your own risk!
#
# Latest update : 2022.04.13
# Version : 1.0.4

import io, os
import time
import csv, json
import datetime
import random
from faker import Faker
from dicttoxml import dicttoxml
import argparse
import numpy
import socket

def convertLog(log_format, log_dict):
    message = ''

    if log_format == 'csv':
        message=str(list(log_dict.values())).strip('[]')
    elif log_format =='xml':
        message=dicttoxml(log_dict).decode()
    elif log_format == 'txt':
        message=str(log_dict).strip('{|}')
    elif log_format == 'json':
        message=str(log_dict)
    # print(' : ' + message)
    # print( message)
    return message


def log_gen(time_loc,log_format,time_format, send_log):
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
    response=['200','404','500','301']
    verb=['GET','POST','DELETE','PUT']
    resources=['/list','/wp-content','/wp-admin','/explore','/search/tag/list','/app/main/posts','/posts/posts/explore','/apps/cart.jsp?appID=']
    uri = random.choice(resources)
    if uri.find('apps')>0:
        uri += str(random.randint(1000,10000))
    resp = numpy.random.choice(response,p=[0.9,0.04,0.02,0.04])
    byt = int(random.gauss(5000,50))
    useragent = numpy.random.choice(ualist,p=[0.5,0.3,0.1,0.05,0.05] )()
    # Create events with more than 10000 characters
    if (send_log == 'none' and  numpy.random.choice([0,1], p=[0.95, 0.05])):
        tenth = 'LOG_TEST message 10000 ABCDEFGHIJKLMNOPQRSTUBWXYZ ' * 200
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



def main():
    #argparse
    print('===== Log Generator Started =====')
    parser = argparse.ArgumentParser(description='Random Log Generator', add_help=True)
    parser.add_argument('--log_path', '-p', dest='log_path', help='default : ./', default='')
    parser.add_argument('--log_format', '-l', dest='log_format', help='Select log format', choices=['csv','json', 'txt', 'xml'], default='csv' )
    parser.add_argument('--send_log', '-s', dest='send_log', help='Send Log', choices=['none','tcp', 'udp'], default='none' )
    parser.add_argument('--time-format', '-tf', dest='time_format', help='Set time format 1 : %%Y-%%m-%%d %%H:%%M, 2 : %%Y/%%m/%%d %%H:%%M:%%S\n', choices=[1, 2], default=1, type=int )
    parser.add_argument('--time_location', '-t', dest='time_location', help='Setting the location of datetime(0~7).-1 : the end of row', default=0, type=int)
    parser.add_argument('--dest_ip', '-di', dest='dest_ip', help='Dest IP', default='172.20.1.35' )
    parser.add_argument('--dest_port', '-dp', dest='dest_port', help='Dest PORT', default='10514', type=int)
    args = parser.parse_args()

    log_path = args.log_path
    time_loc = args.time_location
    log_format = args.log_format
    dest_ip = args.dest_ip
    dest_port = args.dest_port
    send_log = args.send_log
    time_format = '%Y-%m-%d %H:%M:%S' if args.time_format == 1 else '%Y/%m/%d %H:%M:%S'


    while True:
        # execute log_gen functin
        mylog = log_gen(time_loc,log_format,time_format, send_log )
        # set file path + file name
        filename = log_path + datetime.datetime.today().strftime('%m-%d-%Y') + '_Log_Generator.' + log_format
        # print(log_path)

        # Save as file
        # Save as CSV
        
        if send_log == 'none':
            if log_format == 'csv':
                # header list
                header_list=list(mylog.keys())
                if os.path.isfile(filename):
                    with open(filename, 'a', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=header_list)
                        writer.writerow(mylog)
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
                mylog=dicttoxml(mylog).decode()
                with open(filename, 'a+') as f:
                    f.write(mylog)
                    f.write('\n')
        elif send_log == 'tcp':
            # init socket
            sock = None
            # create socket ?
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Set timeout
            timeout=5
            sock.settimeout(timeout)
            # Set dest address
            serverAddress = (dest_ip, dest_port)
            # Connect
            sock.connect(serverAddress)
            # print(sock.recv(1024))
            # Message to send
            message = convertLog(log_format, mylog).encode()
            # Send Message
            sock.sendall(message)
            # Close socket
            sock.close()
        elif send_log == 'udp':
            sock = None
            message = convertLog(log_format, mylog).encode()
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            timeout=5
            sock.settimeout(timeout)
            sock.sendto(message, (dest_ip, dest_port))
            sock.close()

        time.sleep(5)


if __name__=='__main__':
    main()
