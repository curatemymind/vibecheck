import React from 'react';
import '../vibecheck.css';
import { Redirect } from "react-router-dom";

class Playlist extends React.Component { 

  //the states of emotion and source will be set to null initially until the user had filled out the form.
  constructor() {
    super();
    this.state = {
      data: null,
      genres: null
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
      this.setState({
          genres: response.data.data.genres
      });
  }).catch((error) => {
      alert("There was an error connecting to the api")
      console.error(error);
  });
 }

  render()
  {  
    if(this.state.genres != null)
    {
      this.items = this.state.genres.map((item, key) =>
        <option name={item} key={key}>{item}</option>
      ); 
    }
    
    return (
      <div>
        <h1>{this.state.data}</h1>
        <form action = 'http://localhost:5000/user' method = 'POST'>
            <br></br>
            <input required type="email" name="email" placeholder="enter an email address"></input>
            <input required type="password" name="rawPassword" placeholder="enter a password"></input>
            
            <br></br>
            <label for="genres">Choose three Genres:</label>
            <br></br>
              <select name="genres" id="genres" multiple>
                {this.items}
              </select>
              <br></br>
              <label for="artists">Choose three artists:</label>
              <br></br>
              <select name="artists" id="artists" multiple>
                <option value="Artist1">Artist1</option>
                <option value="Artist2">Artist2</option>
                <option value="Artist3">Artist3</option>
                <option value="Artist4">Artist4</option>
              </select>
              <br></br>

          <button type="submit">Sign Up</button>
        </form>
      </div>
    )        
  }
}
export default Playlist;
