import pymysql

db = pymysql.connect('vibecheckdb.cfmab8sxzhn7.us-east-2.rds.amazonaws.com', 'admin', 'rootroot')

cursor = db.cursor()



#this create db command is only run once to create a new db instance/cluster
sql = '''create database testing'''
cursor.execute(sql)

#this use command is called anytime to select a db
sql = '''use testing'''
cursor.execute(sql)
#this create table command creates a table
cursor.execute("CREATE TABLE test (dummyData VARCHAR(255))")

#this command pulls all the tables from the current db and prints them
sql = '''show tables'''
cursor.execute(sql)
print(cursor.fetchall())
