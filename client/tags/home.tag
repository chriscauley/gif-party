import uR from 'unrest.io'

import fatch from '../fatch'

<gtfo-home>
  <div class="home-hero text-center">
    <h1>
      <div class="smaller">Are you ready to</div>
      <div>Gif The</div>
      <div class="text-rainbow">
        <span each={l in "FUNK"}>{l}</span>
      </div>
      <div>Out?</div>
    </h1>
    <div each={link in links}>
      <a href="#/image/new/" class="btn btn-link">
        <img src={link.img} class="inline-img"/>
        {link.text}
        <img src={link.img} class="inline-img"/>
      </a>
    </div>
  </div>

<script>
  this.links = [
    {text: "Heck Yeah!", img: "/media/source_images/party-blob.gif"},
  ]
</gtfo-home>