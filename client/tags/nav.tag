<gtfo-nav>
  <header class="navbar">
    <section class="navbar-section">
      <a href="/" class="navbar-brand mr-2 text-bold">Spectre.css</a>
      <a class="btn btn-link" each={ link in links } href={link.href}>{link.text}</a>
    </section>
    <section class="navbar-section">
      <a class="btn btn-primary" href="https://github.com/chriscauley/gif-party/">github</a>
    </section>
  </header>
<script>
  this.links = [
    { text: "New Party Gif", href: "#/image/new/" }
  ]
</script>
</gtfo-nav>