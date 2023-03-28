<?php
require './vendor/autoload.php';
header('Content-Type:application:json');

$stripe = new \Stripe\StripeClient("sk_test_51M25gLJNS4gB3cUWOEkkGPcmXZCjJ0V0TsGbmq0dBZnsIvn97Mu7smxnLuopWOpa0bAhceZZdNtwC9TOBkfZRkP300O1mg1T0h");
$paymentIntent = $stripe->paymentIntent->create([
    'amount'=> 2000,
    'currency' => 'sgd',
    'payment_method_types'=>['card'],
    'description' =>'Payment to restaurant'

]);

echo json_encode(['client_secret'=>$paymentIntent->client_sercret]);

?>