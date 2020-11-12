import React from 'react';
import '../../vibecheck.css';
import { Redirect } from "react-router-dom";
import Select from 'react-select';
import makeAnimated from 'react-select/animated';
import '../loginsignup.css';

const genres = []
const animatedComponents = makeAnimated();
class NewPlay extends React.Component {


//   <Select options={genres} onChange={this.handleGenres} components={animatedComponents} isMulti />

//   <div className="col-md-4"></div>
// </div>
//   <label for="genres">Choose three Genres:</label>
//    <br></br>
//      <select name="genres" id="genres" multiple>
//        {this.items}
//      </select>
//      <br></br>
//      <label for="artists">Choose three artists:</label>
//      <br></br>
//      <select name="artists" id="artists" multiple>
//        {this.artists}
//      </select>
//      <br></br>
// </div>

  //the states of emotion and source will be set to null initially until the user had filled out the form.
  constructor() {
    super();
    this.state = {
      data: null,
      genres: null,
      recArtists: null,
    };
  } 

  componentDidMount() {
    const axios = require('axios');
    axios.get(`http://localhost:5000/data`)
      .then((response) => {
        this.setState({
          data: (JSON.stringify(response.data.data))
        });
      }).catch((error) => {
        alert("There was an error connecting to the api")
        console.error(error);
      });

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

    axios.get(`http://localhost:5000/recommendations`)
      .then((response) => {
        var length = (response.data.data.tracks.length)

        var tempArr = []
        for (var i = 0; i < length; i++) {
          tempArr.push(response.data.data.tracks[i].artists[0].name)
        }
        this.setState({
          recArtists: tempArr
        });
      }).catch((error) => {
        alert("There was an error connecting to the api")
        console.error(error);
      });
  }

  handleGenres = genreChange => {
    var string = ""
    var finalGenres = []

    if (genreChange != null) {
      if (genreChange.length >= 3) {
        alert(genreChange.length)
        for (var i = genreChange.length - 3; i < genreChange.length; i++) {
          finalGenres.push(genreChange[i]['value'])
        }
        alert(finalGenres)
      }
    }
  };

  render() {
    if (this.state.genres != null) {
      this.items = this.state.genres.map((item, key) =>
        <option name={item} key={key}>{item}</option>
      );
    }

    if (this.state.recArtists != null) {
      this.artists = this.state.recArtists.map((item, key) =>
        <option name={item} key={key}>{item}</option>
      );
    }

    return (
      <div>
      <h1>hello</h1>
      <form action='http://localhost:5000/user' method='POST'>
         <div className="col-md-4"></div>
        
          <label for="genres">Choose three Genres:</label>
          <br></br>
          <select name="genres" id="genres" multiple>
            {this.items}
          </select>
          <br></br>
          <label for="artists">Choose three artists:</label>
          <br></br>
          <select name="artists" id="artists" multiple>
            {this.artists}
          </select>
          <br></br>
       
      </form>
      </div>
    )
  }
}
export default NewPlay;
