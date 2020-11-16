import React, { Component } from 'react';
import Select from 'react-select';
import makeAnimated from 'react-select/animated';
import 'bootstrap/dist/css/bootstrap.min.css';

const animatedComponents = makeAnimated();

const Vibes = [
  { label: "Funky", value: 355 },
  { label: "Happy", value: 54 },
  { label: "Sad", value: 43 },
  { label: "Chill", value: 61 },
  { label: "Flirty", value: 965 },
  { label: "Study", value: 46 },
  { label: "Workout", value: 58 },
  { label: "Nostalgic", value: 528 }
];

 

class App extends Component {

  constructor() {
    super();
    this.state = {
      vibes: []
      
    }
  }
  
  handleVibe= newVibe => {
    alert(newVibe['label'])
  };

  render() {
    return (
      <h1>THIS IS WHERE WE PUT ALL OF THE USERS PLAYLISTS</h1>
      // <div className="container">
      //   <div className="row">
      //     <div className="col-md-3"></div>
      //     <div className="col-md-6">
      //       <Select options={Vibes} onChange={this.handleVibe} components={animatedComponents}
      //          />
      //     </div>
      //     <div className="col-md-4"></div>
      //   </div>
      // </div>
    );
  }
}

export default App