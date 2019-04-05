import riot from 'riot'
import uR from 'unrest.io'

import './routes'
import './tags'
import './models'
import fatch from './fatch'

uR.element.create(
  "gtfo-nav",
  {parent: "#nav"},
  {}
)

fatch()

uR.ready(() => {
})
