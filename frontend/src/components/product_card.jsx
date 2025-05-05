
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
  priceDisplay,
  surgeBadge,
  onBuy,
  sx
}) {
  return (
    <Card sx={{ ...sx }}>
      <CardMedia
        component="img"
        height="140"
        image={image_input}
        alt={alt_name}
      />
      <CardContent>
        <Typography gutterBottom variant="h5">
          {product_name}
        </Typography>
        {priceDisplay}
      </CardContent>
      <CardActions>
        <Button size="small" onClick={onBuy}>Buy Now</Button>
      </CardActions>
    </Card>
  );
}