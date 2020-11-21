from flask import Flask, render_template, json, request, redirect
from bson import json_util
from flask_cors import CORS, cross_origin
import pymysql
import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import bcrypt
import random
import time
import pymysql
import json
import requests
from datetime import datetime

# SELECT Song.song_name, Song.artist, Song.duration FROM Song INNER JOIN Consists ON Song.songid=Consists.songid WHERE Consists.playlistid = 4;
# SELECT vibe, playlist_name, Playlist_duration FROM Playlist WHERE playlistid = 4;

# SELECT playlist FROM Playlist WHERE userid=%s
# ->this could return many so we save these values in a list
# ->we can loop through the list
# for id in list_of_pid:
# select statements that you wrote
# print out all songs in playlist

global userid


# connection string to RDS. This is preferred because it lets you pass in the
# database argument rather than having to select it first, more condensed
db = pymysql.connect(
    host="vibecheckdb.cfmab8sxzhn7.us-east-2.rds.amazonaws.com",
    user="admin",
    password="rootroot",
    database="final"
)

os.environ["SPOTIPY_CLIENT_ID"] = "63e7b7530d13411f9e292730a6ed552e"
os.environ["SPOTIPY_CLIENT_SECRET"] = "4893989706694f2489d4a44f160089c1"
# sets cursor
cursor = db.cursor()
spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials())
print(spotify)

# sql = '''show tables'''
# cursor.execute(sql)
# print(cursor.fetchall())

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.secret_key = 'mysecret'


class Response:
    def __init__(self, code, data, *args):
        # An HTTP Response code
        # See a list here: https://www.restapitutorial.com/httpstatuscodes.html
        self.code = code

        # Use getResponseData to get status and message params.
        self.status = getResponseData(code)['status']
        self.message = getResponseData(code)['message']

        # Pass thru data from constructor.
        #print("data = ", data)
        self.data = data

        # Pass thru optional errorData dict, to help describe an error.
        self.errorData = args[0] if len(args) > 0 else {}

    def serialize(self):
        return json_util.dumps(self.__dict__), {'Content-Type': 'application/json; charset=utf-8'}


def getResponseData(code):
    # Dict containing all possible response codes
    possibleCodes = {
        200: {"status": "Success", "message": "The request completed successfully"},
        401: {"status": "Login Error", "message": "We could not authenticate your login credentials"},
        404: {"status": "Failure", "message": "The resource requested could not be found"}
    }

    # errObj, the default response when a code is not found in the possibleCodes dict
    errObj = {"status": "Fatal Error",
              "message": "The code returned does not correspond with a status! Contact an admin for help."}

    # Return the code's corresponding dict
    return possibleCodes.get(code, errObj)


@app.route('/user', methods=['GET', 'POST'])
def user():
    global userid
    if request.method == 'POST':
        document = request.form.to_dict()
        firstname = document['firstname']
        lastname = document['lastname']
        email = document['email']

        #sign in username + password
        siun = document['siun']
        sipw = document['sipw']
        p = document['rawPassword']
        rawPassword = document['rawPassword'].encode('utf-8')

        hashedPassword = bcrypt.hashpw(rawPassword, bcrypt.gensalt())

        sql = "SELECT MAX(userid) FROM User"
        cursor.execute(sql)
        temp_userid = [item[0] for item in cursor.fetchall()]

        if temp_userid[0] is None:
            userid = 1
        else:
            userid = temp_userid[0] + 1

        genres = request.form.getlist('genres')
        artists = request.form.getlist('artists')

        if(email == ""):
            # this create table command creates a table
            sql = "SELECT email,password FROM User WHERE email=%s AND password =%s"
            val = (siun, sipw)
            print(cursor.execute(sql, val))
            if(cursor.execute(sql, val)):
                print("login exists")
            else:
                print("Incorrect info")
        else:
            # this create table command creates a table
            sql = "SELECT email FROM User WHERE email=%s"
            val = (email)
            if(cursor.execute(sql, val)):
                # alert here
                print("u already have an account")
            else:
                sql = "INSERT INTO User ( userid, first_name, last_name, email, password) VALUES (%s,%s,%s,%s, %s)"
                val = (userid, firstname, lastname, email, rawPassword)
                cursor.execute(sql, val)
                db.commit()
        return redirect("http://localhost:3000/playlist")
        # return Response(200, [siun, sipw, userid, firstname, lastname, email, p, hashedPassword, genres, artists]).serialize()


