// Рендер платформ, контактів та епізодів із episodes/episodes.json
(function () {
  document.getElementById("year").textContent = new Date().getFullYear();

  function el(tag, attrs, text) {
    var node = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) { node.setAttribute(k, attrs[k]); });
    if (text) node.textContent = text;
    return node;
  }

  function formatDate(iso) {
    var d = new Date(iso + "T00:00:00");
    if (isNaN(d)) return iso;
    return d.toLocaleDateString("uk-UA", { day: "numeric", month: "long", year: "numeric" });
  }

  fetch("episodes/episodes.json", { cache: "no-cache" })
    .then(function (r) { return r.json(); })
    .then(function (data) {
      var platforms = document.getElementById("platforms");
      (data.platforms || []).filter(function (p) { return p.url; }).forEach(function (p) {
        platforms.appendChild(el("a", { href: p.url, target: "_blank", rel: "noopener" }, p.name));
      });

      var contact = document.getElementById("contact-links");
      (data.contacts || []).filter(function (c) { return c.url; }).forEach(function (c, i) {
        if (i) contact.appendChild(document.createTextNode(" · "));
        contact.appendChild(el("a", { href: c.url, target: "_blank", rel: "noopener" }, c.name));
      });

      var list = document.getElementById("episode-list");
      list.innerHTML = "";
      var episodes = (data.episodes || []).slice().sort(function (a, b) { return b.number - a.number; });
      if (!episodes.length) {
        list.appendChild(el("p", { class: "muted" }, "Перший епізод — незабаром."));
        return;
      }
      episodes.forEach(function (ep) {
        var card = el("article", { class: "episode", id: "ep-" + ep.number });
        var meta = ["Епізод " + ep.number];
        if (ep.date) meta.push(formatDate(ep.date));
        if (ep.duration) meta.push(ep.duration);
        card.appendChild(el("div", { class: "meta" }, meta.join(" · ")));
        card.appendChild(el("h3", {}, ep.title));
        if (ep.guest) card.appendChild(el("div", { class: "meta" }, "Гість: " + ep.guest));
        if (ep.summary) card.appendChild(el("p", {}, ep.summary));
        if (ep.audio) card.appendChild(el("audio", { controls: "", preload: "none", src: ep.audio }));
        var links = el("div", { class: "links" });
        Object.keys(ep.links || {}).forEach(function (name) {
          if (ep.links[name]) links.appendChild(el("a", { href: ep.links[name], target: "_blank", rel: "noopener" }, name));
        });
        if (links.childNodes.length) card.appendChild(links);
        list.appendChild(card);
      });
    })
    .catch(function () {
      document.getElementById("episode-list").innerHTML = '<p class="muted">Не вдалося завантажити список епізодів.</p>';
    });
})();
