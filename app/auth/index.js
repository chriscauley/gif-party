import RestHook from '@unrest/react-api'

import AuthModal from './Modal'
import withUser from './withUser'

export AuthModal
export withUser

export const loginRequired = withUser(
  Component => (
    props => {
      const { loading, user, refetch } = props.api
      if (loading && !user) {
        return null
      }
      if (!user) {
        return <AuthModal next={() => refetch()} />
      }
    }
  )
)