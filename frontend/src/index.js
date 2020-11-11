import React from 'react';
import ReactDOM from 'react-dom';
import './vibecheck.css';
import * as serviceWorker from './serviceWorker';
import { Switch, Route, BrowserRouter as Router } from 'react-router-dom';
import Home from './pages/Home'
import App from './pages/App'

import Playlist from './pages/Playlist'

/*using react router we set a constant equal to whatever component
we would like to render*/
const routing = (
  <Router>
    <Switch>
      <Route exact path="/" component={Home}/> 
      <Route exact path="/test" component={App}/>  
      <Route exact path="/playlist" component={Playlist}/>  

    </Switch>
  </Router>
)

/*the code below reads the path and renders component on a conditional basis.
i.e. /home throws two different components at different places...*/
ReactDOM.render(routing, document.getElementById("root"));
serviceWorker.unregister();