# spotify implementation
# spotify username: 4l05jlcp1nkx9islgr7ontt7c
# client id: 63e7b7530d13411f9e292730a6ed552e
# secret: 4893989706694f2489d4a44f160089c1
@app.route('/testspotify')
def test_spotify():
    lz_uri = 'spotify:artist:3TVXtAsR1Inumwj472S9r4'

    results = spotify.artist_top_tracks(lz_uri)
    print(spotify.recommendation_genre_seeds())
    # for track in results['tracks'][:10]:
    #print('track    : ' + track['name'])
    #print('audio    : ' + track['preview_url'])
    #print('cover art: ' + track['album']['images'][0]['url'])
    # print()
    return Response(200, results, "tested spotify check terminal log!").serialize()


@app.route('/allGenres')
def all_genres():
    results = spotify.recommendation_genre_seeds()

    return Response(200, results).serialize()


@app.route('/recommendations', methods=['GET', 'POST'])
def rec():
    if request.method == 'GET':
        results = spotify.recommendations(None, ['hip-hop'])

        test = results['tracks'][1]['artists'][0]['name']
        length = len(results['tracks'])

        res = []
        for i in range(len(results['tracks'])):
            res.append(results['tracks'][i]['artists'][0]['name'])

        return Response(200, res).serialize()
    elif request.method == 'POST':
        genreSeeds = request.args.getlist('finalGenres[]')
        results = spotify.recommendations(
            None, genreSeeds, seed_tracks=None, limit=100)

        # print(results)
        #results = dict.fromkeys(results)
        test = results['tracks'][1]['artists'][0]['name']
        length = len(results['tracks'])

        res = []
        for i in range(len(results['tracks'])):
            res.append(results['tracks'][i]['artists'][0]['name'])

        res = list(dict.fromkeys(res))
        return Response(200, res).serialize()
        # return Response(200, results).serialize()

# NOTE THAT IT RETURNS MERGED RESULTS


