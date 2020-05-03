import React from 'react'
import ReactDOM from 'react-dom'
import { BrowserRouter, HashRouter, Route } from 'react-router-dom'

import ImageList, { NewSourceImageModal } from './screens/ImageList'
import PartyImageDetail from './screens/PartyImageDetail'
import PartyImageModal from './screens/PartyImageDetail/Modal'
import Home from './screens/Home'
import Nav from './components/Nav'
import Footer from './components/Footer'
import auth from '@unrest/react-auth'

auth.config.login_redirect = '/images/'

const App = () => {
  return (
    <div className="container mx-auto">
      <BrowserRouter>
        <Nav />
        <Route exact path="/" component={Home} />
        <Route path="/images/" component={ImageList} />
        <Route path="/image/:sourceimage_id/" component={PartyImageDetail} />
        <auth.AuthRoutes />
        <Route path="/new/SourceImage/" component={NewSourceImageModal} />
      </BrowserRouter>
      <HashRouter>
        <Route
          path="/party/:sourceimage_id/:partyimage_id/"
          component={PartyImageModal}
        />
      </HashRouter>
      <Footer />
    </div>
  )
}

const domContainer = document.querySelector('#react-app')
ReactDOM.render(<App />, domContainer)
