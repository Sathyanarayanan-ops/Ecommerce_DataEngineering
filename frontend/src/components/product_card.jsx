import * as React from 'react';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

export default function ImgMediaCard({
    image_input,
    alt_name,
    product_name,
    cost,
    onBuy,        
    onAddToCart,  
    sx,           
  }) {
    return (
      <Card sx={{ maxWidth: 345, ...sx }}>
        <CardMedia
          component="img"
          alt={alt_name}
          height="140"
          image={image_input}
        />
        <CardContent>
          <Typography gutterBottom variant="h5">
            {cost}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            {product_name}
          </Typography>
        </CardContent>
        <CardActions>
          <Button size="small" onClick={onBuy}>Buy Now</Button>
          <Button size="small" onClick={onAddToCart}>Add to Cart</Button>
        </CardActions>
      </Card>
    );
  }
  