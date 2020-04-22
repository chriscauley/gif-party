import React from 'react'
import { Link } from 'react-router-dom'
import css from '@unrest/css'

const LinkHack = (props) => {
  const Tag = props.href ? 'a' : Link
  return <Tag {...props} />
}

export default function ImageCard({ src, children, ...props }) {
  return (
    <LinkHack className={css.card.outer('m-4 w-40')} {...props}>
      <div className="list-img bg-gray-100">
        <img src={src} />
      </div>
      {children}
    </LinkHack>
  )
}
