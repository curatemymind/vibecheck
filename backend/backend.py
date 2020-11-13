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

#connection string to RDS. This is preferred because it lets you pass in the
#database argument rather than having to select it first, more condensed
db = pymysql.connect(
  host="vibecheckdb.cfmab8sxzhn7.us-east-2.rds.amazonaws.com",
  user="admin",
  password="rootroot",
  database="final"
)

os.environ["SPOTIPY_CLIENT_ID"] = "63e7b7530d13411f9e292730a6ed552e"
os.environ["SPOTIPY_CLIENT_SECRET"] = "4893989706694f2489d4a44f160089c1"
#sets cursor
cursor = db.cursor()
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
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
        self.errorData = args[0] if len(args)>0 else {}

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
    errObj = {"status": "Fatal Error", "message": "The code returned does not correspond with a status! Contact an admin for help."}

    # Return the code's corresponding dict
    return possibleCodes.get(code, errObj)


@app.route('/')
def hello_world():
  return Response(200, "hello, world!").serialize()

@app.route('/data', methods=['GET', 'POST'])
@cross_origin()
def data():
  if request.method == 'GET':
    #queryResult array
    res = []
    #select all data from table test and set it equal to the cursor
    cursor.execute("SELECT * FROM test")
    queryResult = cursor.fetchall()
    for x in queryResult:
      print(x)
      res.append(x)
    #send the dictionary over to the frontend
    return Response(200, res).serialize()
  if request.method == 'POST':
    document = request.form.to_dict()
    dummyData = document['dummydata']
    #goes into the test table and inserts the form's dummy data value
    cursor.execute("INSERT INTO test (dummyData) VALUES (%s)", dummyData)
    db.commit()
    #redirects user to the frontend homepage so they can see the update immediately
    #this is a sort of unit test, it sends data through the POST and redirects you to
    #a page that pulls from the GET, In both of these, the db is being interacted with
    return redirect("http://localhost:3000/")

@app.route('/user', methods=['GET', 'POST'])
def user():
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
    
    #rawPassword.encode('utf-8')
    #correctPassword = bcrypt.checkpw(rawPassword.encode('utf-8'), user['rawPassword'])
    #hashedPassword = bcrypt.hashpw(rawPassword, bcrypt.gensalt())
    userid = random.randint(1,100)*2

    genres = request.form.getlist('genres')
    artists = request.form.getlist('artists')
     
    if(email == ""):
      #this create table command creates a table
      sql = "SELECT email,password FROM User2 WHERE email=%s AND password =%s"
      val = (siun,sipw)
      print(cursor.execute(sql, val))
      if(cursor.execute(sql, val)):
        print("login exists")
      else:
        print("Incorrect info")
    else:
      #this create table command creates a table
      sql = "SELECT email FROM User2 WHERE email=%s"
      val = (email)
      if(cursor.execute(sql, val)):
        #alert here  
        print("u already have an account")
      else:
        sql = "INSERT INTO User2 ( userid, first_name, last_name, email, password) VALUES (%s,%s,%s,%s, %s)"
        val = (userid,firstname,lastname,email,rawPassword)
        cursor.execute(sql, val)
        db.commit()

    return Response(200, [siun, sipw, userid, firstname, lastname, email, p, hashedPassword, genres, artists]).serialize()


#spotify implementation
#spotify username: 4l05jlcp1nkx9islgr7ontt7c
#client id: 63e7b7530d13411f9e292730a6ed552e
#secret: 4893989706694f2489d4a44f160089c1
@app.route('/testspotify')
def test_spotify():
  lz_uri = 'spotify:artist:3TVXtAsR1Inumwj472S9r4'

  results = spotify.artist_top_tracks(lz_uri)
  print(spotify.recommendation_genre_seeds())
  #for track in results['tracks'][:10]:
      #print('track    : ' + track['name'])
      #print('audio    : ' + track['preview_url'])
      #print('cover art: ' + track['album']['images'][0]['url'])
      #print()
  return Response(200, results, "tested spotify check terminal log!").serialize()

