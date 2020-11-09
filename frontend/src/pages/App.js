import React, { Component } from 'react';
import Select from 'react-select';
import makeAnimated from 'react-select/animated';
import 'bootstrap/dist/css/bootstrap.min.css';

const animatedComponents = makeAnimated();

const Countries = [
  { label: "Albania", value: 355 },
  { label: "Argentina", value: 54 },
  { label: "Austria", value: 43 },
  { label: "Cocos Islands", value: 61 },
  { label: "Kuwait", value: 965 },
  { label: "Sweden", value: 46 },
  { label: "Venezuela", value: 58 }
];



class App extends Component {

  constructor() {
    super();
    this.state = {
      countries: []
      
    }
  }
  
  handleCountry = newCountry => {
    var string = ""
    
    for(var i = 0; i < newCountry.length; i++)
    {
      string += (newCountry[i]['label'] + ", ")
    }
    alert(string)
  
  };




  render() {
    return (
      <div className="container">
        <div className="row">
          <div className="col-md-3"></div>
          <div className="col-md-6">
            <Select options={Countries} onChange={this.handleCountry} components={animatedComponents}
              isMulti />
          </div>
          <div className="col-md-4"></div>
        </div>
      </div>
    );
  }
}

export default App