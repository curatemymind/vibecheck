import pymysql

db = pymysql.connect('vibecheckdb.cfmab8sxzhn7.us-east-2.rds.amazonaws.com', 'admin', 'rootroot')

cursor = db.cursor()

#this create table command creates a table
cursor.execute("DROP TABLE hi")
 