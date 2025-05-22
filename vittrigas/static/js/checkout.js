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