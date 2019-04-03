import riot from 'riot'
import uR from 'unrest.io'

import './routes'
import './tags'
import './models'

uR.ready(() => {
  uR.admin.start()
})
