import React from 'react';
import ReactDOM from 'react-dom';
import './vibecheck.css';
import * as serviceWorker from './serviceWorker';
import { Switch, Route, BrowserRouter as Router } from 'react-router-dom';
import Home from './pages/Launch' //???? dont delete
import Error from './pages/Error'
import Playlist from './pages/Playlist'
import UserData from './pages/UserData';
import Launch from './pages/Launch';

/*using react router we set a constant equal to whatever component
we would like to render*/
const routing = (
  <Router>
    <Switch>
      <Route exact path="/" component={Launch}/> 
      <Route exact path="/playlist" component={Playlist}/>  
      <Route exact path="/data" component={UserData}/> 
      <Route exact path="/error" component={Error}/> 
      <Route exact path="/*" component={Launch}/>  
    </Switch>
  </Router>
)

/*the code below reads the path and renders component on a conditional basis.
i.e. /home throws two different components at different places...*/
ReactDOM.render(routing, document.getElementById("root"));
serviceWorker.unregister();