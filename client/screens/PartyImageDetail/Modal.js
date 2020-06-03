import React from 'react'
import css from '@unrest/css'
import withSourceImage from './withSourceImage'

export default withSourceImage((props) => {
  const { loading, variants = [] } = props.api
  const partyimage = variants.find(
    (pi) => pi.id === parseInt(props.match.params.partyimage_id),
  )
  if (loading || !partyimage) {
    return null
  }

  return (
    <div className={css.modal.outer()}>
      <a href="#" className={css.modal.mask()} />
      <div className={css.modal.content()}>
        {partyimage.steps.map((step) => (
          <div key={step.name}>
            <h2 className={css.h2()}>{step.name}</h2>
            <div className="flex flex-wrap">
              {step.files.map((fpath) => (
                <img
                  className="m-4"
                  src={`${partyimage.root_url}/${step.path}/${fpath}`}
                  key={fpath}
                />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
})
