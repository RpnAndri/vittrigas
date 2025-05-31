document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault(); // Verhindert evtl. Standardverhalten

            const productId = this.dataset.productId;

            fetch(`/store/cart/add/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'X-Requested-With': 'XMLHttpRequest' // Wichtig, damit Django AJAX erkennt
                },
                credentials: 'same-origin' // Damit Cookies (inkl. Session) mitgesendet werden
            })
            .then(response => response.json())
            .then(data => {
                console.log("Product added via AJAX.");
                
                // Update der Cart-Zahl
                const cartCountSpan = document.querySelector('.cart-count');
                if (cartCountSpan) {
                    cartCountSpan.textContent = data.item_count;

                    if (data.item_count > 0) {
                        cartCountSpan.style.display = 'inline-block';
                    } else {
                        cartCountSpan.style.display = 'none';
                    }
                }
            })
            .catch(error => {
                console.error("Error:", error);
            });
        });
    });
    document.querySelectorAll('.qty-increase').forEach(button => {
        button.addEventListener('click', function () {
            const itemId = this.dataset.itemId;
            updateCartItemQuantity(itemId, 'increase');
        });
    });

    document.querySelectorAll('.qty-decrease').forEach(button => {
        button.addEventListener('click', function () {
            const itemId = this.dataset.itemId;
            updateCartItemQuantity(itemId, 'decrease');
        });
    });

    function updateCartItemQuantity(itemId, action) {
        fetch(`/store/cart/item/${itemId}/${action}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin',
        })
        .then(response => response.json())
        .then(data => {
            console.log("Update response:", data);
            if (data.success) {
                // Aktuell Beispiel: Seite neu laden (oder Update der DOM-Elemente per JS)
                location.reload(); 
            } else {
                alert('Update fehlgeschlagen');
            }
        })
        .catch(error => {
            console.error('Error updating cart item:', error);
        });
    }

    function getCSRFToken() {
        let cookieValue = null;
        const name = 'csrftoken';
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
