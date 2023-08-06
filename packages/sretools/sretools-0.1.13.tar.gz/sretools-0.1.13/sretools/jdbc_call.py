#!/usr/bin/env python3
# Yonghang Wang

import sys
import argparse
import os
import re
import jaydebeapi
from sretools import SimpleTable

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-J', '--jar', dest='jar', help='jdbc driver jar file')
    parser.add_argument('-D', '--driver', dest='driver', help='jdbc driver name')
    parser.add_argument('-U', '--url', dest='url', help='jdbc url or connection string')
    parser.add_argument('-Q', '--sql', dest='sql', help='sql statement to run')
    parser.add_argument('-w', '--maxwidth', dest='maxwidth', type=int, default=-1, help='maxwidth of column')
    parser.add_argument('-F', '--outformat', dest='format', default="", help='json,csv')
    parser.add_argument('-v', '--pivot', dest='pivot', action='store_true', default=False, help='pivot the view')
    parser.add_argument('-X', '--debug', dest='debug', action='store_true', default=False, help='debug mode')
    args = parser.parse_args()

    if not args.jar :
        print("must specify jdbc driver jar(-J).")
        sys.exit(-1)

    if not args.driver :
        print("must specify jdbc driver name(-D).")
        sys.exit(-1)

    if not args.url :
        print("must specify connection string(-U).")
        sys.exit(-1)

    if not args.sql :
        print("must specify SQL statement(-Q).")
        sys.exit(-1)

    conn = jaydebeapi.connect(args.driver, args.url, jars=args.jar)
    cur = conn.cursor()
    cur.execute(args.sql)
    rchg = cur.rowcount
    if rchg == -1 :
        try :
            data = cur.fetchall()
            hdr = [d[0] for d in cur.description]
            if args.debug :
                print("# header :",hdr)
                print("# data :",data)
            if args.pivot :
                print(SimpleTable(data=data,header=hdr).repr_pivot(),end="")
            else :
                if args.format == "json" :
                    print(SimpleTable(data=data,header=hdr).get_json(),end="")
                    sys.exit(0)
                if args.format == "csv" :
                    print(SimpleTable(data=data,header=hdr).get_csv(),end="")
                    sys.exit(0)
                print(SimpleTable(data=data,header=hdr,maxwidth=args.maxwidth),end="")
        except :
            pass
        finally :
            cur.close()
    else :
        print("# {} rows impacted.".format(rchg))

    conn.close()

# postgresql
# sretools-jdbc-call  -F "/usr/share/java/postgresql.jar" -D "org.postgresql.Driver" -U "jdbc:postgresql://localhost:5432/sample?user=postgres&password=postgres" -Q "select id, count(*)cnt from t1 group by id"
# id cnt 
# ------
# 1  1   
# 2  1 

if __name__ == "__main__":
    main()
