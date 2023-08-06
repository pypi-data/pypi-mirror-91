#!/usr/bin/env python3
# Yonghang Wang

import sys
import argparse
import os
import re
import jaydebeapi
import socket
import psutil
import traceback
import json
#from multiprocessing import Process as Task
from threading import Thread as Task
from sretools import SimpleTable

class DBX :
    def __init__(self,jar,driver,url) :
        self.__jar = jar
        self.__driver = driver
        self.__url = url
        self.__conn = None
        self.__cursor = None
    def close(self) :
        try :
            self.__cursor.close()
            self.__conn.close()
        except :
            pass
    def get_connection(self) :
        if not (self.__conn and self.__cursor) :
            self.__conn = jaydebeapi.connect(self.__driver, self.__url, jars=self.__jar)
            self.__cursor = self.__conn.cursor()
    def run_sql(self,sql) :
        self.__cursor.execute(sql)
        rchg = self.__cursor.rowcount
        result = dict()
        result["sql"] = sql
        result["rows_impacted"] = rchg
        if rchg == -1 :
                data = self.__cursor.fetchall()
                hdr = [d[0] for d in self.__cursor.description]
                result["header"] = hdr
                result["data"] = data
        return json.dumps(result)
    def run_sp(self,sp,args=list()) :
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-J', '--jar', dest='jar', help='jdbc driver jar file')
    parser.add_argument('-D', '--driver', dest='driver', help='jdbc driver name')
    parser.add_argument('-U', '--url', dest='url', help='jdbc url or connection string')
    parser.add_argument('-C', '--connect', dest='connect', action='store_true', default=False, help='force connect as server')
    parser.add_argument('-Q', '--sql', dest='sql', help='sql statement to run')
    parser.add_argument('-w', '--maxwidth', dest='maxwidth', type=int, default=-1, help='maxwidth of column')
    parser.add_argument('-F', '--outformat', dest='format', default="", help='json,yaml,csv')
    parser.add_argument('-p', '--pivot', dest='pivot', action='store_true', default=False, help='pivot the view')
    parser.add_argument('-X', '--debug', dest='debug', action='store_true', default=False, help='debug mode')
    args = parser.parse_args()

    ppid = os.getppid()
    found = False
    p = ppid
    for d in ["~/.cache","~/.cache/sretools"] :
        fulld = os.path.expanduser(d)
        if not os.path.exists(fulld) :
            os.mkdir(fulld)
    while p not in [0,1] :
        if os.path.exists(os.path.expanduser("~/.cache/sretools/.dbx.{}".format(p))) :
            found = True
            break
        else :
           np = psutil.Process(ppid).ppid()
           if p == np :
               break
           else :
               p = np
    if not found or args.connect :
        addr = os.path.expanduser("~/.cache/sretools/.dbx.{}".format(ppid))
        if os.path.exists(addr) :
            os.remove(addr)
    else :
        # client only
        addr = os.path.expanduser("~/.cache/sretools/.dbx.{}".format(p))
    # server
    if args.connect :
        if not all([args.jar,args.driver,args.url]) :
            print("# Must specify jdbc driver jar(-J), driver(-D) and URL(-U).")
        pid = os.fork()
        # child
        if pid == 0 :
            print("# DBXServer {}@{}".format(os.getpid(),addr))
            dbx = DBX(driver=args.driver,url=args.url,jar=args.jar)
            dbx.get_connection()
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.bind(addr)
            s.listen(1)
            def sqlworker(netconn,sql) :
                try : 
                    result = dbx.run_sql(sql)
                    if args.debug :
                        print("# Sqlworker: result=",result)
                    netconn.send(result.encode())
                except :
                    traceback.print_exc() 
            while True :
                try : 
                    netconn, cltaddr = s.accept()
                    sql = netconn.recv(4096).decode()
                    if args.debug :
                        print("# Eventloop: sql={}".format(sql))
                    if sql == "terminate" :
                        break
                    wk = Task(target=sqlworker,args=(netconn,sql))
                    wk.start()
                except :
                    traceback.print_exc() 
            if os.path.exists(addr) :
                os.unlink(addr)
        # parent
        elif pid > 0 :
            sys.exit(0)
        else :
            print("# Error forking new process ...")
            sys.exit(-1) 
    # client
    else :
        try :
            if args.debug :
                print("# DBXClient {}".format(addr))
            s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            s.connect(addr)
            s.send(args.sql.encode())
            if args.debug :
                print("# Client sent :",args.sql)
            rsp = s.recv(1024*1024).decode()
            if args.debug :
                print("# Client got :",rsp)
            try :
                obj = json.loads(rsp)
            except :
                obj = dict()
            if args.sql != "terminate" and"header" in obj and "data" in obj :
                if args.format == "json" :
                    t = SimpleTable(header=obj["header"],data=obj["data"])
                    print(t.get_json(),end="")
                elif args.format == "yaml" :
                    t = SimpleTable(header=obj["header"],data=obj["data"])
                    print(t.get_yaml(),end="")
                elif args.format == "csv" :
                    t = SimpleTable(header=obj["header"],data=obj["data"])
                    print(t.get_csv(),end="")
                else :
                    t = SimpleTable(header=obj["header"],data=obj["data"],maxwidth=args.maxwidth)
                    if args.pivot :
                        print(t.repr_pivot(),end="")
                    else :
                        print(t,end="")
        except :
            traceback.print_exc() 

if __name__ == "__main__":
    main()
