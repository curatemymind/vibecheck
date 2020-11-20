import React from 'react';
import '../vibecheck.css';
import { Redirect } from "react-router-dom";
import Select from 'react-select';
import makeAnimated from 'react-select/animated';
import './loginsignup.css';
import axios from 'axios';

const genres = []
const animatedComponents = makeAnimated();
class AxiosExample extends React.Component {

  //the states of emotion and source will be set to null initially until the user had filled out the form.
  constructor() {
    super();
    this.state = {
      example: null,
      exampleArray: [],
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
      var tempArray = []
      for (var i = 0; i < response.data.data.length; i++) {
        tempArray.push(response.data.data[i])
      }
      
      this.setState({
        exampleArray: tempArray
      });

    }).catch((error) => {
      //alert("There was an error connecting to the api")
      console.error(error);
    });

  }


  render() {

    return (
      <div >
        {/*React states can be called directly in the html*/}
        <h2>{this.state.example}</h2>
        {/*In React, map is the equivalent of a loop for html. it requires (key, value) assignments*/}
        <ul>
          {this.state.exampleArray.map((item, key) =>
            <div>
              <h1>{item}</h1>
              <p>you can add any html to this loop!</p>
            </div>
          )}
        </ul>
      </div>
    )
  }
}
export default AxiosExample;
