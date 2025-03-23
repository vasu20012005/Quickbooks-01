let cart = JSON.parse(localStorage.getItem('cart')) || [];

function addToCart(name, price) {
  cart.push({ name, price });
  localStorage.setItem('cart', JSON.stringify(cart));
  alert(`${name} has been added to your cart.`);
}

function buyNow(name, price) {
  cart.push({ name, price });
  localStorage.setItem('cart', JSON.stringify(cart));
  window.location.href = 'cart.html';
}

function displayCart() {
  const cartList = document.getElementById('cart-list');
  const totalPriceEl = document.getElementById('total-price');
  if (!cartList || !totalPriceEl) return; // Ensure elements exist

  cartList.innerHTML = '';
  let total = 0;

  cart.forEach((item, index) => {
    total += item.price;
    const listItem = document.createElement('li');
    listItem.textContent = `${item.name} - ₹${item.price}`;
    const removeBtn = document.createElement('button');
    removeBtn.textContent = 'Remove';
    removeBtn.onclick = () => removeItem(index);
    listItem.appendChild(removeBtn);
    cartList.appendChild(listItem);
  });

  totalPriceEl.textContent = `Total: ₹${total}`;
}

function removeItem(index) {
  cart.splice(index, 1);
  localStorage.setItem('cart', JSON.stringify(cart));
  displayCart();
}

function checkout() {
  if (cart.length === 0) {
    alert('Your cart is empty!');
    return;
  }

  fetch('/order', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ order: cart })
  })
    .then(response => response.json())
    .then(data => {
      alert(data.message);
      cart = [];
      localStorage.removeItem('cart');
      displayCart();
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Error placing order. Try again.');
    });
}

if (window.location.pathname.endsWith('cart.html')) {
  displayCart();
}