import uR from 'unrest.io'

<gtfo-new>
  <h2 class="flexy">What image do you want to party?</h2>
  <div class="images">
    <div each={image in images} class="card">
      <div class="card-body">
        <div class="image"><img src={image.src} /></div>
        <div>{image.name}</div>
      </div>
    </div>
  </div>
<script>
  this.on("mount", () => this.update())
  this.on("update",() => {
    this.images = uR.db.server.SourceImage.objects.all()
    console.log(this.images)
  })
</script>
</gtfo-new>