'''
Created on Mar 8, 2014

@author: apple
'''
# producer_consumer_queue  
  
from Queue import Queue  
  
import random  
  
import threading  
  
import time  

import ConstValue as cv
   
import sys

import Db as db
import string
#Producer thread  

class Producer(threading.Thread):  
  
    def __init__(self, t_name, queue,results):  
  
        threading.Thread.__init__(self, name=t_name)  
        self.data=queue  
        self.results  = results;
        self.remain = ''
        self.windownsLeng = cv.windowsLength
            
    def extractWordlinks(self,aPage):
        text = aPage[2]+aPage[4]
        anchors = aPage[3] +'|'+aPage[5]
        anchorlist = string.split(anchors,'|')
        cutLength =  len(text)/10
        textPoint = -1
        #print anchorlist
        anchorPoint = 0
        val = dict()
        curHead = -1
        curKey = ''
        while(True):
            textPoint = text.find(anchorlist[anchorPoint])
            if textPoint == -1:
                anchorPoint += 1
                if anchorPoint >= len(anchorlist):
                    break
            else:
                textPoint += len(anchorlist[anchorPoint])
                val[anchorlist[anchorPoint]] = [];
                curHead = textPoint
                curKey = anchorlist[anchorPoint]
                break
        anchorPoint += 1
        if curHead <0:
            return val
        times = 1
        while(True):
            if anchorPoint >= len(anchorlist):
                    return val
            anchorlist[anchorPoint] = anchorlist[anchorPoint].strip();
            if anchorlist[anchorPoint] == "":
                anchorPoint += 1
                continue
            tempTextPoint = text.find(anchorlist[anchorPoint],textPoint)
            #print textPoint,tempTextPoint,anchorlist[anchorPoint]
            
            if tempTextPoint == -1 or tempTextPoint - textPoint > times*cutLength:
                if tempTextPoint == -1:
                    tempTextPoint = text.find(anchorlist[anchorPoint],0)
              #      print "NWE ::"+str(tempTextPoint)
                times *=2    
                anchorPoint += 1
            
            
            else:
                times =1
                textPoint  = tempTextPoint
                textPoint += len(anchorlist[anchorPoint])
                if textPoint - curHead <= self.windownsLeng:
                    val[curKey].append(anchorlist[anchorPoint]);
                else:
                    curKey = anchorlist[anchorPoint]
                    curHead  = textPoint
                    if curKey not in val.keys():
                        val[curKey] = []
                anchorPoint +=1 
            
        return val
    def run(self):  
        
        for row in self.results:  
            val = self.extractWordlinks(row)
            for key in val.keys():
                self.data.put( (key.replace('\'','\'\''),('|'.join(val[key])).replace('\'','\'\'')) )  
  
  
   
  
#Consumer thread  
  
class Consumer(threading.Thread):  
  
    def __init__(self, t_name, queue):  
  
        threading.Thread.__init__(self, name=t_name)  
        self.data=queue  
        self.conn = db.pre()
            
    def run(self):  
        while not self.data.empty():
            alink = self.data.get()
            
            self.insertIntoDb(alink)
            
    def insertIntoDb(self,alink):
        cur = self.conn.cursor()
        insertSql =  cv.insertSQL%alink
        cur.execute(insertSql)
        self.conn.commit()
   