function changeQuantity(button, delta) {
  var quantityInput = button.parentElement.querySelector(".quantity-input");
  var currentQuantity = parseInt(quantityInput.value);
  if (currentQuantity + delta > 0) {
    quantityInput.value = currentQuantity + delta;
  }
}
