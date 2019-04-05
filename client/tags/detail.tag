import uR from 'unrest.io'
import fatch from '../fatch'

<gtfo-detail>
  <div class={theme.outer}>
    <div class={theme.header}>
      <div class={theme.header_title}>
        {opts.image.name}
      </div>
    </div>
    <div class={theme.content}>
      <div each={ step in opts.variant.steps }>
        <h3>{step.name}</h3>
        <div>
          <span each={ file in step.files }>
            <img src={prefix+file}/>
          </span>
        </div>
      </div>
    </div>
  </div>
this.mixin(uR.css.ThemeMixin)
this.prefix = fatch.PREFIX
console.log(this.opts)
</gtfo-detail>