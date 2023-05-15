 function paymentFailed(){
            setTimeout(function(){
                  Swal.fire({
                  icon: 'error',
                  title: 'Payment Failed',
                  text: "Please try again, or use a different payment method",
                  showConfirmButton: true,
                  confirmButtonColor: '	#CD1B2B',
                })
         }, 1000);
        }

paypal.Buttons({
    style:{
        color:'white',
        shape:'pill'
    },
    createOrder:function(data,actions){
        return actions.order.create({
            purchase_units:[{
                amount:{
                    value:'4'
                }
            }]
        });
    },
    onApprove:function(data,actions){
        return actions.order.capture().then(function(orderData){
            console.log(orderData)
            const transaction = orderData.purchase_units[0].payments.captures[0];

            email = orderData.payer.email_address;
            amount = transaction.amount.value;
            tr_id = transaction.id;
            updatePayment()


        })
    },
    onCancel:function(data){
        paymentFailed()

    }

}).render('#cbtn1');




paypal.Buttons({
    style:{
        color:'white',
        shape:'pill'
    },
    createOrder:function(data,actions){
        return actions.order.create({
            purchase_units:[{
                amount:{
                    value:'15'
                }
            }]
        });
    },
    onApprove:function(data,actions){
        return actions.order.capture().then(function(orderData){
            console.log(orderData)
            const transaction = orderData.purchase_units[0].payments.captures[0];

            email = orderData.payer.email_address;
            amount = transaction.amount.value;
            tr_id = transaction.id;
            updatePayment()

        })
    },
    onCancel:function(data){
        paymentFailed()
    }

}).render('#cbtn2');



paypal.Buttons({
    style:{
        color:'white',
        shape:'pill'
    },
    createOrder:function(data,actions){
        return actions.order.create({
            purchase_units:[{
                amount:{
                    value:'24'
                }
            }]
        });
    },
    onApprove:function(data,actions){
        return actions.order.capture().then(function(orderData){
            console.log(orderData)
            const transaction = orderData.purchase_units[0].payments.captures[0];

            email = orderData.payer.email_address;
            amount = transaction.amount.value;
            tr_id = transaction.id;
            updatePayment()
        })
    },
    onCancel:function(data){
        paymentFailed()
    }

}).render('#cbtn3');