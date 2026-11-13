// Promo banner injected at the top of the page after load: pushes all content down.
setTimeout(() => {
  const banner = document.createElement("div");
  banner.style.cssText = "height:80px;background:#c0392b;color:#fff;display:grid;place-items:center";
  banner.textContent = "-20 % sur tout le site avec le code GRES20";
  document.body.prepend(banner);
}, 800);
