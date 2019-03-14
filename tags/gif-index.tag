import fatch from './fatch'

<gif-index>
  <div class="flexy">
    <a href="#{gif}" each={ gif in gifs}>
      <img src="{gif}party.gif" />
      {gif}
    </a>
  </div>
  <gif-detail if={target} target={target}/>
<script>
this.gifs = []
const setGifs = (gifs) => {
  this.gifs = gifs
  this.update()
}
fatch('gifs.log').then(setGifs)
this.on("update",() => {
  this.target = window.location.hash.slice(1)
  if (!this.gifs.includes(this.target)) {
    this.target = undefined
  }
})
</script>
</gif-index>