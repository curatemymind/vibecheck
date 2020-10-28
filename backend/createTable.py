import pymysql

db = pymysql.connect('vibecheckdb.cfmab8sxzhn7.us-east-2.rds.amazonaws.com', 'admin', 'rootroot')

cursor = db.cursor()

#code that creates a new db
#sql = '''create database testing2'''
#cursor.execute(sql)

#chooses db to work off of
sql = '''use testing2'''
cursor.execute(sql)

#prints out tables in the db
sql = '''show tables'''
cursor.execute(sql)
print(cursor.fetchall())
