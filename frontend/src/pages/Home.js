import React from 'react';
import '../vibecheck.css';
import { Redirect } from "react-router-dom";
import Select from 'react-select';
import makeAnimated from 'react-select/animated';

const genres = []
const animatedComponents = makeAnimated();
class Home extends React.Component { 

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
    
      for(var i = 0; i < response.data.data.genres.length; i++)
      {
        genres.push({label: response.data.data.genres[i], value: response.data.data.genres[i]})
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
    for(var i = 0; i < length; i++)
    {
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
  
  if(genreChange != null)
  {
    if(genreChange.length >= 3)
    {
      alert(genreChange.length)
      for(var i = genreChange.length - 3; i < genreChange.length; i++)
      {
        finalGenres.push(genreChange[i]['value'])
      }
      alert(finalGenres)
    }
  }

  
  /*for(var i = 0; i < genreChange.length; i++)
  {
    string += (newCountry[i]['label'] + ", ")
  }
  alert(string)*/

};

  render()
  {  
    if(this.state.genres != null)
    {
      this.items = this.state.genres.map((item, key) =>
        <option name={item} key={key}>{item}</option>
      ); 
    }

    if(this.state.recArtists != null)
    {
      this.artists = this.state.recArtists.map((item, key) =>
        <option name={item} key={key}>{item}</option>
      ); 
    }
    
    return (
      <div>
        {/* {this.state.recArtists} 
        <h1>{this.state.data}</h1>  */}

        <form action = 'http://localhost:5000/user' method = 'POST'>
           
            {/* <div className="row"> */}
          <div className="col-md-3"></div>
          <div className="col-md-6">
          <br></br>
            <input required type="name" name="firstname" placeholder="First Name"></input>
            <br></br>
            <br></br>
            <input required type="name" name="lastname" placeholder="Last Name"></input>
            <br></br>
            <br></br>
            <input required type="email" name="email" placeholder="E-mail"></input>
            <br></br>
            <br></br>
            <input required type="password" name="rawPassword" placeholder="Password"></input>
            <br></br>
            <br></br>
            <Select options={genres} onChange={this.handleGenres} components={animatedComponents}
              isMulti />
          {/* </div> */}
          <div className="col-md-4"></div>
        </div>
            {/* <label for="genres">Choose three Genres:</label>
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

          <button type="submit">Sign Up</button> */}
        </form>
      </div>
    )        
  }
}
export default Home;
