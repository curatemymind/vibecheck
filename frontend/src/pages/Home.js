import React from 'react';
import '../vibecheck.css';
import { Redirect } from "react-router-dom";
import Select from 'react-select';
import makeAnimated from 'react-select/animated';
import './loginsignup.css';

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
      <form action='http://localhost:5000/user' method='POST'>
        <div class="login-wrap">
          <div class="login-html">
            <h1>Vibecheck</h1>
            <input id="tab-1" type="radio" name="tab" class="sign-in" />
            <label for="tab-1" class="tab">Sign In</label>
            <input id="tab-2" type="radio" name="tab" class="sign-up" />
            <label for="tab-2" class="tab">Sign Up</label>
            <div class="login-form">
              <div class="sign-in-htm">
                <div class="group">
                  <label for="user" class="label">Username</label>
                  <input   placeholder="E-mail Address" name="siun" id="user" type="text" class="input" />
                </div>
                <div class="group">
                  <label for="pass" class="label">Password</label>
                  <input   placeholder="Password" name="sipw" id="user" type="password" class="input" />
                </div>
                <div class="group">
                  <input type="submit" class="button" value="Sign In" />
                </div>
              </div>
              <div class="sign-up-htm">
                <div class="group">
                  <label for="user" class="label">First Name</label>
                  <input   placeholder="First Name" name="firstname" id="user" type="text" class="input" />
                </div>
                <div class="group">
                  <label for="user" class="label">Last Name</label>
                  <input   placeholder="Last Name" name="lastname" id="user" type="text" class="input" />
                </div>
                <div class="group">
                  <label for="pass" class="label">Password</label>
                  <input   id="pass" placeholder="Password" name="rawPassword" type="password" class="input" data-type="password" />
                </div>
                <div class="group">
                </div>
                <div class="group">
                  <label for="pass" class="label">Email Address</label>
                  <input id="pass" name="email" placeholder="E-mail Address" type="text" class="input" />
                </div>
                <div class="group">
                  <input type="submit" class="button" value="Sign Up" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </form>
    )
  }
}
export default Home;
