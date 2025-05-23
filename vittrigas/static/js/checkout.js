// Get the total price of the products in the cart
products_prices = document.getElementsByClassName("total-product-price");
total_price = 0;
for (var i=0; i<products_prices.length; i++) {
    total_price += Number(products_prices[i].textContent);
}

// Get the total vat computation
vat_pct = Number(document.getElementsByClassName("vat-pct")[0].textContent)/100;
vat_total = total_price * vat_pct;
total_price += vat_total;

// Get the delivery computation
delivery_total = Number(document.getElementsByClassName("total-delivery")[0].textContent);
total_price += delivery_total;

// Reflect to the DOM
document.getElementsByClassName("total-vat")[0].textContent = vat_total;
document.getElementsByClassName("total-price")[0].textContent = total_price;

// console.log(total_price);

dropdown = document.getElementsByClassName("dropdown")[0];
current = document.getElementsByClassName("dropdown-current")[0];
options = document.getElementsByClassName("dropdown-option");

current.addEventListener('click', function() {
    dropdown.classList.toggle("open");
});


for (var i=0; i<options.length; i++) {
    var option = options[i];
    option.addEventListener('click', function () {
        var current_text = current.textContent;
        current.textContent = option.textContent;
        option.textContent = current_text;
        dropdown.classList.remove('open');
    });
};

window.addEventListener("click", (e) => {
    if (!dropdown.contains(e.target)) {
        dropdown.classList.remove("open");
    }
});

