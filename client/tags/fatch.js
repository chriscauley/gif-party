export default url =>
  fetch(url).then(r => r.text()).then(
    text => text.replace(/ /g,'\n').split("\n").filter(Boolean).map(s => s.replace(/^\.\//,""))
  )