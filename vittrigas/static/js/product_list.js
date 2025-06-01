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
            updateQuantity(itemId, 'increase');
        });
    });

    document.querySelectorAll('.qty-decrease').forEach(button => {
        button.addEventListener('click', function () {
            const itemId = this.dataset.itemId;
            updateQuantity(itemId, 'decrease');
        });
    });

    function updateQuantity(itemId, action) {
        fetch(`/store/cart/update/${itemId}/${action}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json'
            }
        })
        .then(res => res.json())
        .then(data => {
            // Update Menge im DOM
            const qtyElement = document.querySelector(`.cart-item[data-item-id="${itemId}"] .qty-number`);
            if (qtyElement) {
                qtyElement.textContent = data.quantity;
            }

            // Optional: Gesamtanzahl oben im Cart-Icon aktualisieren
            const cartCount = document.querySelector('.cart-count');
            if (cartCount && data.item_count !== undefined) {
                cartCount.textContent = data.item_count;
            }
        })
        .catch(error => console.error("Fehler beim Aktualisieren:", error));
    }

    function getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue;
    }
});
