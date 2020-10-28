from flask import Flask, render_template, json, request, redirect
from bson import json_util
from flask_cors import CORS, cross_origin
import pymysql

#connection string to RDS. This is preferred because it lets you pass in the
#database argument rather than having to select it first, more condensed
db = pymysql.connect(
  host="vibecheckdb.cfmab8sxzhn7.us-east-2.rds.amazonaws.com",
  user="admin",
  password="rootroot",
  database="testing"
)

#sets cursor
cursor = db.cursor()


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

if __name__ == '__main__':
  app.run(host="localhost", port=5000, debug=True)
  