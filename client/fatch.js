const get = file =>
  fetch(`/media/.party/${file}.log`)
    .then(r => {
      if (r.status !== 200) {
        return []
      }
      return r.text().then(
        text => text
          .replace(/ /g, '\n')
          .split('\n')
          .filter(Boolean)
          .map(s => s.replace(/^\.\//, '')),
      )
    })

const fatch = () => Promise.all([
  get('files'),
  get('directories'),
]).then(([files,directories]) => {
  files = files.filter(f => !f.endsWith(".log"))
  const tree = {}
  files.forEach( path => {
    const [src,code, step] = path.split("/")
    tree[src] = tree[src] || {}
    tree[src][code] = tree[src][code] || {}
    if (step === 'party.gif') {
      tree[src][code]['99-party'] = [step]
      return
    }
    tree[src][code][step] = tree[src][code][step] || []
    tree[src][code][step].push(path)
  })
  uR.storage.set("RESULTS_TREE",tree)
  return tree
})

fatch.getTree = () => uR.storage.get("RESULTS_TREE")

export default fatch