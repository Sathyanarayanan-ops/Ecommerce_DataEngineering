import * as React from 'react';
import { Box, Grid } from '@mui/material';
import ImgMediaCard from './product_card';
import axios from 'axios';

export default function HomePage({userEmail}) {

  // handle user id in the backend ?
  // here only handle request sent 
  // When POST is made, product name should be sent -> associate a product id with it 
  const handleBuy = async(productId, productName) => {
    // const endpoint = action === 'buy' ? '/buy' : '/cart/add';
    try{
        const {data} = await axios.post(
            `http://localhost:8000/buy`,
            {email: userEmail, product_id: productId}
        );
        alert(`Purchased ${productName}`);
    }catch(err){
        console.error(`Failed to buy product ${productId}:`,err)
    }
  };



  // Define your products here
  const products = [
    { id: 1, image_input: '/gettyimages-174478330-612x612.jpg', alt: 'cookies',      product_name: 'Cookies',      cost: '$3.99' },
    { id: 2, image_input: '/istockphoto-1989575540-612x612.jpg', alt: 'milk',        product_name: 'Milk',         cost: '$2.99' },
    { id: 3, image_input: '/istockphoto-1989575540-612x612.jpg', alt: 'eggs',        product_name: 'Eggs',         cost: '$4.99' },
    { id: 4, image_input: '/istockphoto-1989575540-612x612.jpg', alt: 'pizza',       product_name: 'Frozen Pizza', cost: '$5.99' },
    { id: 5, image_input: '/istockphoto-1989575540-612x612.jpg', alt: 'ice cream',   product_name: 'Ice Cream',    cost: '$2.99' },
    { id: 6, image_input: '/istockphoto-1989575540-612x612.jpg', alt: 'cake',        product_name: 'Cake',         cost: '$9.99' },
    { id: 7, image_input: '/istockphoto-1989575540-612x612.jpg', alt: 'detergent',   product_name: 'Detergent',    cost: '$19.99' },
    { id: 8, image_input: '/istockphoto-1989575540-612x612.jpg', alt: 'anti-freeze', product_name: 'Anti‑Freeze',  cost: '$19.99' },
    { id: 9, image_input: '/istockphoto-1989575540-612x612.jpg', alt: 'soda',        product_name: 'Soda',         cost: '$6.99'   },
  ];


  return (
    <Box sx={{ flexGrow: 1, p: 2 }}>
      <Grid container spacing={2}>
        {products.map(prod => (
          <Grid item key={prod.id} xs={12} sm={6} md={4} lg={3}>
            <ImgMediaCard
                {...prod}
                // image_input={prod.image_input}
                // alt_name={prod.alt_name}
                // product_name={prod.product_name}
                // cost = {prod.cost}
                onBuy={() => handleBuy(prod.id, prod.product_name)}
                onAddToCart={() => handleBuy(prod.id,prod.product_name)}
            />
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}
