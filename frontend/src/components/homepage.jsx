import * as React from 'react';
import { Box, Grid } from '@mui/material';
import ImgMediaCard from './product_card';

export default function HomePage() {
  const handleBuy = () => console.log('bought!');
  const handleAdd = () => console.log('added to cart!');

  // Define your products here
  const products = [
    {
      image_input: '/gettyimages-174478330-612x612.jpg',
      alt_name: 'cookie-card',
      product_name: 'Cookies',
      cost: '$3.99',
    },
    {
      image_input: '/istockphoto-1989575540-612x612.jpg',
      alt_name: 'milk-card',
      product_name: 'Milk',
      cost: '$2.99',
    },
    {
      image_input: '/istockphoto-1989575540-612x612.jpg',
      alt_name: 'egg-card',
      product_name: 'Eggs',
      cost: '$4.99',
    },
    {
      image_input: '/istockphoto-1989575540-612x612.jpg',
      alt_name: 'pizza-card',
      product_name: 'Frozen Pizza',
      cost: '$5.99',
    },
    {
        alt_name: 'ice-cream',
        product_name: 'Ice Cream',
        cost: '$2.99',
        image_input: '/istockphoto-1989575540-612x612.jpg',
    },
    {
        alt_name: 'cake-card',
        product_name: 'Cake',
        cost: '$9.99',
        image_input: '/istockphoto-1989575540-612x612.jpg',
    },
    {
        image_input: '/istockphoto-1989575540-612x612.jpg',
        alt_name: 'detergent-card',
        product_name: 'Detergent',
        cost: '$19.99',
    },
    {
        image_input: '/istockphoto-1989575540-612x612.jpg',
        alt_name: 'anti-freeze',
        product_name: 'Anti-Freeze',
        cost: '$19.99',
    },
    {
        image_input: '/istockphoto-1989575540-612x612.jpg',
        alt_name: 'Soda',
        product_name: 'Soda',
        cost: '$6.99',
    }
    
      
  ];

  return (
    <Box sx={{ flexGrow: 1, p: 2 }}>
      <Grid container spacing={2}>
        {products.map((prod, idx) => (
          <Grid item key={idx} xs={12} sm={6} md={4} lg={3}>
            <ImgMediaCard
              {...prod}
              onBuy={handleBuy}
              onAddToCart={handleAdd}
            />
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}
