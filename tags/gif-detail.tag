import fatch from './fatch'

<gif-detail>
  <div each={directory in directories}>
    <h4>{directory.path}</h4>
    <div class="flexy">
      <img each={src in directory.srcs} src={src} />
    </div>
  </div>
<script>
this.directories=[]
this.on('mount',() => this.update())
this.on('update',() => {
  if (this.target === this.opts.target) { return }
  this.target = this.opts.target
  Promise.all([
    fatch(`${this.target}directories.log`),
    fatch(`${this.target}files.log`),
  ]).then(loadData)
})

const loadData = ([directories,files]) => {
  const dir_map = {}
  directories.forEach(d => dir_map[d] = [])
  files.forEach(f => {
    const d = f.split('/')[0] + "/"
    if (!dir_map[d]) { return }
    dir_map[d].push(this.target+f)
  })
  this.directories = directories.map( path => ({
    path,
    srcs: dir_map[path]
  }))
  this.update()
}

</script>
</gif-detail>