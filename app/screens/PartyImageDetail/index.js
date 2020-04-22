import React from 'react'
import css from '@unrest/css'

import PartyImageForm from './Form'
import PartyImageCard from './Card'
import withImage from './withImage'

export default withImage((props) => {
  const { variants, loading, id, src, colors, n_frames, refetch } = props.api
  if (loading && !variants) {
    return null
  }
  return (
    <div className="flex">
      <div className="w-1/3 p-4">
        <h2 className="h2">2. Select Gif Options</h2>
        <PartyImageForm
          colors={colors}
          n_frames={n_frames}
          onSuccess={() => refetch(props)}
          sourceimage_id={id}
        />
        <a href="#/help/" className={css.link()}>
          {"What's all this?"}
        </a>
      </div>
      <div className="w-2/3 p-4">
        <h2 className="h2">3. Download results</h2>
        <div className="flex flex-wrap">
          <div className={css.card.outer('m-4 w-40')}>
            <div className="list-img bg-gray-100">
              <img src={src} />
            </div>
            <div className={css.card.body()}>(no changes)</div>
          </div>
          {variants.map((variant) => (
            <PartyImageCard
              key={variant.name}
              sourceimage_id={id}
              {...variant}
            />
          ))}
        </div>
      </div>
    </div>
  )
})
