import React from 'react'
import css from '@unrest/css'

const PARTY_FIELDS = ['n_frames', 'delay', 'fuzz', 'method', 'negate_channel', 'replace_color']
const FLAG_TO_FIELD = {
    'R': 'replace_color',
    'N': 'negate_channel',
}

const _square = "w-4 h-4"
const _rect = "w-8 h-4"

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
  return name
}

const ReplaceColor = ({color}) => (
  <div className="flex items-center mb-1" title={"replace color: "+color}>
    <span className={_square} style={{background: color}}></span>
    <i className="fa fa-arrow-right mx-1" />
    <span className={_square.replace('w-4',"w-8 bg-rainbow")}></span>
  </div>
)

const NegateChannel = ({color}) => (
  <div className="flex items-center mb-1" title={"negate channel: "+color}>
    <span className={_rect + " channel-negated-base"}></span>
    <i className="fa fa-arrow-right mx-1" style={{color}} />
    <span className={_rect + " channel-negated-"+color}></span>
  </div>
)


export default props => {
  const { name, src, delay, fuzz, replace_color, negate_channel } = props
  const speed = delay && parseInt(100/delay)
  return (
    <div className={css.card.outer('m-4 w-40')}>
      <div className="list-img bg-gray-100">
        <img src={src} />
      </div>
      <div className={css.card.body()}>
        <div>
          {negate_channel && (
            <NegateChannel color={negate_channel} />
          )}
          {replace_color ? (
            <ReplaceColor color={replace_color} />
          ) : (
            <div className="flex items-center mb-1" title="hue rotate">
              <i className="fa fa-rotate-right" />
              <div className="text-3xl rainbow-wheel" />
            </div>
          )}
          {speed && (
            <div className="mb-1" title={"Animation Speed: "+speed+'fps'}>
              <i className="fa fa-hourglass mr-2" />
              {`${speed}/s`}
            </div>
          )}
          {replace_color && fuzz && (
            <div className="mb-1" title={`fuzz ${fuzz}%`}>
              <i className="fa fa-tint mr-2" />
              {fuzz}%
            </div>
          )}
        </div>
      </div>
    </div>
  )
}