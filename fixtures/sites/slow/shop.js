// Minimal cart stored in localStorage: enough for the add-to-cart check of the crawler.
const KEY = "cart";
const euros = (n) => n.toFixed(2).replace(".", ",") + " €";
const readCart = () => JSON.parse(localStorage.getItem(KEY) || "[]");

function updateCount() {
  const count = document.getElementById("cart-count");
  if (count) count.textContent = readCart().length;
}

document.querySelectorAll(".add-to-cart").forEach((button) => {
  button.addEventListener("click", () => {
    const cart = readCart();
    cart.push({ name: button.dataset.name, price: Number(button.dataset.price) });
    localStorage.setItem(KEY, JSON.stringify(cart));
    updateCount();
  });
});

const items = document.getElementById("cart-items");
if (items) {
  const cart = readCart();
  for (const item of cart) {
    const li = document.createElement("li");
    li.textContent = `${item.name} — ${euros(item.price)}`;
    items.append(li);
  }
  const subtotal = cart.reduce((sum, item) => sum + item.price, 0);
  const shipping = subtotal >= 50 ? 0 : 4.9;
  document.getElementById("cart-empty").hidden = cart.length > 0;
  document.getElementById("subtotal").textContent = euros(subtotal);
  document.getElementById("shipping").textContent =
    cart.length === 0 ? "—" : shipping ? euros(shipping) : "Offerte";
  document.getElementById("total").textContent = euros(cart.length ? subtotal + shipping : 0);
}

updateCount();
