import uR from 'unrest.io'
import fatch from './fatch'

<gtfo-new-form>
  <div class="columns">
    <div class="column col-4">
      <ur-form model={uR.db.server.PartyImage} editable_fieldnames={editable_fieldnames}
               initial={initial} submit={submit} />
    </div>
    <div class="column col-8">
      <gtfo-viewer source_id={image.id} code={this.code} />
    </div>
  </div>
<script>
this.on('before-mount', () => {
  this.editable_fieldnames = ['resize', 'n_frames', 'negate', 'hue_rotate']
  this.image = uR.db.server.SourceImage.objects.get(this.opts.matches[1])
  this.initial = { n_frames: 12, resize:32, negate:"", hue_rotate: false, }
})
this.on("update",() => {
  console.log(this.code)
})

submit(form) {
  const data = {
    ...form.getData(),
    source: this.opts.matches[1],
  }
  uR.ajax({
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