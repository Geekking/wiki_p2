'''
Created on Mar 8, 2014

@author: apple
'''
import ConstValue as cv
import MySQLdb
import sys

def pre():
        try:
            conn=MySQLdb.connect(host='localhost',user='root',passwd='627116',charset='utf8',port=3306)
            conn.select_db(cv.database)
            return conn
        except MySQLdb.Error,e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])  
            sys.exit()
