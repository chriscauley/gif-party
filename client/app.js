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
auth.config.social = [
  {name: 'GitHub'},
  {name: 'Twitter'},
  {name: 'Google', slug: 'google-oauth2'},
]

const App = () => {
  return (
    <>
      <BrowserRouter>
        <Nav />
        <div className="app-content">
          <Route exact path="/" component={Home} />
          <Route path="/images/" component={ImageList} />
          <Route path="/image/:sourceimage_id/" component={PartyImageDetail} />
          <auth.Routes />
          <Route path="/new/SourceImage/" component={NewSourceImageModal} />
        </div>
      </BrowserRouter>
      <HashRouter>
        <Route
          path="/party/:sourceimage_id/:partyimage_id/"
          component={PartyImageModal}
        />
      </HashRouter>
      <Footer />
    </>
  )
}

const domContainer = document.querySelector('#react-app')
ReactDOM.render(<App />, domContainer)
