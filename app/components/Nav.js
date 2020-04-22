import React from 'react'
import { Link } from 'react-router-dom'
import AuthNavLink from '../auth/NavLink'

export default function Nav() {
  return (
    <header className="navbar p-4 flex justify-between items-center bg-gray-100">
      <section className="navbar-section">
        <Link
          to="/images/"
          className="navbar-brand mr-2 font-bold text-blue-700 text-3xl"
        >
          GTFO.party
        </Link>
      </section>
      <section className="navbar-section">
        <AuthNavLink />
      </section>
    </header>
  )
}
