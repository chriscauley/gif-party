import React from 'react'

import css from '@unrest/css'
import Form from '@unrest/react-jsonschema-form'

import config from './config'
import withUser from './withUser'
import post from '../post'

class BaseModal extends React.Component {
  state = {
    slug: 'login',
    error: ''
  }
  getOptions = () => {
    const { slug=this.state.slug } = this.props
    return config[slug]
  }
  onSubmit = formData => {
    return post(this.getOptions().post_url, formData)
      .catch(error => this.setState({error}))
  }
  onSuccess = () => {
    this.props.api.refetch()
    const { hash } = window.location
    if (hash === config.login.url || config.signup.url) {
      window.location.hash = ""
    }
  }

  render() {
    const { title, url, schema } = this.getOptions()
    const defaultSuccess = () => (window.location.hash = "")
    return (
      <div className={css.modal.outer()}>
        <a href="#" className={css.modal.mask()}></a>
        <div className={css.modal.content()}>
          <Form
            schema={schema}
            onSubmit={this.onSubmit}
            onSuccess={this.onSuccess}
          />
        </div>
      </div>
    )
  }
}

const Modal = withUser(BaseModal)

export default Modal


export const LoginModal = () => (
  <Modal slug="login" />
)


export const SignupModal = () => (
  <Modal slug="signup" />
)
