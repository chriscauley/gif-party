import React from 'react'
import ReactDOM from 'react-dom'
import { BrowserRouter, HashRouter, Route, Link } from 'react-router-dom'

import ImageList from './screens/ImageList'
import PartyImageDetail from './screens/PartyImageDetail'
import Home from './screens/Home'
import Nav from './components/Nav'
import { AuthRoutes, LoginModal } from './components/Auth'

const App = () => {
  return (
    <div className="container mx-auto">
      <Nav />
      <BrowserRouter>
        <Route exact path="/" component={Home} />
        <Route path="/images/" component={ImageList} />
        <Route path="/image/:object_id/" component={PartyImageDetail} />
      </BrowserRouter>
      <HashRouter>
        <AuthRoutes />
      </HashRouter>
    </div>
  )
}

const domContainer = document.querySelector('#react-app')
ReactDOM.render(<App />, domContainer)
