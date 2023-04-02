console.log("yes");
const stripe = Stripe(
  "pk_test_51Mmaq9Kcs6la72jh1ZMbbP5wP4yd0wbYZ43d1aDu09CDagPhLEet12Mcho1Nm2gApRmaPt8CCHrrFpWNsKb3h6De00PYaYjnbP"
);

const place_order_URL = "http://localhost:5100/place_order";
const payment_URL = "http://localhost:6002/payment";
const box_url = "http://localhost:5000/box";
const restaurant_url = "http://localhost:5000/restaurant";

// HERE CREATE PAYMENT ELEMENT
const options = {
  mode: "payment",
  amount: 1099, // this one needs to be generated dynamically from UI NOTE
  currency: "sgd",
  appearance: {
    theme: "stripe",
  },
};

// Set up Stripe.js and Elements to use in checkout form
const elements = stripe.elements(options);

// HERE Create and mount the Payment Element
const paymentElement = elements.create("payment", {
  layout: {
    type: "accordion",
    defaultCollapsed: false,
    radios: true,
    spacedAccordionItems: false,
  },
  customer: {
    customerNumber: "123456",
    quantity: "1",
  },
});
paymentElement.mount("#payment-element");

// // CALLED ON LOAD
// createIntent();

// // CREATE PAYMENT INTENT -------------------------------------
// let intentId;

// // NOTE: We will create Intent on load -> connecting to payment.py
// async function createIntent() {
//     const response = await fetch(`${payment_URL}/create-payment-intent`, {
//         method: "POST",
//         headers: {
//             "Content-Type": "application/json"
//         },
//         body: JSON.stringify(payment)
//     })

//     // obtain client secret -> to confirm payment
//     const {
//         clientSecret,
//         payment_intent_id
//     } = await response.json();

//     intentId = payment_intent_id;
//     // get payment intent id as global to retrieve the client secret to confirm payment later
// }

// NOTE: Create payment Intent will be done by place order

// form.addEventListener("submit", async (event) => {
//   // We don't want to let default form submission happen here,
//   // which would refresh the page.
//   event.preventDefault();

//   // Trigger form validation and wallet collection
//   const { error: submitError } = await elements.submit();
//   if (submitError) {
//     handleError(submitError);
//     return;
//   }

//   if (error.type === "card_error" || error.type === "validation_error") {
//     showMessage(error.message);
//   } else {
//     showMessage("An unexpected error occurred.");
//   }

//   setLoading(false);

//   // Create the PaymentIntent and obtain clientSecret

//   // Confirm the PaymentIntent using the details collected by the Payment Element
//   const { error } = await stripe.confirmPayment({
//     elements,
//     clientSecret,
//     confirmParams: {
//       return_url: "https://example.com/order/123/complete",
//     },
//   });

//   if (error) {
//     // This point is only reached if there's an immediate error when
//     // confirming the payment. Show the error to your customer (for example, payment details incomplete)
//     handleError(error);
//   } else {
//     // Your customer is redirected to your `return_url`. For some payment
//     // methods like iDEAL, your customer is redirected to an intermediate
//     // site first to authorize the payment, then redirected to the `return_url`.
//   }
// });

// Show a spinner on payment submission
