import React from 'react'
import { Link } from 'react-router-dom'
import AuthNavLink from '../auth/NavLink'
import css from '@unrest/css'

export default function Nav() {
  return (
    <header className={css.nav.outer()}>
      <section className={css.nav.section()}>
        <Link
          to="/images/"
          className={css.nav.brand()}
        >
          GTFO.party
        </Link>
      </section>
      <section className={css.nav.section()}>
        <AuthNavLink />
      </section>
    </header>
  )
}
