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
cursor.execute("CREATE TABLE User( userid INT,first_name VARCHAR(20) NOT NULL, last_name VARCHAR(20) NOT NULL, email VARCHAR(30) NOT NULL, password BINARY(60) NOT NULL, PRIMARY KEY(userid))")
cursor.execute("CREATE TABLE Song(songid INT,song_name VARCHAR(25) NOT NULL, artist VARCHAR(30) NOT NULL, duration TIME,genre VARCHAR(20),PRIMARY KEY (songid))")
cursor.execute("CREATE TABLE Playlist( playlistid INT, playlist_name VARCHAR(20) NOT NULL, vibe VARCHAR(15) NOT NULL, Playlist_duration TIME, userid INT, PRIMARY KEY(playlist_id))")
cursor.execute("CREATE TABLE MovieSuggestion( movieid INT, movie_title VARCHAR(35) NOT NULL, movie_director VARCHAR(30), movie_duration TIME, move_genre VARCHAR(20), PRIMARY KEY(movieid))")
cursor.execute("CREATE TABLE Requests( userid INT, movieid INT, PRIMARY KEY(userid, movieid), FOREIGN KEY (userid) REFERENCES User, FOREIGN KEY (movierid) REFERENCES Movie_Suggestion)")
cursor.execute("CREATE TABLE Creates( userid INT NOT NULL, playlistid INT NOT NULL, PRIMARY KEY(playlistid), FOREIGN KEY (userid) REFERENCES User, FOREIGN KEY (playlistrid) REFERENCES Playlist)")
cursor.execute("CREATE TABLE Consists( songid INT NOT NULL, playlistid INT NOT NULL, PRIMARY KEY(songid), FOREIGN KEY (songid) REFERENCES Song, FOREIGN KEY (playlistrid) REFERENCES Playlist )")

#this command pulls all the tables from the current db and prints them
sql = '''show tables'''
cursor.execute(sql)
print(cursor.fetchall())
