console.log("Sanity check");

// Get Stripe publishable key
// this code will be made from the UI NOTE
fetch("/config")
  .then((result) => {
    return result.json();
  })
  //   "data" contains the public key for stripe API, which is needed to initialize Stripe.js and securely process payments using the Stripe API on the client side.
  .then((data) => {
    // Initialize Stripe.js
    const stripe = Stripe(data.publicKey);

    // NOTE when user clicks on the checkout button from index.html
    document.querySelector("#submitBtn").addEventListener("click", () => {
      // Get Checkout Session ID
      fetch("/create-checkout-session")
        .then((result) => {
          return result.json();
        })
        .then((data) => {
          console.log(data);
          // Redirect to Stripe Checkout
          return stripe.redirectToCheckout({ sessionId: data.sessionId });
        })
        .then((res) => {
          console.log(res);
        });
    });
  });