@app.route('/newPlaylist', methods=['POST'])
def newPlaylist():
    # In the arrays used in this example, even indices hold song/artist names
    # And odd indices hold the genre
    # I believe this was the most efficient way to transfer the data over from array to array without losing
    # anything/getting mixed up in semantics of dicts and such
    global userid
    # gets list from "arguments" passed over by our manual react submit function
    #document = request.args.getlist('dataToSend[]')
    document = request.form.to_dict()

    #document['vibe'], document['genresSelected'], document['chosenArtists'], document['playlistName']

    # ) [0] = Vibe of playlist
    # ) [1] = All Genres selected
    # ) [2] = Artists selected and the genre they belong to i.e. ['Drake', 'Hip-Hop']

  # VIBE OF PLAYLIST TO PUSH TO PLAYLIST TABLE
    vibe = document['vibe']
    playlistName = document['playlistName']
    artistsAndGenres = document['chosenArtists']
    genresSelected = document['genresSelected']

    print('Playlist Name: ' + playlistName)
    print('Vibe of Playlist: ' + vibe)

    parsed = artistsAndGenres.split(',')

    # i.e. ['ID0', 'GENRE0', 'ID1', 'GENRE1']
    idsAndGenres = []
    # ADD ERROR CHECKING! SOME ARTISTS RETURN ONLY ONE RELEVANT PLAYLIST SO USING [0]['ID']
    # WILL RETURN OUT OF RANGE
    i = 0
    while i < len(parsed):
        #print(parsed[i] + ": " + parsed[i+1])
        # parsed[i+1] accesses the artiist's genre in our data structure
        # performs search and appends ID of playlist and then the genre it belongs to
        response1 = spotify.search(
            q=str(vibe + " " + parsed[i]),  type='playlist')

        if(response1['playlists']['total'] == 0):
            response1 = spotify.search(
                q=str(parsed[i]),  type='playlist')

        idsAndGenres.append(response1['playlists']['items'][0]['id'])

        #i + 1 == Genre
        idsAndGenres.append(parsed[i + 1])
        i += 2

    finalResponse = []
    i = 0

    while i < len(idsAndGenres):
        # queries playlist
        res = spotify.playlist(idsAndGenres[i])
        # ERROR CHECK TO SEE IF PLAYLIST HAS FIVE SONGS
        for j in range(5):
            # makes array of metadata to append into larger final response array
            innerRes = []
            innerRes.append(res['tracks']['items'][j]['track']['name'])
            innerRes.append(res['tracks']['items'][j]['track']['duration_ms'])
            innerRes.append(res['tracks']['items'][j]
                            ['track']['artists'][0]['name'])
            innerRes.append(idsAndGenres[i + 1])
            finalResponse.append(innerRes)
        i += 2

    sql = "SELECT MAX(playlistid) FROM Playlist"
    cursor.execute(sql)
    temp_playlistid = [item[0] for item in cursor.fetchall()]

    if temp_playlistid[0] is None:
        playlistid = 1
    else:
        playlistid = temp_playlistid[0] + 1

    totalms = 0
    sql = "SELECT MAX(songid) FROM Song"
    cursor.execute(sql)
    temp_songid = [item[0] for item in cursor.fetchall()]

    if temp_songid[0] is None:
        songid = 1
    else:
        songid = temp_songid[0] + 1

    sql = "INSERT INTO Playlist ( playlistid, playlist_name, vibe, userid) VALUES (%s,%s,%s,%s)"
    val = (playlistid, playlistName, vibe, userid)
    cursor.execute(sql, val)
    db.commit()

    for item in finalResponse:
        sql = "INSERT INTO Song ( songid, song_name, artist, duration, genre) VALUES (%s,%s,%s,%s, %s)"
        item[1] = int(item[1])
        totalms = totalms + item[1]
        seconds = (item[1]/1000) % 60
        seconds = int(seconds)
        minutes = (item[1]/(1000*60)) % 60
        minutes = int(minutes)
        hours = (item[1]/(1000*60*60)) % 2
        item[1] = "%d:%d:%d" % (hours, minutes, seconds)
        item = (songid, item[0], item[2], item[1], item[3])
        cursor.execute(sql, item)
        db.commit()
        sql = "INSERT INTO Consists (songid, playlistid) VALUES (%s,%s)"
        item = (songid, playlistid)
        cursor.execute(sql, item)
        db.commit()

        songid = songid + 1

    seconds2 = (totalms/1000) % 60
    seconds2 = int(seconds2)
    minutes2 = (totalms/(1000*60)) % 60
    minutes2 = int(minutes2)
    hours2 = (totalms/(1000*60*60)) % 2
    playlistDuration = "%d:%d:%d" % (hours2, minutes2, seconds2)

    sql = "UPDATE Playlist SET Playlist_duration = %s WHERE playlistid = %s"
    val = (playlistDuration, playlistid)
    cursor.execute(sql, val)
    db.commit()

    sql = "INSERT INTO Creates (userid, playlistid) VALUES (%s,%s)"
    item = (userid, playlistid)
    cursor.execute(sql, item)
    db.commit()

    return redirect("http://localhost:3000/axios")


    # return Response(200, finalResponse).serialize()
