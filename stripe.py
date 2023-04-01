# 1. Process Checkout Pipeline
@app.route("/checkout", methods=['POST'])
def processPayment():
    response = request.get_json()
    cid = response["cid"]
    # Step 1 Get Customer Stripe Details
    getUser_URL = accountMSURL + "/getuser/"+str(cid)
    customerData = invoke_http(getUser_URL, method='GET')
    customerStripeID = customerData['data']["stripedata"]["customerStripeID"]

    # Step 2 Calculate amount of items in cart
    amount = calculateAmount(cid)
    if amount == False:
        message = "Calculate amount error"
        channel.basic_publish(exchange=exchangename, routing_key="checkout.error",
                              body=message, properties=pika.BasicProperties(delivery_mode=2))
        return jsonify(
            {
                "message": message,
                "code": 400
            }
        )

    # Step 3 Send payment instructions to Stripe
    payment_URL = stripeMSURL+"/chargecustomer"
    payment_data = {
        "amount": amount,
        "currency": "sgd",
        "customer": customerStripeID
    }
    result = invoke_http(payment_URL, method='POST', json=payment_data)

    if result["code"] == 200:
        # Step 4 Send updates to Inventory MS
        cartDetails = getCartDetails(cid)
        cartItems = cartDetails["cartItems"]
        minusInvent = True
        for item in cartItems:
            productid = item[0]
            qty = item[1]
            updateInventoryQtyURL = inventoryMSURL + \
                "/api/products/"+str(productid)+"/"+str(qty)
            result = requests.get(updateInventoryQtyURL)
        if result.status_code != 200:
            return jsonify(
                {
                    "message": "Checkout failed error with inventory",
                    "res": result,
                    "code": 400
                })
        # Step 5 Send updates to Cart MS that Cart has been checked out
        checkoutURL = cartMSURL+"/cart"
        result = invoke_http(checkoutURL, method='PUT',
                             json={"customerID": cid})
        if result["code"] == 201 or result["code"] == 200:
            return jsonify(
                {
                    "message": "Checkout successful",
                    "code": 200
                })
        else:
            message = "Checkout confirmation error, error with cartms"
            channel.basic_publish(exchange=exchangename, routing_key="checkout.info",
                                  body=message, properties=pika.BasicProperties(delivery_mode=2))
            return jsonify(
                {
                    "message": message,
                    "code": 400
                }
            )
    else:
        message = "Stripe error"
        channel.basic_publish(exchange=exchangename, routing_key="checkout.info",
                              body=message, properties=pika.BasicProperties(delivery_mode=2))
        return jsonify(
            {
                "message": message,
                "code": 400
            }
        )