import React from 'react';
import '../vibecheck.css';
import { Redirect } from "react-router-dom";
import Select from 'react-select';
import makeAnimated from 'react-select/animated';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';

const genres = []
var recommended = []
const animatedComponents = makeAnimated();

const Vibes = [
{ label: "Funky", value: "Funky" },
{ label: "Happy", value: "Happy" },
{ label: "Sad", value: "Sad" },
{ label: "Chill", value: "Chill" },
{ label: "Flirty", value: "Flirty" },
{ label: "Study", value: "Study" },
{ label: "Workout", value: "Workout" },
{ label: "Nostalgic", value: "Nostalgic" }
];

class Playlist extends React.Component {
  //the states of emotion and source will be set to null initially until the user had filled out the form.
  constructor() {
    super();
    this.state = {
        data: null,
        genres: null,
        recArtists: null,
        vibe: "Funky"
      };
  }

  componentDidMount() {

    //creates a k,v pair list for genres that will be fed into react-select
    axios.get(`http://localhost:5000/allGenres`)
    .then((response) => {
      for (var i = 0; i < response.data.data.genres.length; i++) {
      genres.push({ label: response.data.data.genres[i], value: response.data.data.genres[i] })
      }
      
      this.setState({
        genres: response.data.data.genres
      });

    }).catch((error) => {
      alert("There was an error connecting to the api")
      console.error(error);
    });

  }

  handleVibe = newVibe => {
    //handles updating the state for vibe
    this.setState({vibe: newVibe['label']})
  };

  //creates a k,v pair list for artists from a certaini genre that will be fed into react-select
  handleGenres = genreChange => {
    var string = ""
    var finalGenres = []

    if (genreChange != null) {
      if (genreChange.length >= 3) {
        if(genreChange.length === 3) {
          //ensures only three genres are sent over as seeds
          for (var i = genreChange.length - 3; i < genreChange.length; i++) {
            finalGenres.push(genreChange[i]['value'])
          }
          //a custom axios post request to ensure data is sent over...
          //in this case, data is sent in params attribute
          const request = axios({
            headers: {
            'content-type': 'application/json'
            },
            method: 'post',
            url: `http://localhost:5000/recommendations`,
            params: {
            finalGenres
            }
          })
          .then((response) => {
            var length = (response.data.data.tracks.length)
            for (var i = 0; i < recommended.length; i++) {
              recommended.pop()
            }
            for (var i = 0; i < length; i++) {
              recommended.push({label: response.data.data.tracks[i].artists[0].name, value: response.data.data.tracks[i].artists[0].name})
            }
          }).catch((error) => {
            alert("There was an error connecting to the api")
            console.error(error);
          });
        }
        else {
          alert("You must ONLY have three genres.")
        }
      }
    }
  };

  submit = function (e) {
    alert('it works!');
    alert("hello")
    e.preventDefault();
  }

  render() 
    {
      return (
        <div>
          <form action='http://localhost:5000/newPlaylist' method='POST' onSubmit={this.submit}>
            <div className="container">
              <div className="row">
                <div className="col-md-6">
                  <h1>Select Vibe</h1>
                  <Select options={Vibes} onChange={this.handleVibe} components={animatedComponents}
                  />
                  <br></br>
                  <h1>Select Genres</h1>
                  <Select options={genres} onChange={this.handleGenres} components={animatedComponents} isMulti />
                  <br></br>
                  <h1>Select Artists</h1>
                  <Select options={recommended} components={animatedComponents} isMulti />
                  <br></br>
                  <input type="submit" class="button" value="Sign Up" />
                </div>
              </div>
            </div>
          </form>
        </div>
      )
    }
}
export default Playlist;