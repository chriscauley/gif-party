import React from 'react'
import ReactDOM from 'react-dom'
import { BrowserRouter, HashRouter, Route, Link } from 'react-router-dom'

import Home from './screens/Home'
import Nav from './components/Nav'

class App extends React.Component {
  render() {
    return (
      <div className="container mx-auto">
        <Nav />
        <BrowserRouter>
          <Route exact path="/" component={Home} />
        </BrowserRouter>
        <HashRouter>
        </HashRouter>
      </div>
    )
  }
}

const domContainer = document.querySelector('#react-app')
ReactDOM.render(<App />, domContainer)
