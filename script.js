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