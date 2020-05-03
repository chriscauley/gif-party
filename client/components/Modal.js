import React from 'react'
import css from '@unrest/css'

export default function Modal(props) {
  return (
    <div className={css.modal.outer()}>
      <a href="#" className={css.modal.mask()}></a>
      <div className={css.modal.content()}>{props.children}</div>
    </div>
  )
}
