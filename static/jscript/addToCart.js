$(document).ready(function () {
    $('.order-button').click(function () {
      const itemId = $(this).data('item-id');
      const quantity = $('.item-quantity').val();
      const price = parseFloat($('.item-price').text().replace('RM', '')); // Extract and parse the price
      const csrfToken = "{{ csrf_token }}";
  
      $.ajax({
        url: `/add_to_cart/${itemId}/${quantity}/`,
        type: 'POST',
        data: JSON.stringify({ price: price }),  // Include the price in the request payload
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken,
        },
        success: function (data) {
          alert(`Item added to the cart. Cart total: RM${data.cart_total.toFixed(2)}`);
        },
        error: function (error) {
          console.error('Error:', error);
        },
      });
    });
  });