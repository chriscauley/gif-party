import uR from 'unrest.io'

<gtfo-party-image>
  <div>
    <h2 class="flexy">
      {source.name}
      <a class="fa fa-2x fa-refresh btn btn-link" onclick={refresh}></a>
    </h2>
    <img src={source.src}/>
  </div>
<script>
  this.on('before-mount', () => {
    this.party = uR.db.server.PartyImage.objects.get(this.opts.matches[1])
    this.source = this.party.source
  })
  refresh() {
    console.log(this.party.id)
  }
</gtfo-party-image>