import riot from 'riot'
import uR from 'unrest.io'

import "./tags/gif-index"
import "./tags/gif-detail"
import "./models"

uR.ready(() => {
  uR.admin.start()
})