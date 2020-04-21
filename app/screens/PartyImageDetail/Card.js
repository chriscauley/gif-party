import React from 'react'
import css from '@unrest/css'

const PARTY_FIELDS = ['n_frames', 'delay', 'fuzz', 'method', 'negate_channel', 'replace_color']
const FLAG_TO_FIELD = {
    'R': 'replace_color',
    'N': 'negate_channel',
}

PARTY_FIELDS.forEach(field => {
  if (!Object.values(FLAG_TO_FIELD).includes(field)) {
    FLAG_TO_FIELD[field[0]] = field
  }
})

// name has a lot of unecessary variables
const fudgeName = name => {
  name = name.replace(/-n\d+/, '')
  const out = {}
  name.split('-').filter(Boolean).forEach( flag_part => {
    const flag_name = FLAG_TO_FIELD[flag_part[0]]
    const value = flag_part.slice(1)
    out[flag_name] = value
  })
  console.log(out)
  return name
}

export default ({ name, src }) => {
  return (
    <div className={css.card.outer('m-4 w-40')}>
      <div className="list-img bg-gray-100">
        <img src={src} width="96" />
      </div>
      <div className={css.card.body()}>
        <div className="truncate">
          {fudgeName(name)}
        </div>
      </div>
    </div>
  )
}