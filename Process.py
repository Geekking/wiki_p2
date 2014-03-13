#encoding:utf-8

import MySQLdb
from Queue import Queue  

from ProCostomer import Producer
from ProCostomer import Consumer
import ConstValue as cv
import Db as db
import time

def main():
    sTime = time.time()
    try:
        conn=MySQLdb.connect(host='localhost',user='root',passwd='627116',charset='utf8',port=3306)
        cur=conn.cursor() 
        conn.select_db(cv.database)
        
        cur.execute("DROP TABLE IF EXISTS `wordlinks`;")
        cur.execute("CREATE TABLE `wordlinks` ( `word` varchar(100) NOT NULL ,`colwords` longtext) ENGINE=InnoDB AUTO_INCREMENT=332485 DEFAULT CHARSET=utf8mb4;")
        print "create wordlinks table success"
        count=cur.execute('select * from article where 1')
        
        print 'there has %s rows record' % count
    
        results=cur.fetchall()
        queue = Queue()  
  
        producer = Producer('Pro.', queue,results)  
    
        consumer = Consumer('Con.', queue)  
    
        producer.start()  
  
        consumer.start()  
  
        producer.join()  
  
        consumer.join()  
        #
        cur.execute("DROP TABLE IF EXISTS `newLinks`;")
        cur.execute("create table newLinks select word,group_concat(colwords separator '|') as colwords from wordlinks group by word;")
        conn.commit()
        cur.close()
        conn.close()
        eTime = time.time()
        print '用时：'+str((eTime - sTime)/60) +" min"
        
    except MySQLdb.Error,e:
         print "Mysql Error %d: %s" % (e.args[0], e.args[1])
 
if __name__ == '__main__':  
  
    main()  
    
