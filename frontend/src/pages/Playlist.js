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
        genresSelected: null,
        recArtists: null,
        vibe: "Funky",
        chosenArtists: null,
        change: false,
        arrLen: 0,
        playlistName: null,
      };
      this.handleChange = this.handleChange.bind(this);
      this.submit = this.submit.bind(this);
  }

  componentDidMount() {

    //creates a k,v pair list for genres that will be fed into react-select
    axios.get(`http://localhost:5000/allGenres`)
    .then((response) => {
      for (var i = 0; i < response.data.data.genres.length; i++) {
      genres.push({ label: response.data.data.genres[i], value: response.data.data.genres[i]})
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

  handleArtists = chosenArtists => {
    //handles updating the state for vibe
    if(chosenArtists != null)
    {
      var tempArray = []

      for(var i = 0; i < chosenArtists.length; i++)
      {
        tempArray.push([chosenArtists[i]['label'], chosenArtists[i]['parent']])
      }
      this.setState({chosenArtists: tempArray})
    }
    else{this.setState({chosenArtists: null})}
  };

  //creates a k,v pair list for artists from a certaini genre that will be fed into react-select
  handleGenres = genreChange => {
    var string = ""
    var finalGenres = []


    if (genreChange != null) {
      
      var tempArray = []

      for(var i = 0; i < genreChange.length; i++)
      {
        tempArray.push(genreChange[i]['label'])
      }
      this.setState({genresSelected: tempArray})

      if(this.state.change === true){this.setState({change: false})}
      else{this.setState({change: true})}

       
      if (genreChange.length >= 1) {
          //ensures only three genres are sent over as seeds
          if(genreChange.length <= this.state.arrLen)
          {
            var temp = this.state.arrLen - 1
            for(var b = 0; b < 10; b++)
            {
              recommended.pop()
              
            }
            //alert(recommended.length)
            this.setState({arrLen: temp})
          }
          else 
          {
            var temp = this.state.arrLen + 1
            this.setState({arrLen: temp})
          }
          
          finalGenres.push(genreChange[genreChange.length - 1]['value'])
          
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
            for (var i = 0; i < length; i++) {
              recommended.push({label: response.data.data.tracks[i].artists[0].name, value: response.data.data.tracks[i].artists[0].name, parent: finalGenres[0]})
            }
            //alert(recommended.length)
          }).catch((error) => {
            alert("There was an error connecting to the api")
            console.error(error);
          });
        
      }
    }
    else{this.setState({genresSelected: null})}
  };

  handleChange(event) {
    this.setState({playlistName: event.target.value});
  }

  submit = function (e) {
    
    var dataToSend = [this.state.vibe, this.state.genresSelected, this.state.chosenArtists, this.state.playlistName]
    const request = axios({
      headers: {
      'content-type': 'application/json'
      },
      method: 'post',
      url: `http://localhost:5000/newPlaylist`,
      params: {
        dataToSend
      }
    })
    /*alert(this.state.vibe)
    alert(this.state.genresSelected)
    alert(this.state.chosenArtists)
    alert("hey")*/
    alert("Since we did a manual post request with the data contained in the states, we need to manually redirect to the next page. The output will be in the python terminal.")
    e.preventDefault();
    window.location.replace("http://localhost:3000/test")
  }

  render() 
    {
      return (
        <div>
          {/* <h1>this is used to validate states are updating properly</h1>
          <h2>Vibe: {this.state.vibe}</h2>
          <h2>Genres Selected [{this.state.arrLen}]: {this.state.genresSelected}</h2>

          <h2>Artists: {this.state.chosenArtists}</h2>
           */}
          <form action='http://localhost:5000/newPlaylist' method='POST' onSubmit={this.submit}>
            <div className="container">
              <div className="row">
                <div className="col-md-6">
                  <h1>Playlist Name</h1>
                  <input type="text" value={this.state.playlistName} onChange={this.handleChange}/>
                  <h1>Select One Vibe</h1>
                  <Select options={Vibes} onChange={this.handleVibe} components={animatedComponents}
                  />
                  <br></br>
                  <h1>Select Three Genres</h1>
                  <Select options={genres} onChange={this.handleGenres} components={animatedComponents} isMulti />
                  <br></br>
                  <h1>Select Three Artists</h1>
                  {this.state.change === true && <Select options={recommended} onChange={this.handleArtists} components={animatedComponents} isMulti />}
                  {this.state.change === false && <Select options={recommended} onChange={this.handleArtists} components={animatedComponents} isMulti />}
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