import React from 'react';
import '../vibecheck.css';
import { Redirect } from "react-router-dom";
import Select from 'react-select';
import makeAnimated from 'react-select/animated';
import './loginsignup.css';
import axios from 'axios';
import Accordion from 'react-bootstrap/Accordion'
import Card from "react-bootstrap/Card";
import Button from "react-bootstrap/Button";

const genres = []
const animatedComponents = makeAnimated();
class AxiosExample extends React.Component {

  //the states of emotion and source will be set to null initially until the user had filled out the form.
  constructor() {
    super();
    this.state = {
      example: null,
      exampleArray: []
    };
  }

  componentDidMount() {

    //creates a k,v pair list for genres that will be fed into react-select
    axios.get(`http://localhost:5000/example`)
      .then((response) => {
        //alert(response.data.data)

        this.setState({
          example: response.data.data
        });

      }).catch((error) => {
        alert("There was an error connecting to the api")
        console.error(error);
      });

    //secong get request
    axios.get(`http://localhost:5000/exampleArray`)
      .then((response) => {
        //alert(response.data.data)
        //we have to set a temp array and then set that equal to that state
        //this is beacause state arrays have no simple push feature, only setState
        var mack = []

        for (var i = 0; i < response.data.data.length; i++) {
          mack.push(response.data.data[i])
        }

        this.setState({
          exampleArray: mack,

        });

      }).catch((error) => {
        //alert("There was an error connecting to the api")
        console.error(error);
      });
  }

  render() {

    return (
      <div >
        <br></br>
        <div class="btn-group">

          <a href="http://localhost:3000/playlist" class="btn btn-primary btn-lg" role="button">Create New Playlist</a>
          <a href="http://localhost:5000/logout" class="btn btn-primary btn-lg" role="button">Log Out</a>

        </div>
        <br></br>
                  <form action='http://localhost:5000/deletePlaylist' method='POST'>
                     <br></br><label class="label">Enter a Playlist ID to Delete: </label><br></br>
                      <input name="deleteId" requiredplaceholder= "Playlist ID" type="text" class="input" />
                      <br></br><br></br><button type="submit">Delete Playlist</button>
                  </form>
                  <br></br>
                  <form action='http://localhost:5000/updatePlaylist' method='POST'>
                    <label class="label">Enter a Playlist ID to Update Playlist Name:</label>
                    <br></br><input name="playlistId" requiredplaceholder= "Playlist ID" type="text" class="input" />
                    <br></br>
                    <label class="label">Enter New Playlist Name: </label>
                    <br></br><input name="newName" requiredplaceholder= "Playlist ID" type="text" class="input" />
                    <br></br><br></br> <button type="submit">Update Playlist</button>
                    <br></br>
                  </form>
        <br></br>

        {/*In React, map is the equivalent of a loop for html. it requires (key, value) assignments*/}
        <br></br>

        {this.state.exampleArray.map((item, key) =>
          <Accordion defaultActiveKey="1">
            <Card>
              <Card.Header>
                <Accordion.Toggle as={Button} variant="link" eventKey="0">
               <h1>Playlist Name: {item[1]} Playlist Duration: {item[3]}  Playlist Vibe: {item[2]} Playlist Id: {item[0]}</h1>   
                </Accordion.Toggle>
              </Card.Header>
              <Accordion.Collapse eventKey="0">
    
               
                <Card.Body>
                 
                   {(item[4]).map((song, key2) =>
                  <li>Song Name: {song[0]} Song Artist: {song[1]} Duration: {song[2]} </li>
                )}
                  {/* {(item[4]).map((movie, key3) =>
                  <li>Movie id: {movie[0]} Movie Title: {movie[1]} Movie Genre: {movie[2]} </li>
                )}  */}
                </Card.Body>
               
              {/* <Card.Body> {(item[5]).map((movie, key3) =>
                  <li>Movie id: {movie[0]} Movie Title: {movie[1]} Movie Genre: {movie[2]} </li>
                )}</Card.Body> */}
               
              </Accordion.Collapse>
               
            </Card>

          </Accordion>
        )}



      </div>

    )

  }
}
export default AxiosExample;
