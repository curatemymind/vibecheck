import React from 'react';
import '../vibecheck.css';
import { Redirect } from "react-router-dom";
import Select from 'react-select';
import makeAnimated from 'react-select/animated';
import './loginsignup.css';
import axios from 'axios';

const genres = []
const animatedComponents = makeAnimated();
class Home extends React.Component {

  //the states of emotion and source will be set to null initially until the user had filled out the form.
  constructor() {
    super();
    this.state = {
      toggleLogin: true,
      text: "New User?"
    };
    this.toggle = this.toggle.bind(this);
  }

   
  componentDidMount() {
    
  }

    
  toggle = function(e) {
    if(this.state.toggleLogin === false)
    {
      this.setState({toggleLogin: true, text: "New User?"})
    }
    else
    {
      this.setState({toggleLogin: false, text: "Returning User?"})
    }
  }

  render() {
    

    return (
      <div>
        
        <h1>Vibecheck</h1>
        <button onClick={this.toggle}>{this.state.text}</button>
        <br></br>
        <br></br>
        {this.state.toggleLogin === false && <form action='http://localhost:5000/user' method='POST'>
          <div class="">
            <div class="">
              <div class="login-form">
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
                    <input type="submit" class="button" value="Sign Up"  />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </form>}

        {this.state.toggleLogin === true && <form action='http://localhost:5000/login' method='POST'>
          <div class="">
            <div class="">
              <div class="login-form">
                <div class="sign-up-htm">
                  
                  <div class="group">
                    <label for="pass" class="label">Email Address</label>
                    <input id="pass" name="email" placeholder="E-mail Address" type="text" class="input" />
                  </div>
                
                  <div class="group">
                    <label for="pass" class="label">Password</label>
                    <input   id="pass" placeholder="Password" name="rawPassword" type="password" class="input" data-type="password" />
                  </div>
                  
                  <div class="group">
                    <input type="submit" class="button" value="Login"  />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </form>}
      </div>
      
    )
  }
}
export default Home;
