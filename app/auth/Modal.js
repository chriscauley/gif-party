import React from 'react'
import { Link, withRouter, Redirect } from 'react-router-dom'

import css from '@unrest/css'
import Form, { post } from '@unrest/react-jsonschema-form'

import config from './config'
import withAuth from './withAuth'

class BaseModal extends React.Component {
  state = {
    error: '',
  }
  getOptions = () => {
    const { slug = this.state.slug } = this.props
    return config[slug]
  }
  onSubmit = (formData) => {
    return post(this.getOptions().post_url, formData).catch((error) =>
      this.setState({ error }),
    )
  }
  onSuccess = () => {
    this.props.auth.refetch()
    this.props.history.replace(this.getNext() || config.login_redirect)
  }

  render() {
    const { schema } = this.getOptions()
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

const Modal = withRouter(withAuth(BaseModal))

export default Modal

export const LoginModal = () => <Modal slug="login" />

export const SignupModal = () => <Modal slug="signup" />
