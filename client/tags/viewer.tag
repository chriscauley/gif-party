import uR from 'unrest.io'
import fatch from '../fatch'
import _ from 'lodash'

<gtfo-viewer>
  <div if={image}>
    <h2>
      <img src={image.src} class="inline-img" />
      {image.name}
    </h2>
    <div if={fatch_obj} class="image-list">
      <div each={variant in fatch_obj.variants} class="card">
        <div class="card-body">
          <div class="fixed-image">
            <img src="{prefix}{variant.party_src}" />
          </div>
          {variant.name}
        </div>
      </div>
    </div>
  </div>
<script>
this.on('mount',() => this.update())
this.on('update',() => {
  this.image = uR.db.server.SourceImage.objects.get(this.opts.source_id)
  const filename = this.image.src.split("/").pop()
  this.fatch_obj = fatch.list.find(f => f.filename === filename)
  console.log(this.fatch_obj)
  this.prefix = fatch.PREFIX
})
</script>
</gtfo-viewer>