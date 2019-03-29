import riot from 'riot'
import uR from 'unrest.io'

import "./tags/gif-index"
import "./tags/gif-detail"

uR.auth.enabled = false
window.riot = riot
riot.mount("gif-index")