# -*- coding:utf-8 -*-

# [Log Generator]
# Author : DenverAlmighty
# Notice : Use at your own risk!
# 
# Latest update : 2022.04.11
# Version : 0.1.0

import io, os
import time
import csv, json
import datetime
import random
from faker import Faker
from dicttoxml import dicttoxml
from xml.dom.minidom import parseString
import logging
import pandas as pd
import argparse
import numpy


def log_gen(time_loc,log_format,time_format):
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
    response=["200","404","500","301"]
    verb=["GET","POST","DELETE","PUT"]  
    resources=["/list","/wp-content","/wp-admin","/explore","/search/tag/list","/app/main/posts","/posts/posts/explore","/apps/cart.jsp?appID="]
    uri = random.choice(resources)
    if uri.find("apps")>0:
        uri += str(random.randint(1000,10000))
    resp = numpy.random.choice(response,p=[0.9,0.04,0.02,0.04])
    byt = int(random.gauss(5000,50))
    useragent = numpy.random.choice(ualist,p=[0.5,0.3,0.1,0.05,0.05] )()
    # Create events with more than 10000 characters
    if numpy.random.choice([0,1], p=[0.95, 0.05]):
        tenth = "LOG_TEST message 10000 ABCDEFGHIJKLMNOPQRSTUBWXYZ " * 200
    else: 
        tenth= "NULL"

    field_list = ["ip", "referer", "uri", "resp", "byt", "useragent", "tenth"]
    
    # Place datetime field in time_loc order
    for i in range(len(field_list)):
        if i == time_loc:
            mylog["datetime"] = time
            mylog[field_list[i]] = locals()[field_list[i]]
        else:
            mylog[field_list[i]] = locals()[field_list[i]]
        
    if time_loc==-1:
            mylog["datetime"] = time
    # print(mylog)

    return mylog



def main():
    #argparse
    print("Log Generator Started")
    parser = argparse.ArgumentParser(description='Random Log Generator')
    parser.add_argument("--log_path", '-p', dest="log_path", help="default : ./", default="./")
    parser.add_argument("--log-format", "-l", dest='log_format', help="Log format, Common or Extended Log Format ", choices=['csv','json', 'txt', 'xml'], default="csv" )
    parser.add_argument("--time-format", "-tf", dest='time_format', help="Time Format : 1 - %Y-%m-%d %H:%M, 2 - %Y/%m/%d %H:%M:%S ", choices=[1, 2], default=1, type=int )
    parser.add_argument("--time_location", "-t", dest="time_location", help="Setting the location of datetime(0~7). -1 : the end of row", default=0, type=int)
    args = parser.parse_args()

    log_path = args.log_path
    time_loc = args.time_location
    log_format = args.log_format
    time_format = "%Y-%m-%d %H:%M:%S" if args.time_format == 1 else "%Y/%m/%d %H:%M:%S"

    
    while True:
        # execute log_gen functin
        mylog = log_gen(time_loc,log_format,time_format )
        # set file path + file name
        filename = log_path + datetime.datetime.today().strftime("%m-%d-%Y") + "_Log_Generator." + log_format

        # Save as file
        # Save as CSV
        if log_format == "csv":
            # header list
            header_list=list(mylog.keys())
            if os.path.isfile(filename):
                with open(filename, 'a', newline='', encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=header_list)
                    writer.writerow(mylog)
            else:
                with open(filename, 'w', newline='', encoding="utf-8") as f:
                    writer = csv.DictWriter(f, fieldnames=header_list)
                    writer.writeheader()
                    writer.writerow(mylog)
        # Save as JSON
        elif log_format == "json":
            with open(filename, "a+") as f:
                json.dump(mylog, f)
        # Save as TXT
        elif log_format == "txt":
            with open(filename, "a+") as f:
                f.write(str(mylog))
        # Save as XML
        elif log_format == "xml":
            mylog=dicttoxml(mylog).decode()
            with open(filename, "a+") as f:
                f.write(mylog)
        
        #Time Sleep
        time.sleep(1)


if __name__=='__main__':
    main()