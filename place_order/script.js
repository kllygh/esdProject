const stripe = Stripe(
  "pk_test_51M25gLJNS4gB3cUWC9UQDBWnQfcivrY2TdhUL0PGSTh5Gsu27E1WfJreVOxN2rCIy63Bt0qDGDD7ulYshCGmUcju00SnS84DEU"
);

// const cardnum = document.querySelector("#cardnum");
// const cardexp = document.querySelector("#cardexp");
// const cardcvc = document.querySelector("#cardcvc");
// const form = document.querySelector("#my-form");
// const sts = document.querySelector(".status");

// const mystyle = {
//   base: {
//     iconColor: "rgb(128, 128, 255)",
//     color: "rgb(128, 128, 255)",
//     fontFamily: "sans-serif",
//     "::placeholder": { color: "#757593" },
//   },
//   complete: { color: "green" },
// };

// const elements = stripe.elements();
const items = [{ id: "foodbox"}];
let elements;
initialize();
checkStatus()
document.querySelector("#my-form").addEventListener("submit",handleSubmit);

async function initialize() {
  const response = await fetch("/create-payment-intent", {
    method: "POST",
    headers: { "Content-Type": "application/json"},
    body: JSON.stringify({ items }),
  });
  const { clientSecret } = await response.json();
  const appearance = {them:'stripe',};

  elements = stripe.elements({appearance, clientSecret});

  const paymentElementOptions = {
    layout: "tabs",
  };

  const paymentElement = elements.create("payment", paymentElementOptions);
  paymentElement.mount("#payment-element")
}
async function handleSubmit(e){
  e.preventDefault();
  setLoading(true);

  const { error } = await stripe.confirmPayment({
    elements,
    confirmParams: {
      return_url: "http://localhost:4343/place_order.html",
    },
  });

  if (error.type === "card_error" || error.type === "validation_error"){
    showMessage(error.message);
  } else {
    showMessage("An unexpected error occurred.");
  }
  setLoading(false);
}

async function checkStatus(){
  const clientSecret = new URLSearchParams(window.location.search).get(
    "payment_intent_client_secret"
  );

  if (!clientSecret) {
    return;
  }

  const { paymentIntent }= await stripe.retrievePaymentIntent(clientSecret);
  switch (paymentIntent.status){
    case "succeeded":
      showMessage("Payment succeeded!");
      break;
      case "processing":
      showMessage("Your payment is processing.");
      break;
    case "requires_payment_method":
      showMessage("Your payment was not successful, please try again.");
      break;
    default:
      showMessage("Something went wrong.");
      break;
  }  
}

function showMessage(messageText){
  const messageContainer = document.querySelector("#payment-message");

  messageContainer.classList.remove("hidden");
  messageContainer.textContent = messageText;

  setTimeout(function () {
    messageContainer.classList.add("hidden");
    messageText.textContent = "";
  }, 4000);
}

function setLoading(isLoading){
  if (isLoading) {
    // Disable the button and show a spinner
    document.querySelector("#submit").disabled = true;
    document.querySelector("#spinner").classList.remove("hidden");
    document.querySelector("#button-text").classList.add("hidden");
  } else {
    document.querySelector("#submit").disabled = false;
    document.querySelector("#spinner").classList.add("hidden");
    document.querySelector("#button-text").classList.remove("hidden");
  }
}

// const numElm = elements.create("cardNumber", {
//   showIcon: true,
//   iconStyle: "solid",
//   style: mystyle,
// });
// numElm.mount(cardnum);

// const expElm = elements.create("cardExpiry", { style: mystyle });
// expElm.mount(cardexp);

// const cvcElm = elements.create("cardCvc", { style: mystyle });
// cvcElm.mount(cardcvc);
// document.querySelector("#my-form").addEventListener("click", function () {
//   console.log("good");
//   // fetch('./paymentIntent.php', {
//   //     method:'POST',
//   //     headers:{'Content-Type': 'application/json'},
//   //     body:{}
//   // })
//   // .then(res=>res.json())
//   // .then(payload => {
//   //     stripe.confirmCardPayment(payload.client_secret, {
//   //         payment_method:{card:numElm}
//   //     }).then(transStat => {
//   //         if(transStat.error){
//   //             sts.innerHTML = `
//   //             <strong>Error:  </string> ${transStat.error.message}
//   //             `
//   //         }
//   //         else{
//   //             sts.innerHTML = `
//   //            <h3>${transStat.paymentIntent.description}</h3>
//   //            <strong>Transction Id: </strong>${transStat.paymentIntent.id}<br>
//   //            <strong>Amount deducted: </strong> ${transStat.paymentIntent.amount/100} ${transStat.paymentIntent.currency}
//   //             `
//   //         }
//   //         sts.style.display='block'
//   //     })
//   // })
//   alert("button clicked!");
// });