"""
    # NAME OF PLAYLIST TO PUSH TO PLAYLIST TABLE

    # this series of string formatting takes the string "array" that was passed from frontend
    # and converts iit into a list
    parsed = str(document[2]).replace('[', '')
    parsed = parsed.replace(']', '')
    parsed = parsed.split(',')

    for i in range(len(parsed)):
        parsed[i] = parsed[i].replace('"', '')

    # prints data passed from frontend as string
    # print(parsed)
    i = 0
    # array to keep track of playlist id and genre
    # i.e. ['ID0', 'GENRE0', 'ID1', 'GENRE1']
    idsAndGenres = []
    # ADD ERROR CHECKING! SOME ARTISTS RETURN ONLY ONE RELEVANT PLAYLIST SO USING [0]['ID']
    # WILL RETURN OUT OF RANGE
    while i < len(parsed):
        #print(parsed[i] + ": " + parsed[i+1])
        # parsed[i+1] accesses the artiist's genre in our data structure
        # performs search and appends ID of playlist and then the genre it belongs to

        response1 = spotify.search(
            q=str(vibe + " " + parsed[i]),  type='playlist')

        if(response1['playlists']['total'] == 0):
            response1 = spotify.search(
            q=str(parsed[i]),  type='playlist')

    
        idsAndGenres.append(response1['playlists']['items'][0]['id'])

        #i + 1 == Genre
        idsAndGenres.append(parsed[i + 1])
        i += 2 
     
    # prints playlist ID and Genres
    
    finalResponse = []
    i = 0

    while i < len(idsAndGenres):
        # queries playlist
        res = spotify.playlist(idsAndGenres[i])
        # ERROR CHECK TO SEE IF PLAYLIST HAS FIVE SONGS
        for j in range(5):
            # makes array of metadata to append into larger final response array
            innerRes = []
            innerRes.append(res['tracks']['items'][j]['track']['name'])
            innerRes.append(res['tracks']['items'][j]['track']['duration_ms'])
            innerRes.append(res['tracks']['items'][j]
                            ['track']['artists'][0]['name'])
            innerRes.append(idsAndGenres[i + 1])
            finalResponse.append(innerRes)
        i += 2

    # prints entire playlist with metadata and genre for each song :)
    print(finalResponse)

    sql = "SELECT MAX(playlistid) FROM Playlist"
    cursor.execute(sql)
    temp_playlistid = [item[0] for item in cursor.fetchall()]

    if temp_playlistid[0] is None:
        playlistid = 1
    else:
        playlistid = temp_playlistid[0] + 1

    totalms = 0
    sql = "SELECT MAX(songid) FROM Song"
    cursor.execute(sql)
    temp_songid = [item[0] for item in cursor.fetchall()]

    if temp_songid[0] is None:
        songid = 1
    else:
        songid = temp_songid[0] + 1

    sql = "INSERT INTO Playlist ( playlistid, playlist_name, vibe, userid) VALUES (%s,%s,%s,%s)"
    val = (playlistid, playlistName, vibe, userid)
    cursor.execute(sql, val)
    db.commit()

    for item in finalResponse:
        sql = "INSERT INTO Song ( songid, song_name, artist, duration, genre) VALUES (%s,%s,%s,%s, %s)"
        item[1] = int(item[1])
        totalms = totalms + item[1]
        seconds = (item[1]/1000) % 60
        seconds = int(seconds)
        minutes = (item[1]/(1000*60)) % 60
        minutes = int(minutes)
        hours = (item[1]/(1000*60*60)) % 2
        item[1] = "%d:%d:%d" % (hours, minutes, seconds)
        item = (songid, item[0], item[2], item[1], item[3])
        cursor.execute(sql, item)
        db.commit()
        sql = "INSERT INTO Consists (songid, playlistid) VALUES (%s,%s)"
        item = (songid, playlistid)
        cursor.execute(sql, item)
        db.commit()

        songid = songid + 1

    seconds2 = (totalms/1000) % 60
    seconds2 = int(seconds2)
    minutes2 = (totalms/(1000*60)) % 60
    minutes2 = int(minutes2)
    hours2 = (totalms/(1000*60*60)) % 2
    playlistDuration = "%d:%d:%d" % (hours2, minutes2, seconds2)

    sql = "UPDATE Playlist SET Playlist_duration = %s WHERE playlistid = %s"
    val = (playlistDuration, playlistid)
    cursor.execute(sql, val)
    db.commit()

    sql = "INSERT INTO Creates (userid, playlistid) VALUES (%s,%s)"
    item = (userid, playlistid)
    cursor.execute(sql, item)
    db.commit()

    return redirect("http://localhost:3000/axios")
    #return Response(200, finalResponse).serialize() """


@app.route('/allArtists')
def all_artists():
    #results = spotify.current_user_top_artists()

    urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'

    artist = spotify.artist(urn)
    print(artist)

    # user = spotify.user('plamere')
    # print(user)
    return Response(200, user).serialize()


@app.route('/example')
def example():
    return Response(200, "this is dynamically loaded data that is set into a state using axios!").serialize()


