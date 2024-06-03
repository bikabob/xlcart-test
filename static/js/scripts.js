document.addEventListener("DOMContentLoaded", function() {
    var ProductImg = document.getElementById("ProductImg");
    var SmallImg = document.getElementsByClassName("small-img");

    for (let i = 0; i < SmallImg.length; i++) {
        SmallImg[i].onclick = function () {
            ProductImg.src = SmallImg[i].src;
        }
    }
});

$(document).ready(function() {
    $("#cartButton").click(function(e) {
        e.preventDefault();
        var url = "{% url 'furniture:cart_view' %}";
        Swal.fire({
            title: 'Go to Cart?',
            text: 'Do you want to proceed to your cart?',
            icon: 'info',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, Go to Cart'
        }).then((result) => {
            if (result.isConfirmed) {
                // If user confirms, redirect to cart page
                window.location.href = url;
            }
        });
    });
});




$(document).on("click", ".action-button", function (e) {
    e.preventDefault();
    $this = $(this);
    var text = $this.attr("data-text");
    var type = "warning";
    var confirmButtonText = "Yes";
    var confirmButtonColor = "#DD6B55";
    var url = $this.attr("href");
    var title = $this.attr("data-title");
    const csrfToken = document.getElementById('csrf-token-form').querySelector('input[name="csrfmiddlewaretoken"]').value;
    if (!title) {
      title = "Are you sure?";
    }
    var isReload = $this.hasClass("reload");
    var isRedirect = $this.hasClass("redirect");
    var noResponsePopup = $this.hasClass("no-response-popup");
  
    Swal.fire({
      title: title,
      text: text,
      icon: type,
      showCancelButton: true,
      confirmButtonColor: confirmButtonColor,
      confirmButtonText: confirmButtonText,
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.showLoading();
        window.setTimeout(function () {
          jQuery.ajax({
            type: "POST",
            url: url,
            dataType: "json",
            beforeSend: function(xhr) {
              // Include CSRF token in header (assuming you have a way to retrieve it)
              xhr.setRequestHeader('X-CSRFToken', csrfToken); // Replace csrfToken with your logic to retrieve the token
            },
            success: function (data) {
                var message = data["message"];
                var status = data["status"];
                var redirect = data["redirect"];
                var redirect_url = data["redirect_url"];
                var stable = data["stable"];
                var title = data["title"];

                Swal.hideLoading();

                if (status == "success") {
                    if (title) {
                        title = title;
                    } else {
                        title = "Success";
                    }
                    if (!noResponsePopup) {
                        Swal.fire({
                            icon: "success",
                            title: title,
                            text: message,
                            type: "success",
                        }).then((result) => {
                            if (stable != "yes") {
                                if (isRedirect && redirect == "yes") {
                                    window.location.href = redirect_url;
                                }
                                if (isReload) {
                                    window.location.reload();
                                }
                            }
                        });
                    }
                } else {
                    if (title) {
                        title = title;
                    } else {
                        title = "An Error Occurred";
                    }

                    Swal.fire(title, message, "error");

                    if (stable != "true") {
                        window.setTimeout(function () {}, 2000);
                    }
                }
            },
            error: function (data) {
                Swal.hideLoading();

                var title = "An error occurred";
                var message =
                    "An error occurred. Please try again later.";
                Swal.fire(title, message, "error");
            },
          });
        }, 100);
      }
    });
  });





  $(document).ready(function() {
    // Buy Now button click event handler
    $("#buyNowBtn").click(function(e) {
        e.preventDefault(); // Prevent default link behavior
        
        // Show SweetAlert pop-up for confirmation
        Swal.fire({
            title: 'Confirm Purchase',
            text: 'Are you sure you want to buy this product?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, Buy Now'
        }).then((result) => {
            if (result.isConfirmed) {
                // If user confirms, show order confirmed message
                Swal.fire({
                    title: 'Order Confirmed',
                    text: 'Your order has been confirmed!',
                    icon: 'success'
                });
            }
        });
    });
});

