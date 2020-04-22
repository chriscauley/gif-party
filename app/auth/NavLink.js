import React from 'react'

import css from '@unrest/css'

import config from './config'
import withUser from './withUser'

const dropdown = css.CSS({
  shelf: 'border p-4 absolute right-0 top-100 bg-white min-w-full z-10',
  toggle: css.button('cursor-pointer'),
  outer: 'relative',
  item: 'cursor-pointer',
})

class UserDropdown extends React.Component {
  state = {}
  toggle = () => this.setState({ open: !this.state.open })
  logout = () => fetch(config.logout.post_url).then(() => this.props.refetch())

  render() {
    const { user } = this.props
    return (
      <div className={dropdown.outer()}>
        <div className={dropdown.toggle()} onClick={this.toggle}>
          {user.username}
        </div>
        <div className={dropdown.shelf(this.state.open ? 'block' : 'hidden')}>
          <div className={dropdown.item()} onClick={this.logout}>
            Logout
          </div>
        </div>
      </div>
    )
  }
}

export default withUser((props) => {
  const { user, refetch } = props.api
  return user ? (
    <UserDropdown user={user} refetch={refetch} />
  ) : (
    <>
      <a href={config.login.url} className={css.button.light()}>
        Login
      </a>
      <a href={config.signup.url} className={css.button.light()}>
        Sign Up
      </a>
    </>
  )
})
