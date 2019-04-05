import uR from 'unrest.io'
import fatch from '../fatch'

<gtfo-new-form>
  <div class="columns">
    <div class="column col-4">
      <ur-form model={uR.db.server.PartyImage} editable_fieldnames={editable_fieldnames}
               initial={initial} submit={submit} onchange={change} />
    </div>
    <div class="column col-8">
      <gtfo-viewer source_id={image.id} code={this.code} />
    </div>
  </div>
<script>
this.on('before-mount', () => {
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
}

submit(form) {
  const data = {
    ...form.getData(),
    source: this.opts.matches[1],
  }
  return uR.ajax({
    url: "/api/party/",
    method: "POST",
    data,
  })
    .then(({code}) => {
      this.code = code
      return fatch().then(() => this.update())
    })
}
</script>
</gtfo-new-form>