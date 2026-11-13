// FakeReviews: imitates a heavy third-party reviews app, loaded synchronously in <head>.
window.FakeReviews = { version: "3.2.1" };

const start = Date.now();
while (Date.now() - start < 300) {
  // Busy loop: blocks the main thread like a large unoptimised bundle would.
}

document.addEventListener("DOMContentLoaded", () => {
  const badge = document.createElement("p");
  badge.textContent = "FakeReviews ★★★★★ 4,8/5 (127 avis)";
  document.querySelector("main")?.append(badge);
});
