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
  getNext = () => decodeURIComponent(this.props.match.params.next || '')

  render() {
    if (this.props.auth.user) {
      return <Redirect to={this.getNext()} />
    }
    const { schema } = this.getOptions()
    return (
      <div className={css.modal.outer()}>
        <div
          onClick={() => this.props.history.goBack()}
          className={css.modal.mask()}
        />
        <div className={css.modal.content()}>
          <Form
            schema={schema}
            onSubmit={this.onSubmit}
            onSuccess={this.onSuccess}
          />
          {this.props.slug === 'login' ? (
            <div>
              {"Don't have an account? "}
              <Link
                replace={true}
                to={config.makeUrl('signup', this.getNext())}
              >
                Signup
              </Link>
            </div>
          ) : (
            <div>
              {'Already have an account?'}
              <Link replace={true} to={config.makeUrl('login', this.getNext())}>
                Login
              </Link>
            </div>
          )}
        </div>
      </div>
    )
  }
}

const Modal = withRouter(withAuth(BaseModal))

export default Modal

export const LoginModal = () => <Modal slug="login" />

export const SignupModal = () => <Modal slug="signup" />
