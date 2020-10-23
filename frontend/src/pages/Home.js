import React from 'react';
import '../vibecheck.css';
import { Redirect } from "react-router-dom";

class Home extends React.Component { 

  //the states of emotion and source will be set to null initially until the user had filled out the form.
  constructor() {
    super();
    this.state = {
      data: null,
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
 }

  render()
  {  
    
    return (
      <div>
        <h1>{this.state.data}</h1>
        <form action = 'http://localhost:5000/data' method = 'POST'>
            <br></br>
          <input required type="text" name="dummydata" placeholder="Enter your dummy data"></input>
            <br></br>
          <button type="submit">Sign Up</button>
        </form>
      </div>
    )        
  }
}
export default Home;
