function removeProduct(cartId) {
        const qty = document.getElementById(`qty-${cartId}`).value;
        const data = {
            'cart_id': cartId,
            'qty': qty
        };

        fetch('http://127.0.0.1:6002/removeProduct', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.ok) {
                // Remove the product row from the table on success
                const row = document.getElementById(`product-row-${cartId}`);
                if (row) {
                    row.remove();
                }
            } else {
                console.error('Failed to remove product');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
