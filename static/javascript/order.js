// order.js
$(document).ready(function() {
    // Assume you have some way to get the item details (name, price, quantity)
    var itemName = "Product Name";
    var itemPrice = 10.0;
    var itemQuantity = 2;
  
    addToCart(itemName, itemPrice, itemQuantity);
  
    function addToCart(name, price, quantity) {
      $.ajax({
        type: "GET",
        url: "/add_to_cart/",
        data: {
          name: name,
          price: price,
          quantity: quantity,
        },
        success: function(response) {
          // Success handling (optional)
          console.log("Item added to cart:", response);
  
          // After adding to cart, update the cart UI
          updateCart();
        },
        error: function(error) {
          console.error("Error adding to cart:", error);
        }
      });
    }
  
    function updateCart() {
      $.ajax({
        type: "GET",
        url: "/get_cart/",
        success: function(response) {
          updateCartUI(response);
        },
        error: function(error) {
          console.error("Error fetching cart:", error);
        }
      });
    }
  
    function updateCartUI(cartData) {
      // Update the cart UI based on the received cart data
      // This logic depends on your specific UI implementation
    }
  });