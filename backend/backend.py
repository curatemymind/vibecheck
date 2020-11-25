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
import datetime 

# SELECT Song.song_name, Song.artist, Song.duration FROM Song INNER JOIN Consists ON Song.songid=Consists.songid WHERE Consists.playlistid = 4;
# SELECT vibe, playlist_name, Playlist_duration FROM Playlist WHERE playlistid = 4;

# SELECT playlist FROM Playlist WHERE userid=%s
# ->this could return many so we save these values in a list
# ->we can loop through the list
# for id in list_of_pid:
# select statements that you wrote
# print out all songs in playlist

global userid
userid = None

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

def convert(seconds):     
    min, sec = divmod(seconds, 60)     
    hour, min = divmod(min, 60)     
    return "%d:%02d:%02d" % (hour, min, sec)

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

@app.route('/isLoggedIn')
def isLoggedIn():
    if(userid is None):
        return Response(200, False).serialize()
    else:
        return Response(200, True).serialize()
@app.route('/logout')
def logout():
    global userid
    userid = None
    return redirect("http://localhost:3000/")

@app.route('/updatePlaylist', methods=['POST'])
def updatePlaylist():
    document = request.form.to_dict()
    playlistid = document['playlistId']
    newName = document['newName']

    sql = "UPDATE Playlist SET playlist_name = %s WHERE playlistid = %s"
    val = (newName, playlistid)
    cursor.execute(sql, val)
    db.commit()

    return redirect("http://localhost:3000/data")


@app.route('/login', methods=['POST'])
def login():
    global userid
    document = request.form.to_dict()

    email = document['email']
    password = document['rawPassword']

    sql = "SELECT userid, email, password FROM User WHERE email=%s"
    val = (email)
            #print(cursor.execute(sql, val))
    if(cursor.execute(sql, val)):
        info = cursor.fetchall()
        dbEmail = info[0][1]
        dbHashedPassword = info[0][2]
        print(dbHashedPassword)
        correctPassword = bcrypt.checkpw(password.encode('utf-8'), dbHashedPassword.encode('utf-8'))

        if correctPassword == True:
            userid = info[0][0]
            return redirect("http://localhost:3000/data")
        else:
            return redirect("http://localhost:3000/error")
    else:
        return redirect("http://localhost:3000/error")
        
