const stripe = Stripe('pk_test_51M25gLJNS4gB3cUWC9UQDBWnQfcivrY2TdhUL0PGSTh5Gsu27E1WfJreVOxN2rCIy63Bt0qDGDD7ulYshCGmUcju00SnS84DEU')
const cardnum = document.querySelector('#cardnum')
const cardexp = document.querySelector('#cardexp')
const cardcvc = document.querySelector('#cardcvc')
var btn = document.querySelector('#PlaceOrder');
const sts = document.querySelector('.status')

const mystyle={
    base:{iconColor:'rgb(128, 128, 255)',
    color:'rgb(128, 128, 255)',
    fontFamily:'sans-serif',
    '::placeholder': { color:'#757593'}
    },
    complete:{ color:'green'}
}

const elements = stripe.elements()

const numElm = elements.create('cardNumber',{showIcon:true,iconStyle:'solid', style:mystyle})
numElm.mount(cardnum)

const expElm = elements.create('cardExpiry',{style:mystyle})
expElm.mount(cardexp)

const cvcElm = elements.create('cardCvc',{style:mystyle})
cvcElm.mount(cardcvc)

btn.addEventListener("click", function(){
    // fetch('./paymentIntent.php', {
    //     method:'POST', 
    //     headers:{'Content-Type': 'application/json'},
    //     body:{}
    // })
    // .then(res=>res.json())
    // .then(payload => {
    //     stripe.confirmCardPayment(payload.client_secret, {
    //         payment_method:{card:numElm}
    //     }).then(transStat => {
    //         if(transStat.error){
    //             sts.innerHTML = `
    //             <strong>Error:  </string> ${transStat.error.message}
    //             `
    //         }
    //         else{
    //             sts.innerHTML = `
    //            <h3>${transStat.paymentIntent.description}</h3>
    //            <strong>Transction Id: </strong>${transStat.paymentIntent.id}<br>
    //            <strong>Amount deducted: </strong> ${transStat.paymentIntent.amount/100} ${transStat.paymentIntent.currency}
    //             `
    //         }
    //         sts.style.display='block'
    //     })
    // })
    alert("button clicked!")
})