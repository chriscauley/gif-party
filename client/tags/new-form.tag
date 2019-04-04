import uR from 'unrest.io'

<gtfo-new-form>
  <div class="columns">
    <div class="column col-4 text-center">
      <h2>{image.name}</h2>
      <img src={image.src}/>
    </div>
    <div class="column col-8">form goes here!</div>
  </div>
<script>
this.on('before-mount', () => {
  this.image = uR.db.server.SourceImage.objects.get(this.opts.matches[1])
})
</script>
</gtfo-new-form>