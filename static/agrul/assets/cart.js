const CART_KEY = 'GIZ_PASSION_CART' 

const NAVBAR_CART_ID = 'navbar-cart'
const NAVBAR_TOTAL = 'navbar-total'
const NAVBAR_ITEMS_COUNT = 'navbar-count'
const NAVBAR_ITEMS_COUNT2 = 'navbar-count2'

const CHECKOUT_CART_ID = 'checkout-cart'
const CHECKOUT_TOTAL = 'checkout-total'
const CHECKOUT_TOTAL_2 = 'checkout-total_2'
const CHECKOUT_ITEMS_COUNT = 'checkout-count'

class Cart {
    constructor() {
        this.cart = [];
        this.loadCart();
    }

    loadCart() {

        let storedCart = JSON.parse(localStorage.getItem(CART_KEY));
        if (storedCart) {
            this.cart = storedCart;
        }
        this.updateCart()
    }

    saveCart() {
        localStorage.setItem(CART_KEY, JSON.stringify(this.cart));
    }

    addProduct(id, image, name, cost, qty = 1) {
        let item = this.getProduct(id);
        if (item) {
            item.qty += 1
        } else {
            this.cart.push({
                id: id,
                image: image,
                name: name,
                cost: parseFloat(cost),
                qty: qty,
            });
        }
        this.updateCart()
    }

    updateCart() {
        this.saveCart();
        this.renderElements()
    }

    getProduct(id) {
        return this.cart.find((item) => item.id === id);
    }

    adjustQty(id, qty) {
        let item = this.getProduct(id + "");
        if (item) {
            if (qty < 1) {
                removeFromCart(id)
            }
            else {
                item.qty = qty;
            }
        }
        this.updateCart()
    }

    getCartTotal() {
        let total = 0;
        this.cart.forEach((item) => {
            total += item.cost * item.qty;
        });
        return total;
    }

    getCartTotalItems() {
        let total = 0;
        this.cart.forEach((item) => {
            total += item.qty;
        });
        return total;
    }

    getCartItems() {
        return this.cart;
    }

    removeProduct(id) {
        let index = this.cart.findIndex((item) => item.id === id + "");
        if (index >= 0) {
            this.cart.splice(index, 1);
            this.updateCart()
        }
    }

    clearCart() {
        this.cart = [];
        this.updateCart()
    }

    renderElements() {
        this.renderProducts(document.getElementById(NAVBAR_CART_ID), this.renderProduct);
        this.renderProducts(document.getElementById(CHECKOUT_CART_ID), this.renderCheckoutProduct);

        this.renderInElement(document.getElementById(NAVBAR_ITEMS_COUNT), this.getCartTotalItems());
        this.renderInElement(document.getElementById(NAVBAR_ITEMS_COUNT2), this.getCartTotalItems());
        this.renderInElement(document.getElementById(CHECKOUT_ITEMS_COUNT), this.getCartTotalItems());

        this.renderInElement(document.getElementById(NAVBAR_TOTAL), formatNumber(this.getCartTotal()));
        this.renderInElement(document.getElementById(CHECKOUT_TOTAL), formatNumber(this.getCartTotal()));
        this.renderInElement(document.getElementById(CHECKOUT_TOTAL_2), formatNumber(this.getCartTotal()));

    }

    renderProducts(parent, renderFunction) {
        if (parent) {
            parent.innerHTML = "";
            this.cart.forEach((item) => {
                parent.innerHTML += renderFunction(item);
            });
        }
    }

    renderInElement(elem, value) {
        if (elem) {
            elem.innerHTML = ""
            elem.innerHTML = value
        }
    }

    renderProduct(item) {
        const new_cart_item = `
            <li>
                <div class="thumb">
                    <a href="index-3.html#" class="photo">
                        <img src="${item?.image}" alt="Thumb">
                    </a>
                    <a href="javascript:void(0)" class="remove-product" onClick="removeFromCart(${item.id})" >
                        <i class="fas fa-times"></i>
                    </a>
                </div>
                <div class="info">
                    <h6><a href="javascript:void(0)">${item?.name}</a></h6>
                    <p>${item?.qty}x - <span class="price">Kes ${formatNumber(item.cost)}/-</span></p>
                </div>
            </li>
        `
        const old_cart_item = `
            <tr>
                <td>
                    <div class="product-cart-image">
                        <img src="${item.image}" style="max-width: 30px" alt="">
                    </div>
                </td>
                <td>
                    ${item.name}
                    </br>
                    <small class='cart-item-price'>KES ${formatNumber(item.cost)}/-</small>
                </td>
                <td>${item.qty}</td>
                <td>${formatNumber(item.qty * item.cost)}</td>
            </tr>
      `;
      return new_cart_item;
    }

