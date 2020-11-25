import React, { Component } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';


class Error extends Component {

  constructor() { super();}
  
  componentDidMount()
  {
    alert("There was an error on your sign up/login. Redirecting you to the home page.")
    window.location.replace("http://localhost:3000/")
  }

  render() {return (<div></div>)}
}

export default Error