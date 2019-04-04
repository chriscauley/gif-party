import riot from 'riot'
import uR from 'unrest.io'

import './routes'
import './tags'
import './models'

uR.element.create(
  "gtfo-nav",
  {parent: "#nav"},
  {}
)

uR.ready(() => {
  uR.admin.start()
})
