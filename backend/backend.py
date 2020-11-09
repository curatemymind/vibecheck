from flask import Flask, render_template, json, request, redirect
from bson import json_util
from flask_cors import CORS, cross_origin
import pymysql
import os
import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#connection string to RDS. This is preferred because it lets you pass in the
#database argument rather than having to select it first, more condensed
db = pymysql.connect(
  host="vibecheckdb.cfmab8sxzhn7.us-east-2.rds.amazonaws.com",
  user="admin",
  password="rootroot",
  database="testing"
)

os.environ["SPOTIPY_CLIENT_ID"] = "63e7b7530d13411f9e292730a6ed552e"
os.environ["SPOTIPY_CLIENT_SECRET"] = "4893989706694f2489d4a44f160089c1"
#sets cursor
cursor = db.cursor()
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

sql = '''show tables'''
cursor.execute(sql)
print(cursor.fetchall())

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

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
    email = document['email']
    rawPassword = document['rawPassword']
    genres = request.form.getlist('genres')
    artists = request.form.getlist('artists')
  return Response(200, [email, rawPassword, genres, artists]).serialize()


#spotify implementation
#spotify username: 4l05jlcp1nkx9islgr7ontt7c
#client id: 63e7b7530d13411f9e292730a6ed552e
#secret: 4893989706694f2489d4a44f160089c1
@app.route('/testspotify')
def test_spotify():
  lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

  results = spotify.artist_top_tracks(lz_uri)
  print(spotify.recommendation_genre_seeds())
  #for track in results['tracks'][:10]:
      #print('track    : ' + track['name'])
      #print('audio    : ' + track['preview_url'])
      #print('cover art: ' + track['album']['images'][0]['url'])
      #print()
  return Response(200, "tested spotify check terminal log!").serialize()

@app.route('/allGenres')
def all_genres():
  results = spotify.recommendation_genre_seeds()
  return Response(200, results).serialize()

@app.route('/recommendations')
def rec():
  results = spotify.recommendations(None, ['alternative'])
  return Response(200, results).serialize()

@app.route('/allArtists')
def all_artists():
  #results = spotify.current_user_top_artists()

  urn = 'spotify:artist:3jOstUTkEu2JkjvRdBA5Gu'

  artist = spotify.artist(urn)
  print(artist)

  user = spotify.user('plamere')
  print(user)
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