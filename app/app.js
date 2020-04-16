import React from 'react'
import ReactDOM from 'react-dom'
import { BrowserRouter, HashRouter, Route, Link } from 'react-router-dom'

import Home from './screens/Home'

class App extends React.Component {
  render() {
    return (
      <div className="App">
        <div className="container mx-auto">
          <BrowserRouter>
            <Route exact path="/" component={Home} />
          </BrowserRouter>
          <HashRouter>
          </HashRouter>
        </div>
      </div>
    )
  }
}

const domContainer = document.querySelector('#react-app')
ReactDOM.render(<App />, domContainer)
