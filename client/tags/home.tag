import uR from 'unrest.io'

import fatch from './fatch'

<gtfo-home>
  <!--<h2 class="flexy">Gif Tha Funk Out!</h2>-->
  <div class="flexy">
    <a href="#{gif}" each={ gif in gifs}>
      <img src="/media/.party/{gif}" />
      {gif}
    </a>
  </div>
  <gif-detail if={target} target={target}/>
<script>
this.gifs = []
const setGifs = (gifs) => {
  gifs = gifs.filter(g => g.endsWith("party.gif"))
  uR.storage.set("image-choices",gifs)
  this.gifs = gifs
  this.update()
}
fatch("files").then(setGifs)
fatch("files").then(l=> console.log(l))
fatch("directories").then(l=> console.log(l))
this.on("update",() => {
  this.target = window.location.hash.slice(1)
  if (!this.gifs.includes(this.target)) {
    this.target = undefined
  }
})
window.addEventListener("hashchange",e=>this.update())
</script>
</gtfo-home>