@app.route('/allGenres')
def all_genres():
  results = spotify.recommendation_genre_seeds()
  return Response(200, results).serialize()


@app.route('/lexie')
def lexie():
  #ALL WE NEED TO DO IS PASS THE GENRE1, GENRE2, GENRE3, ID1,ID2, ID3
  res = []
  #get ids for all three playlists (corresponding with each artist + vibe)
  response1 = spotify.playlist("0RVjFnEY7zzHWtQzOG4wKB")
  response2 = spotify.playlist("3Kmqb5j2x9qfYDXjSzlmbi")
  response3 = spotify.playlist("1etBZAb8BFmHtiCx1eFDSz")

  for i in range(5):
    innerRes1 = []
    innerRes1.append(response1['tracks']['items'][i]['track']['name'])
    innerRes1.append(response1['tracks']['items'][i]['track']['duration_ms'])
    innerRes1.append(response1['tracks']['items'][i]['track']['artists'][0]['name'])
    innerRes1.append("genre 1")
    res.append(innerRes1)

  for i in range(5):
    innerRes2 = []
    innerRes2.append(response2['tracks']['items'][i]['track']['name'])
    innerRes2.append(response2['tracks']['items'][i]['track']['duration_ms'])
    innerRes2.append(response2['tracks']['items'][i]['track']['artists'][0]['name'])
    innerRes2.append("genre 2")
    res.append(innerRes2)

  for i in range(5):
    innerRes3 = []
    innerRes3.append(response3['tracks']['items'][i]['track']['name'])
    innerRes3.append(response3['tracks']['items'][i]['track']['duration_ms'])
    innerRes3.append(response3['tracks']['items'][i]['track']['artists'][0]['name'])
    innerRes3.append("genre 3")
    res.append(innerRes3)

  count = 0
  for val in res:
    sql = "INSERT INTO Song ( songid, song_name, artist, duration, genre) VALUES (%s,%s,%s,%s, %s)"
    val[1] = int(val[1])
    seconds=(val[1]/1000)%60
    seconds = int(seconds)
    minutes=(val[1]/(1000*60))%60
    minutes = int(minutes)
    hours=(val[1]/(1000*60*60))%2
    val[1] = "%d:%d:%d" % (hours, minutes, seconds)
    val = (count,val[0], val[2],val[1],val[3])
    cursor.execute(sql, val)
    db.commit()
    count += 1

  return Response(200, res).serialize()


@app.route('/recommendations', methods=['GET', 'POST'])
def rec():
  if request.method == 'GET':
    results = spotify.recommendations(None, ['alternative'])
    return Response(200, results).serialize()
  elif request.method == 'POST':
    genreSeeds = request.args.getlist('finalGenres[]')
    results = spotify.recommendations(None, genreSeeds, seed_tracks=None, limit=100)
    return Response(200, results).serialize()

#NOTE THAT IT RETURNS MERGED RESULTS

@app.route('/newPlaylist', methods=['POST'])
def newPlaylist():
  document = request.args.getlist('dataToSend[]')
  print(document)
  return Response(200, document).serialize()

@app.route('/allArtists')
def all_artists():
  #results = spotify.current_user_top_artists()

  urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'

  artist = spotify.artist(urn)
  print(artist)

  # user = spotify.user('plamere')
  # print(user)
  return Response(200, user).serialize()

@app.route('/spotify')
def spo():
  return Response(200, "successful redirect!").serialize()

user = '4l05jlcp1nkx9islgr7ontt7c'
scope = 'user-read-private user-read-playback-state user-modify-playback-state'

if __name__ == '__main__':
  app.run(host="localhost", port=5000, debug=True)
  

  #/user user sign up + top three artists [predefined] + top three genres [predefined] + vibe +  
  #/login login 
  #