    renderCheckoutProduct(item) {
        return `
            <tr>
                <td>
                    <div class="cart-image">
                        <img src="${item.image}" alt="">
                    </div>
                </td>
                <td>
                    ${item.name}
                </td>
                <td>
                    ${formatNumber(item.cost)}/-
                </td>
                <td>
                <div class="d-flex align-items-center">
                    <button class="btn btn-outline-secondary" onclick="adjustQty(${item.id}, ${item.qty - 1})">
                        <i class="fa fa-minus"></i>
                    </button>
                    <div class="bg-light py-2 px-3 mx-1 rounded" style="max-width: 60px;">
                        ${item.qty}
                    </div>
                    <button class="btn btn-outline-primary" onclick="adjustQty(${item.id}, ${item.qty + 1})">
                        <i class="fa fa-plus"></i>
                    </button>
                </div>
                </td>
                <td>${formatNumber(item.qty * item.cost)}</td>
            </tr>
      `;
    }
}


function formatNumber(number, decimals = 2, decimalSeparator = ".", thousandsSeparator = ",") {
    if (number) {
        let parts = number.toFixed(decimals).split(".");
        parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, thousandsSeparator);
        return parts.join(decimalSeparator);
    }
    return 0
}


// Initiate a new cart
const cart = new Cart();

function addToCart(id, image, name, cost) {
    cart.addProduct(id, image, name, cost);
    toastr.info('Product added to cart')
}

function removeFromCart(id) {
    cart.removeProduct(id);
    toastr.info('Item removed from cart')
}

function adjustQty(id, qty) {
    cart.adjustQty(id, qty);
    toastr.info(`Item quantity adjusted`)
}

function clearCart() {
    cart.clearCart()
    toastr.info("Cart cleared!.")
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
        }
    }
});

function checkPhoneNumberLen() {
    const checkoutPhoneNumberInput = document.getElementById('checkout_phone_number');

    if (checkoutPhoneNumberInput) {
        checkoutPhoneNumberInput.addEventListener('input', () => {
            const currentValue = checkoutPhoneNumberInput.value;

            if (currentValue.length > 9) {
                const newValue = currentValue.slice(0, 9);
                checkoutPhoneNumberInput.value = newValue;
            }
        });
    }
}

checkPhoneNumberLen()

function placeOrder(url) {
    const loc = window.location
    const order_url = loc.protocol + "//" + loc.host + url

    const phone_number = document.getElementById('checkout_phone_number').value
    if (phone_number.length < 9) {
        toastr.error("Your MPesa phone number should be 9 digits long")
        return
    }
    else if (cart.getCartItems()?.length < 1) {
        toastr.error("Add items to cart before checkout")
        return
    }
    else {
        toastr.info("Placing order, please wait")
        $.ajax({
            type: "POST",
            url: order_url,
            data: { data: JSON.stringify(cart.getCartItems()), phone_number: phone_number },
            success: function (response) {
                console.log(response)
                if (response?.message === "success") {
                    toastr.success("Order placed successfully. Check your account to make the payment.")
                    cart.clearCart()
                }
            },
            error: function (xhr, status, error) {
                console.error("Error:", error);
            }
        });
    }
}

// function getCookie(name) {
//     var cookieValue = null;
//     if (document.cookie && document.cookie !== "") {
//         var cookies = document.cookie.split(";");
//         for (var i = 0; i < cookies.length; i++) {
//             var cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === name + "=") {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }

function makePayment(url) {
    const loc = window.location
    const order_url = loc.protocol + "//" + loc.host + url
    toastr.info("Creating invoice, please wait")
    $.ajax({
        type: "POST",
        url: order_url,
        data: { data: JSON.stringify(cart.getCartItems()) },
        success: function (response) {
            console.log(response)
            if (response?.message === "success") {
                toastr.success("Invoice created.")
                cart.clearCart()
            }
        },
        error: function (xhr, status, error) {
            console.error("Error:", error);
        }
    });
}