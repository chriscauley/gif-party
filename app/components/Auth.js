import React from 'react'
import { Route } from 'react-router-dom'

import css from '@unrest/css'
import Form from '@unrest/react-jsonschema-form'

export const config = {
  login_title: "Login To Continue",
  signup_title: "Signup To Continue",
  urls: {
    login: "#/login/",
    signup: "#/signup/",
  }
}

export const AuthNavLink = props => {
  const { user } = props
  return (
    <>
      <a href={config.urls.login} className={css.button.light()}>Login</a>
      <a href={config.urls.signup} className={css.button.light()}>Sign Up</a>
    </>
  )
}

const Modal = ({children}) => (
  <div className={css.modal.outer()}>
    <a href="#" className={css.modal.mask()}></a>
    <div className={css.modal.content()}>
      {children}
    </div>
  </div>
)


export const LoginModal = (props) => {
  const schema = {
    title: config.login_title,
    type: "object",
    properties: {
      username: { type: 'string', title: 'Email' },
      password: { type: 'string', title: 'Password' },
    }
  }
  return (
    <Modal>
      <Form schema={schema} />
    </Modal>
  )
}

export const SignupModal = (props) => {
  const schema = {
    title: config.signup_title,
    type: "object",
    properties: {
      username: { type: 'string', title: 'Email' },
      password: { type: 'string', title: 'Password' },
    }
  }
  return (
    <Modal>
      <Form schema={schema} />
    </Modal>
  )
}

export const AuthRoutes = () => (
  <>
    <Route path={config.urls.login.replace(/^#/,'')} component={LoginModal} />
    <Route path={config.urls.signup.replace(/^#/,'')} component={SignupModal} />
  </>
)