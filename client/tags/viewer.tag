import uR from 'unrest.io'
import fatch from '../fatch'
import _ from 'lodash'

<gtfo-viewer>
  <div if={image}>
    <h2>
      <img src={image.src} class="inline-img" />
      {image.name}
    </h2>
    <div class="image-list">
      <div each={variant in variants} class="card { 'bg-secondary': variant === highlight }"
           style="order: {variant.order}" onclick={showDetail}>
        <div class="card-body" title={variant.name}>
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
  if (this.fatch_obj && this.fatch_obj.variants) {
    this.variants = _.sortBy(
      this.fatch_obj.variants,
      variant => {
        const index = this.opts.sort_codes.indexOf(variant.name)
        if (index === 0) {
          this.highlight = variant
        }
        return (index === -1)? 999:index
      })
  }
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