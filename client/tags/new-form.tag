import uR from 'unrest.io'
import fatch from '../fatch'

<gtfo-new-form>
  <div class="columns">
    <div class="column col-4 {loading: loading}">
      <ur-form model={uR.db.server.PartyImage} editable_fieldnames={editable_fieldnames}
               initial={initial} submit={submit} onchange={change} />
    </div>
    <div class="column col-8">
      <gtfo-viewer source_id={image.id} sort_codes={sort_codes}/>
    </div>
  </div>
<script>
this.on('before-mount', () => {
  this.sort_codes = ['-r32-n12-d4-Rsrgba(244,171,186,1)']
  this.editable_fieldnames = [ 'resize', 'negate', 'color_method', 'replace_color' ]
  this.image = uR.db.server.SourceImage.objects.get(this.opts.matches[1])
  window.IMAGE = this.image
  if (this.image.n_frames <= 1) {
    this.editable_fieldnames.unshift("delay")
    this.editable_fieldnames.unshift("n_frames")
  }
  this.initial = { n_frames: 12, resize:32, negate:"", hue_rotate: false, }
})
this.on("update",() => {
})


change(form) {
  this.root.className = "method__"+this.root.querySelector('[name=color_method]').value
  const color = this.root.querySelector("[name=replace_color]").value.replace("srgb","rgb")
  const label = this.root.querySelector("[for=__replace_color]")
  label.style.backgroundColor=color
}

submit(form) {
  const data = {
    ...form.getData(),
    source: this.opts.matches[1],
  }
  this.loading = true
  this.update()
  return uR.ajax({
    url: "/api/party/",
    method: "POST",
    data,
  })
    .then(({code}) => {
      this.sort_codes.unshift(code)
      return fatch().then(() => {
        this.loading = false
        this.update()
      })
    })
}
</script>
</gtfo-new-form>