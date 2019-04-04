import uR from "unrest.io"

uR.router.add({
  "^#/image/new/": uR.router.routeElement("gtfo-new",() => {
  }),
})

uR.router.default_route = uR.router.routeElement("gtfo-home",()=> {})