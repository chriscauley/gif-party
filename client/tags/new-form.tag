import uR from 'unrest.io'

<gtfo-new-form>
  <div class="columns">
    <div class="column col-4 text-center">
      <h2>{image.name}</h2>
      <img src={image.src}/>
    </div>
    <div class="column col-8">
      <ur-form model={uR.db.server.PartyImage} editable_fieldnames={editable_fieldnames}
               initial={initial} success={success} />
    </div>
  </div>
<script>
this.on('before-mount', () => {
  this.editable_fieldnames = ['resize', 'n_frames', 'negate', 'hue_rotate']
  this.image = uR.db.server.SourceImage.objects.get(this.opts.matches[1])
  this.initial = { source: this.image, n_frames: 12 }
})
success(obj) {
  //should redirect to object index
}
</script>
</gtfo-new-form>