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
      <div each={variant in fatch_obj.variants} class="card" onclick={showDetail}>
        <div class="card-body" tile={variant.name}>
          <div class="fixed-image">
            <img src="{prefix}{variant.party_src}" />
          </div>
          <div class="ellipsis">{variant.name}</div>
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
  this.prefix = fatch.PREFIX
})
showDetail(e) {
  uR.element.alert(
    'gtfo-detail',
    {},
    { variant: e.item.variant, image: this.image }
  )
}
</script>
</gtfo-viewer>