@app.route('/user', methods=['GET', 'POST'])
def user():
    global userid
    if request.method == 'POST':
        document = request.form.to_dict()
        firstname = document['firstname']
        lastname = document['lastname']
        email = document['email']
        rawPassword = document['rawPassword'].encode('utf-8')

        hashedPassword = bcrypt.hashpw(rawPassword, bcrypt.gensalt())

        # this create table command creates a table
        sql = "SELECT email FROM User WHERE email=%s"
        val = (email)
        if(cursor.execute(sql, val)):
            return redirect("http://localhost:3000/error")
        else:
            sql = "SELECT MAX(userid) FROM User"
            cursor.execute(sql)
            temp_userid = [item[0] for item in cursor.fetchall()]

            if temp_userid[0] is None:
                userid = 1
            else:
                userid = temp_userid[0] + 1
            sql = "INSERT INTO User ( userid, first_name, last_name, email, password) VALUES (%s,%s,%s,%s, %s)"
            val = (userid, firstname, lastname, email, hashedPassword)
            cursor.execute(sql, val)
            db.commit()
            return redirect("http://localhost:3000/data")
        


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
            response1 = spotify.search(q=str(parsed[i]),  type='playlist')

        idsAndGenres.append(response1['playlists']['items'][0]['id'])

        #i + 1 == Genre
        idsAndGenres.append(parsed[i + 1])
        i += 2

    finalResponse = []
    i = 0

    while i < len(idsAndGenres):
        # queries playlist
        res = spotify.playlist(idsAndGenres[i])
        # ERROR CHECK TO SEE IF dele HAS FIVE SONGS
        num = 0
        if len(res['tracks']['items']) > 5:
            num = 5
        else:
            num = len(res['tracks']['items'])

        print(len(res['tracks']['items']))
        
            
        for j in range(num):
            # makes array of metadata to append into larger final response array
            innerRes = []
            innerRes.append(res['tracks']['items'][j]['track']['name'])
            innerRes.append(res['tracks']['items'][j]['track']['duration_ms'])
            innerRes.append(res['tracks']['items'][j]['track']['artists'][0]['name'])
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
        sql = "INSERT INTO Song ( songid, song_name, artist, duration, genre, playlistid, userid) VALUES (%s,%s,%s,%s, %s, %s,%s)"
        item[1] = int(item[1])
        totalms = totalms + item[1]
        seconds = (item[1]/1000) % 60
        seconds = int(seconds)
        minutes = (item[1]/(1000*60)) % 60
        minutes = int(minutes)
        hours = (item[1]/(1000*60*60)) % 2
        item[1] = "%d:%d:%d" % (hours, minutes, seconds)
        item = (songid, item[0], item[2], item[1], item[3], playlistid, userid)
        cursor.execute(sql, item)
        db.commit()
        sql = "INSERT INTO Consists (songid, playlistid, userid) VALUES (%s,%s,%s)"
        item = (songid, playlistid,userid)
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

    movidid = ""
    movies = []
    genre = ""
    url = "https://api.themoviedb.org/3/discover/movie?api_key=bfc99ccbd00163a238c5723818865149&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres="
  

    if vibe == "Funky":
        movidid = "35"
        genre = "Comedy"
    elif vibe == "Happy":
        movidid = "12"
        genre = "Adventure"
    elif vibe == "Sad":
        movidid = "18"
        genre = "Drama"
    elif vibe == "Chill":
        movidid = "14"
        genre = "Fantasy"
    elif vibe == "Flirty":
        movidid = "10749"
        genre = "Romance"
    elif vibe == "Study":
        movidid = "99"
        genre = "Documentary"
    elif vibe == "Workout":
        movidid = "28"
        genre = "Action"
    elif vibe == "Nostalgic":
        movidid = "36"
        genre = "History"

    url = url + movidid
    r = requests.get(url)

    response = r.json()
    idA = ""
    movtit = ""
    for i in range(5):
        idA = response['results'][i]['id']
        movtit = response['results'][i]['original_title']

        print("\n\n")
        print(idA)
        print(movtit)
        print(genre)
        print("\n\n")
        movies.append([idA, movtit, genre])
        idA = idA + playlistid
        sql = "INSERT INTO MovieSuggestion (movieid, movie_title, movie_genre, playlistid, userid) VALUES(%s, %s, %s, %s, %s)"
        val = (idA,movtit,genre,playlistid, userid)
        cursor.execute(sql, val)
        db.commit()
        sql = "INSERT INTO Requests (userid, movieid, playlistid) VALUES(%s, %s, %s)"
        val = (userid,idA,playlistid)
        cursor.execute(sql, val)
        db.commit()
    
    #return Response(200, res).serialize()
    #return Response(200, movies[:5]).serialize()
    return redirect("http://localhost:3000/data")

@app.route('/deleteAccount')
def deleteAccount():
    global userid

    sql = "DELETE FROM Consists WHERE userid = %s"
    val = userid
    cursor.execute(sql, val)
    db.commit()

    sql = "DELETE FROM Creates WHERE userid = %s"
    val = userid
    cursor.execute(sql, val)
    db.commit()

    sql = "DELETE FROM Requests WHERE userid = %s"
    val = userid
    cursor.execute(sql, val)
    db.commit()

    sql = "DELETE FROM MovieSuggestion WHERE userid = %s"
    val = userid
    cursor.execute(sql, val)
    db.commit()

    sql = "DELETE FROM Song WHERE userid = %s"
    val = userid
    cursor.execute(sql, val)
    db.commit()
    
    #order matters, must go last as it is a foreign key
    sql = "DELETE FROM Playlist WHERE userid = %s"
    val = userid
    cursor.execute(sql, val)
    db.commit()

    sql = "DELETE FROM User WHERE userid = %s"
    val = userid
    cursor.execute(sql, val)
    db.commit()

    userid = None
    return redirect("http://localhost:3000/")

