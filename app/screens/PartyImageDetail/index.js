import React from 'react'
import css from '@unrest/css'
import RestHook from '@unrest/react-api'
import PartyImageForm from './Form'
import PartyImageCard from './Card'

const withImage = RestHook('/api/server/SourceImage/${match.params.object_id}/')

export default withImage(props => {
  const { variants, loading, id, src, name, colors, n_frames, refetch } = props.api
  if (loading && !variants) {
    return null
  }
  return (
    <div className="flex">
      <div className="w-1/3 p-4">
        <PartyImageForm
          colors={colors}
          n_frames={n_frames}
          onSuccess={() => refetch(props)}
          sourceimage_id={id}
        />
      </div>
      <div className="w-2/3 p-4 flex flex-wrap">
        {variants.map(({src, name}) => (
          <PartyImageCard key={name} name={name} src={src} />
        ))}
      </div>
    </div>
  )
})
