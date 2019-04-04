import uR from "unrest.io"

uR.router.add({
  "^#/image/new/$": uR.router.routeElement("gtfo-new",() => {}),
  "^#/image/new/(\\d+)/$": uR.router.routeElement("gtfo-new-form",() => {}),
  "^#/image/(\\d+)/$": uR.router.routeElement("gtfo-party-image",() => {}),
})

uR.router.default_route = uR.router.routeElement("gtfo-home",()=> {})