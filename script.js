const stripe = Stripe('pk_test_51M25gLJNS4gB3cUWC9UQDBWnQfcivrY2TdhUL0PGSTh5Gsu27E1WfJreVOxN2rCIy63Bt0qDGDD7ulYshCGmUcju00SnS84DEU')
const cardnum = document.querySelector('#cardnum')
const cardexp = document.querySelector('#cardexp')
const cardcvc = document.querySelector('#cardcvc')
const btn = document.querySelector('#PlaceOrder')
const sts = document.querySelector('.status')

const elements = stripe.elements()

const numElm = elements.create('cardNumber',{showIcon:true,iconStyle:'solid'})
numElm.mount(cardnum)

const expElm = elements.create('cardExpiry',{disabled:true})
expElm.mount(cardexp)

const cvcElm = elements.create('cardCvc',{disabled:true})
cvcElm.mount(cardcvc)

numElm.on('change',(e)=>{
    if(e.complete){
        expElm.update({disabled:false})
        expElm.focus()
    }
})
expElm.on('change',(e)=>{
    if(e.complete){
        cvcElm.update({disabled:false})
        cvcElm.focus()
    }

})
cvcElm.on('change',(e)=>{
    if(e.complete){
        btn.disabled = false
    }
})

btn.addEventListener('click', ()=>{
    fetch('./paymentIntent.php', {
        method:'POST', 
        headers:{'Content-Type': 'application/json'},
        body:{}
    })
    .then(res=>res.json())
    .then(payload => {
        stripe.confirmCardPayment(payload.client_secret, {
            payment_method:{card:numElm}
        }).then(transStat => {
            if(transStat.error){
                sts.innerHTML = `
                <strong>Error:  </string> ${transStat.error.message}
                `
            }
            else{
                sts.innerHTML = `
               <h3>${transStat.paymentIntent.description}</h3>
               <strong>Transction Id: </strong>${transStat.paymentIntent.id}<br>
               <strong>Amount deducted: </strong> ${transStat.paymentIntent.amount/100} ${transStat.paymentIntent.currency}
                `
            }
            sts.style.display='block'
        })
    })
})