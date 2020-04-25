import React from 'react'
import css from '@unrest/css'

export default function Footer() {
  return (
    <div className={css.footer()}>
      <a
        className="text-blue-500"
        href="https://github.com/chriscauley/gif-party/"
      >
        View on GitHub
      </a>
    </div>
  )
}
