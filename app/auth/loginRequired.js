import React from 'react'
import { Redirect, withRouter } from 'react-router-dom'

import config from './config'
import withAuth from './withAuth'

export default (Component) => {
  return withRouter(
    withAuth((props) => {
      if (props.auth.user) {
        return <Component {...props} />
      }
      return <Redirect to={config.makeUrl('login', props.location.pathname)} />
    }),
  )
}
