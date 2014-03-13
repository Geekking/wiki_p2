'''
Created on Mar 8, 2014

@author: apple
'''

database  = "wikipedia"
createTableSQL = '''DROP TABLE IF EXISTS `wordlinks`;
                CREATE TABLE `wordlinks` ( `word` varchar(100) NOT NULL ,`colwords` longtext) ENGINE=InnoDB AUTO_INCREMENT=332485 DEFAULT CHARSET=utf8mb4;'''
insertSQL = 'INSERT INTO `wordlinks`(`word`, `colwords`) VALUES (\'%s\',\'%s\')'

windowsLength = 500;