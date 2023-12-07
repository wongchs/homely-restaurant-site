$(document).ready(function() {
    updateCart();
  
    function updateCart() {
      $.ajax({
        type: "GET",
        url: "/get_cart/",  // Replace with your actual URL
        success: function(response) {
          updateCartUI(response);
        },
        error: function(error) {
          console.error("Error fetching cart:", error);
        }
      });
    }
  
    function updateCartUI(cartData) {
      var cartItemsHtml = "";
      var cartSubtotal = 0;
  
      cartData.forEach(function(item) {
        var subtotal = item.price * item.quantity;
        cartSubtotal += subtotal;
  
        cartItemsHtml += `
          <tr>
            <td><img src="${item.image}" alt="product-image" /></td>
            <td>${item.name}</td>
            <td>RM${item.price.toFixed(2)}</td>
            <td><input type="number" value="${item.quantity}" /></td>
            <td>RM${subtotal.toFixed(2)}</td>
          </tr>
        `;
      });
  
      $("#cart-items").html(cartItemsHtml);
      $("#cart-subtotal").text("RM" + cartSubtotal.toFixed(2));
      $("#cart-total").text("RM" + cartSubtotal.toFixed(2));
    }
  });