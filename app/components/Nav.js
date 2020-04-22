import React from 'react'
import AuthNavLink from '../auth/NavLink'

export default () => {
  return (
    <header className="navbar p-4 flex justify-between items-center bg-gray-100">
      <section className="navbar-section">
        <a href="/images/" className="navbar-brand mr-2 font-bold text-blue-700 text-3xl">GTFO.party</a>
      </section>
      <section className="navbar-section">
        <AuthNavLink />
      </section>
    </header>
  )
}