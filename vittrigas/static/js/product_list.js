document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();

            const productId = this.dataset.productId;

            fetch(`/store/cart/add/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin'
            })
                .then(response => response.json())
                .then(data => {
                    const cartCountSpan = document.querySelector('.cart-count');
                    if (cartCountSpan) {
                        cartCountSpan.textContent = data.item_count;

                        if (data.item_count > 0) {
                            cartCountSpan.style.display = 'inline-block';
                        } else {
                            cartCountSpan.style.display = 'none';
                        }
                    }
                    const cartDropdownWrapper = document.querySelector('.cart-dropdown-wrapper');
                    if (cartDropdownWrapper) {
                        cartDropdownWrapper.innerHTML = data.cart_html;
                    }
                })

                .catch(error => {
                    console.error("Error:", error);
                });
        });
    });
    document.addEventListener('click', function (e) {
        if (e.target.matches('.qty-increase')) {
            const itemId = e.target.dataset.itemId;
            updateQuantity(itemId, 'increase');
        }
    });

    document.addEventListener('click', function (e) {
        if (e.target.matches('.qty-decrease')) {
            const itemId = e.target.dataset.itemId;
            updateQuantity(itemId, 'decrease');
        }
    });

    document.addEventListener('click', function (e) {
        if (e.target.matches('.qty-remove')) {
            const itemId = e.target.dataset.itemId;
            updateQuantity(itemId, 'remove');
        }
    });

    function updateCartDropdown() {
        let url = `/store/cart/get/dropdown/`;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json'
            }
        })
            .then(res => res.json())
            .then(data => {
                const wrapper = document.querySelector('.cart-dropdown-wrapper');
                if (wrapper) {
                    wrapper.innerHTML = data.cart_html;
                }
            })
            .catch(error => console.error("Update error:", error));
    }

    function updateQuantity(itemId, action) {
        let url = '';

        if (action === 'increase') {
            url = `/store/cart/item/${itemId}/increase/`;
        } else if (action === 'decrease') {
            url = `/store/cart/item/${itemId}/decrease/`;
        } else if (action === 'remove') {
            url = `/store/cart/item/${itemId}/remove/`;
        }

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCSRFToken(),
                'Content-Type': 'application/json'
            }
        })
            .then(res => res.json())
            .then(data => {
                const qtyElement = document.querySelector(`.cart-item[data-item-id="${itemId}"] .qty-number`);
                if (qtyElement) {
                    if (data.quantity > 0) {
                        qtyElement.textContent = data.quantity;
                    } else {
                        const cartItem = document.querySelector(`.cart-item[data-item-id="${itemId}"]`);
                        if (cartItem) {
                            cartItem.remove();
                        }
                    }
                }

                const cartCount = document.querySelector('.cart-count');
                if (cartCount && data.item_count !== undefined) {
                    cartCount.textContent = data.item_count;
                }
                if (data.item_count == 0) {
                    updateCartDropdown();
                }
            })
            .catch(error => console.error("Update error:", error));
    }


    function getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        return cookieValue;
    }
});
