import uR from 'unrest.io'

<gtfo-new>
  <h2 class="flexy">What image do you want to party?</h2>
  <div class="image-list">
    <a href="#/image/new/{image.id}/" each={image in images} class="card">
      <div class="card-body">
        <div class="fixed-image"><img src={image.src} /></div>
        <div class="text-center">{image.name}</div>
      </div>
    </a>
  </div>
<script>
  this.on("mount", () => this.update())
  this.on("update",() => {
    this.images = uR.db.server.SourceImage.objects.all()
  })
</script>
</gtfo-new>