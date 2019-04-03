import uR from 'unrest.io'

<gtfo-new>
  <div each={image in images}>
    <img src={image.src} />
    <div>{image.name}</div>
  </div>
<script>
  this.on("mount", () => this.update())
  this.on("update",() => {
    this.images = uR.db.server.SourceImage.objects.all()
    console.log(this.images)
  })
</script>
</gtfo-new>