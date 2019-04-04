import uR from 'unrest.io'

<gtfo-viewer>
  <div if={image}>
    <h2>
      <img src={image.src} class="inline-img" />
      {image.name}
    </h2>
    <div if={!opts.code}>

    </div>
  </div>
<script>
this.on('mount',() => this.update())
this.on('update',() => {
  this.image = uR.db.server.SourceImage.objects.get(this.opts.source_id)
})
</script>
</gtfo-viewer>