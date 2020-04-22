import React from 'react'
import { Route } from 'react-router-dom'
import { LoginModal, SignupModal } from './Modal'
import config from './config'

console.log(config)

export default function AuthRoutes() {
  return (
    <>
      <Route path={config.login.url.replace(/^#/,'')} component={LoginModal} />
      <Route path={config.signup.url.replace(/^#/,'')} component={SignupModal} />
    </>
  )
}