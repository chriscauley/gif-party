import React from 'react'
import { Route } from 'react-router-dom'
import { LoginModal, SignupModal } from './Modal'
import config from './config'

export default function AuthRoutes() {
  return (
    <>
      <Route
        exact
        path={[config.login.url, config.login.next_url]}
        component={LoginModal}
      />
      <Route
        exact
        path={[config.signup.url, config.signup.next_url]}
        component={SignupModal}
      />
    </>
  )
}