@app.route('/deletePlaylist', methods=['POST'])
def deletePlaylist():
    document = request.form.to_dict()
    deleteId = document['deleteId']

    sql = "DELETE FROM Consists WHERE playlistid = %s"
    val = deleteId
    cursor.execute(sql, val)
    db.commit()

    sql = "DELETE FROM Creates WHERE playlistid = %s"
    val = deleteId
    cursor.execute(sql, val)
    db.commit()

    sql = "DELETE FROM Requests WHERE playlistid = %s"
    val = deleteId
    cursor.execute(sql, val)
    db.commit()

    sql = "DELETE FROM MovieSuggestion WHERE playlistid = %s"
    val = deleteId
    cursor.execute(sql, val)
    db.commit()

    sql = "DELETE FROM Song WHERE playlistid = %s"
    val = deleteId
    cursor.execute(sql, val)
    db.commit()
    
    #order matters, must go last as it is a foreign key
    sql = "DELETE FROM Playlist WHERE playlistid = %s"
    val = deleteId
    cursor.execute(sql, val)
    db.commit()

    

    return redirect("http://localhost:3000/data")

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

    returnlist = []
    mack = []
    playlistlist = []
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
        songnames = songnames + (temp) 
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
       

        songartists = songartists + (temp)

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
        songdurations = songdurations + (temp)
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
        

        songgenres = songgenres + (temp)
        

        h = []
        for i in (songdurations):
            h.append(convert(int(i)))

        
        for i in range(len(songgenres)):
            returnlist.append([songnames[i] + " ",songartists[i] + " ",h[i]+ " ",songgenres[i]])
        


        sql = "SELECT playlist_name, vibe, Playlist_duration FROM Playlist WHERE playlistid = %s"
        val = str(j)
        cursor.execute(sql,val)
        lex = cursor.fetchall()
        playlistlist.append(str(j) + " ")
        playlistlist.append(str(lex[0][0]) + " ")
        playlistlist.append(str(lex[0][1]) + " ")
        playlistlist.append(str(lex[0][2]) + " ")

        playlistlist.append(returnlist)

        sql = "SELECT movie_title FROM MovieSuggestion WHERE playlistid = %s"
        val = str(j)
        cursor.execute(sql,val)
        movieQuery = cursor.fetchall()

        #print(movieQuery)
        finalMovies = []
        for row in movieQuery:
            finalMovies.append(row[0])
        print(finalMovies)
        playlistlist.append(finalMovies)

         
        mack.append(playlistlist)
        returnlist = []
        songnames = []
        songgenres = []
        songdurations = []
        songartists = []
        playlistlist = []
        

   

    return Response(200, mack).serialize()

@app.route('/movieReccomendation', methods=['POST', 'GET'])
def movieReccomendation():
    global userid
    vibe = "Flirty"
    movidid = ""
    movies = []
    genre = ""
    url = "https://api.themoviedb.org/3/discover/movie?api_key=bfc99ccbd00163a238c5723818865149&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1&with_genres="
    if request.method == 'GET':

        if vibe == "Funky":
            movidid = "35"
            genre = "Comedy"
        elif vibe == "Happy":
            movidid = "12"
            genre = "Adventure"
        elif vibe == "Sad":
            movidid = "18"
            genre = "Drama"
        elif vibe == "Chill":
            movidid = "14"
            genre = "Fantasy"
        elif vibe == "Flirty":
            movidid = "10749"
            genre = "Romance"
        elif vibe == "Study":
            movidid = "99"
            genre = "Documentary"
        elif vibe == "Workout":
            movidid = "28"
            genre = "Action"
        elif vibe == "Nostalgic":
            movidid = "36"
            genre = "History"

        url = url + movidid
        r = requests.get(url)

        response = r.json()
        id = ""
        movtit = ""
        for i in range(len(response['results'])):
            id = response['results'][i]['id']
            movtit = response['results'][i]['original_title']

            print("\n\n")
            print(id)
            print(movtit)
            print(genre)
            print("\n\n")
            movies.append([id, movtit, genre])

            # sql = "INSERT INTO MovieSuggestion (movieid, movie_title, movie_genre) VALUES(%s, %s, %s)"
            # val = (id,movtit,genre)
            # cursor.execute(sql, val)
            # db.commit()
            # sql = "INSERT INTO Requests (userid, movieid) VALUES(%s, %s)"
            # val = (userid,movtit)
            # cursor.execute(sql, val)
            # db.commit()

        return Response(200, movies).serialize()

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)

    # /user user sign up + top three artists [predefined] + top three genres [predefined] + vibe +
    # /login login
    #
