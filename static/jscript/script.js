function changeQuantity(button, delta) {
  let quantityInput = button.parentElement.querySelector(".quantity-input");
  let currentQuantity = parseInt(quantityInput.value);
  if (currentQuantity + delta > 0) {
    quantityInput.value = currentQuantity + delta;
  }
}
