import _ from 'lodash'

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
      return
    }
    tree[src][code][step] = tree[src][code][step] || []
    tree[src][code][step].push(path)
  })
  uR.storage.set("RESULTS_TREE", tree)
  fatch.cacheList()
  return tree
})

fatch.getTree = () => uR.storage.get("RESULTS_TREE")

fatch.cacheList = () => {
  const tree = fatch.getTree()
  if (!tree) {
    fatch.list = []
    return
  }
  const list = []
  _.entries(tree).forEach( ([filename,variant_map]) => {
    const variants = []
    _.entries(variant_map).forEach( ([variant_name,step_map]) => {
      const steps = []
      _.entries(step_map).forEach(([name,files]) => {
        steps.push({ name, files})
      })
      variants.push({
        name: variant_name,
        steps: _.sortBy(steps,'name'),
        party_src: `${filename}/${variant_name}/party.gif`
      })
    })
    list.push({
      filename,
      variants: _.sortBy(variants,'name'),
    })
  })
  fatch.list = _.sortBy(list,'filename')
}

fatch.cacheList()

fatch.PREFIX = "/media/.party/"

export default fatch