import React from 'react'
import RestHook from '@unrest/react-api'

const withImage = RestHook('/api/server/SourceImage/${match.params.object_id}/')

export default withImage(props => {
  const { variants, loading, id, src, name } = props.api
  if (loading) {
    return null
  }
  return (
    <div>
      {variants.map(({src, name}) => (
        <div key={name}>
          <img src={src} />
          {name}
        </div>
      ))}
    </div>
  )
})