@app.route('/exampleArray')
def exampleArray():
    global userid
    # #for testing set userid = 1 to isolate endpoint
    userid = 1
    sql = "SELECT playlistid FROM Creates WHERE userid = %s"
    val = userid
    cursor.execute(sql, val)
    playlistCursor = cursor.fetchall()
    hi = []
    for row in playlistCursor:
        hi.append(row[0])

    songnames = []
    songdurations = []
    songartists = []
    songgenres = []
    total = 0
    for j in hi:
        sql = "SELECT COUNT(*) FROM Consists WHERE playlistid = %s"
        val = j
        cursor.execute(sql, val)
        songcount = cursor.fetchall()
        numofsongs = int((songcount[0][0]))
        total = total + numofsongs
        sql = "SELECT Song.song_name FROM Song INNER JOIN Consists ON Song.songid=Consists.songid WHERE Consists.playlistid = %s "
        val = str(j)
        cursor.execute(sql, val)
        res = cursor.fetchall()

        yo = str(res)
      
        newstr = yo.replace("(('", "")
        newstr = newstr.replace("',)", "")
        newstr = newstr.replace("('", "")
        newstr = newstr.replace("(\"", "")
        newstr = newstr.replace("\"', '", "")
        newstr = newstr.replace("\"', '", "")
        newstr = newstr.replace("')'","")
        newstr = newstr.replace(")", "")
        temp = newstr.split(",")
        songnames = songnames + temp
        while("" in songnames) : 
            songnames.remove("") 

        sql = "SELECT Song.artist FROM Song INNER JOIN Consists ON Song.songid=Consists.songid WHERE Consists.playlistid = %s "
        val = str(j)
        cursor.execute(sql, val)
        res = cursor.fetchall()
        
        artist = str(res)
        artist = artist.replace("(('", "")
        artist = artist.replace("',)", "")
        artist = artist.replace("('", "")
        artist = artist.replace("(\"", "")
        artist = artist.replace("\"', '", "")
        artist = artist.replace("\"', '", "")
        artist = artist.replace("')'","")
        artist = artist.replace(")", "")
        temp = artist.split(",")

        songartists = songartists + temp

        sql = "SELECT Song.duration FROM Song INNER JOIN Consists ON Song.songid=Consists.songid WHERE Consists.playlistid = %s "
        val = str(j)
        cursor.execute(sql, val)
        res = cursor.fetchall()


        duration = str(res)
        duration = duration.replace("(datetime.timedelta(seconds=","")
        duration = duration.replace("),)", "")
        duration = duration.replace("(", "")
        duration = duration.replace(")", "")
        temp = duration.split(",")
        songdurations = songdurations + temp
        #songdurations.append(str(res))

        sql = "SELECT Song.genre FROM Song INNER JOIN Consists ON Song.songid=Consists.songid WHERE Consists.playlistid = %s "
        val = str(j)
        cursor.execute(sql, val)
        res = cursor.fetchall()

        genre = str(res)
        genre = genre.replace("(('", "")
        genre = genre.replace("',)", "")
        genre = genre.replace("('", "")
        genre = genre.replace("(\"", "")
        genre = genre.replace("\"', '", "")
        genre = genre.replace("\"', '", "")
        genre = genre.replace("')'","")
        genre = genre.replace(")", "")
        temp = genre.split(",")

        songgenres = songgenres + temp
        
        total = 0

    print("\n\n\n\n")
    print("SONGNAMES LIST : ")
    print(songnames)
    print("NUM OF SONGS:" + str(len(songnames)))
    print("\n\n\n\n")
    print("SONGARTISTS LIST : ")
    print(songartists)
    print("NUM OF ARTISTS:" + str(len(songartists)))
    print("\n\n\n\n")
    print("SONGDURATION LIST : ")
    print(songdurations)
    print("NUM OF DURATIONS:" + str(len(songartists)))
    print("\n\n\n\n")
    print("SONGGENRES LIST : ")
    print(songgenres)
    print("NUM OF GENRES:" + str(len(songgenres)))
    print("\n\n\n\n")

    return Response(200, songnames, songartists, songdurations, songgenres).serialize()


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)

    # /user user sign up + top three artists [predefined] + top three genres [predefined] + vibe +
    # /login login
    #
