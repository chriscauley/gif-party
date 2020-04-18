import React from 'react'
import ReactDOM from 'react-dom'
import { BrowserRouter, HashRouter, Route, Link } from 'react-router-dom'

import ImageList from './screens/ImageList'
import ImageDetail from './screens/ImageDetail'
import Home from './screens/Home'
import Nav from './components/Nav'

const App = () => {
  return (
    <div className="container mx-auto">
      <Nav />
      <BrowserRouter>
        <Route exact path="/" component={Home} />
        <Route path="/images/" component={ImageList} />
        <Route path="/image/:object_id/" component={ImageDetail} />
      </BrowserRouter>
      <HashRouter>
      </HashRouter>
    </div>
  )
}

const domContainer = document.querySelector('#react-app')
ReactDOM.render(<App />, domContainer)
