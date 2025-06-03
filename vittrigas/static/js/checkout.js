// Add a slash for the expiry
expire_text = document.getElementById("expire-text");
expire_text.addEventListener("input", () => {
    let value = expire_text.value.replace(/\//g, "");
    if (value.length >= 2) {
        value = value.slice(0, 2) + "/" + value.slice(2, 4);
    }  
    expire_text.value = value;
})

// Get the total price of the products in the cart
products_prices = document.getElementsByClassName("total-product-price");
total_price = 0;
for (var i=0; i<products_prices.length; i++) {
    total_price += Number(products_prices[i].textContent);
}

// Get the total vat computation
vat_pct = Number(document.getElementsByClassName("vat-pct")[0].textContent)/100;
vat_total = total_price * vat_pct;
vat_total = vat_total.toFixed(2);
total_price += Number(vat_total);

// Get the delivery computation
delivery_total = Number(document.getElementsByClassName("total-delivery")[0].textContent);
total_price += delivery_total;

// Reflect to the DOM
document.getElementsByClassName("total-vat")[0].textContent = vat_total;
document.getElementsByClassName("total-price")[0].textContent = total_price;

// console.log(total_price);

var cardDrop = document.getElementById('card-dropdown');
var activeDropdown;
cardDrop.addEventListener('click',function(){
  var node;
  for (var i = 0; i < this.childNodes.length-1; i++)
    node = this.childNodes[i];
    if (node.className === 'dropdown-select') {
      node.classList.add('visible');
       activeDropdown = node; 
    };
})

var logo = document.getElementsByClassName("payment-logo")[0];
window.onclick = function(e) {
  if (e.target.tagName === 'LI' && activeDropdown){
    if (e.target.innerHTML === 'Master Card') {
        logo.src = '/static/img/payment/mastercard.png';
        activeDropdown.classList.remove('visible');
        activeDropdown = null;
        e.target.innerHTML = document.getElementById('current-card').innerHTML;
        document.getElementById('current-card').innerHTML = 'Master Card';
    }
    else if (e.target.innerHTML === 'American Express') {
        logo.src = '/static/img/payment/amex.png';
        activeDropdown.classList.remove('visible');
        activeDropdown = null;
        e.target.innerHTML = document.getElementById('current-card').innerHTML;
        document.getElementById('current-card').innerHTML = 'American Express';      
    }
    else if (e.target.innerHTML === 'Visa') {
        logo.src = '/static/img/payment/visa.png';
        activeDropdown.classList.remove('visible');
        activeDropdown = null;
        e.target.innerHTML = document.getElementById('current-card').innerHTML;
        document.getElementById('current-card').innerHTML = 'Visa';
    }
    }
    else if (e.target.className !== 'dropdown-btn' && activeDropdown) {
        activeDropdown.classList.remove('visible');
        activeDropdown = null;
    }
}


