// import * as React from 'react';
// import { Box, Grid, Typography } from '@mui/material';
// import ImgMediaCard from './product_card';
// import axios from 'axios';

// export default function HomePage({ userEmail }) {
//   const [priceMap, setPriceMap] = React.useState({});
//   const [updateTrigger, setUpdateTrigger] = React.useState(0);

//   // Fetch latest prices with polling
//   React.useEffect(() => {
//     const fetchPrices = () => {
//       axios.get("http://localhost:8000/latest_prices")
//         .then(res => {
//           const map = {};
//           res.data.forEach(item => {
//             map[item.product_id] = {
//               base_price: item.base_price,
//               surge_price: item.surge_price
//             };
//           });
//           console.log("📦 Received prices:", map);
//           setPriceMap(map);
//         })
//         .catch(err => console.error("❌ Failed to fetch prices:", err));
//     };

//     // Initial fetch
//     fetchPrices();
    
//     // Set up polling every 5 seconds
//     const interval = setInterval(fetchPrices, 5000);
    
//     // Cleanup interval on unmount
//     return () => clearInterval(interval);
//   }, []);

//   // Handle product buy
//   const handleBuy = async (productId, productName) => {
//     try {
//       await axios.post("http://localhost:8000/buy", {
//         email: userEmail,
//         product_id: productId
//       });
//       alert(`✅ Purchased ${productName}`);
//     } catch (err) {
//       console.error(`❌ Failed to buy product ${productId}:`, err);
//     }
//   };

//   // Product list
//   const products = [
//     { id: 1, image_input: '/gettyimages-174478330-612x612.jpg', alt: 'cookies', product_name: 'Cookies' },
//     { id: 2, image_input: '/istockphoto-1989575540-612x612.jpg', alt: 'milk', product_name: 'Milk' },
//     { id: 3, image_input: '/istockphoto-1989575540-612x612.jpg', alt: 'eggs', product_name: 'Eggs' },
//     { id: 4, image_input: '/istockphoto-1989575540-612x612.jpg', alt: 'pizza', product_name: 'Frozen Pizza' },
//     { id: 5, image_input: '/istockphoto-1989575540-612x612.jpg', alt: 'ice cream', product_name: 'Ice Cream' },
//     { id: 6, image_input: '/istockphoto-1989575540-612x612.jpg', alt: 'cake', product_name: 'Cake' },
//     { id: 7, image_input: '/istockphoto-1989575540-612x612.jpg', alt: 'detergent', product_name: 'Detergent' },
//     { id: 8, image_input: '/istockphoto-1989575540-612x612.jpg', alt: 'anti-freeze', product_name: 'Anti‑Freeze' },
//     { id: 9, image_input: '/istockphoto-1989575540-612x612.jpg', alt: 'soda', product_name: 'Soda' },
//   ];

//   return (
//     <Box sx={{ flexGrow: 1, p: 2 }}>
//       <Grid container spacing={2}>
//         {products.map(prod => {
//           const priceInfo = priceMap[prod.id];
//           const base = priceInfo?.base_price;
//           const surge = priceInfo?.surge_price;
//           const isSurged = base != null && surge != null && base !== surge;

//           return (
//             <Grid item key={prod.id} xs={12} sm={6} md={4} lg={3}>
//               <ImgMediaCard
//                 image_input={prod.image_input}
//                 alt_name={prod.alt}
//                 product_name={prod.product_name}
//                 priceDisplay={
//                   base != null ? (
//                     isSurged ? (
//                       <Typography component="div">
//                         <s>${base.toFixed(2)}</s>
//                         <Typography component="span" sx={{ color: 'error.main', ml: 1 }}>
//                           ${surge.toFixed(2)}
//                         </Typography>
//                       </Typography>
//                     ) : (
//                       <Typography>${base.toFixed(2)}</Typography>
//                     )
//                   ) : (
//                     <Typography color="text.secondary">Loading price...</Typography>
//                   )
//                 }
//                 surgeBadge={isSurged}
//                 onBuy={() => handleBuy(prod.id, prod.product_name)}
//                 onAddToCart={() => handleBuy(prod.id, prod.product_name)}
//               />
//             </Grid>
//           );
//         })}
//       </Grid>
//     </Box>
//   );
// }
import * as React from 'react';
import { Box, Grid, Typography } from '@mui/material';
import ImgMediaCard from './product_card';
import axios from 'axios';

export default function HomePage({ userEmail }) {
  const [priceMap, setPriceMap] = React.useState({});
  const [loading, setLoading] = React.useState(true);
  const [updateCount, setUpdateCount] = React.useState(0);

  // Fetch prices with proper error handling
  const fetchPrices = React.useCallback(async () => {
    try {
      const response = await axios.get(
        `http://localhost:8000/latest_prices?_=${Date.now()}`,
        { headers: { 'Cache-Control': 'no-cache' } }
      );

      const newPriceMap = response.data.reduce((acc, item) => {
        acc[item.product_id] = {
          base: item.base_price,
          surge: item.surge_price,
          updated: Date.now()
        };
        return acc;
      }, {});

      console.log('🔄 Price update:', newPriceMap);
      setPriceMap(newPriceMap);
      setUpdateCount(c => c + 1);
    } catch (error) {
      console.error('⚠️ Price fetch error:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  // Proper polling setup
  React.useEffect(() => {
    let intervalId;
    
    const initFetch = async () => {
      await fetchPrices();
      intervalId = setInterval(fetchPrices, 3000);
    };

    initFetch();
    
    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [fetchPrices]);

  // Product list with fallback images
  const products = [
    { id: 1, name: 'Cookies', image: '/cookie.jpg' },
    { id: 2, name: 'Milk', image: '/milk.jpg' },
    { id: 3, name: 'Eggs', image: '/eggs.jpg' },
    { id: 4, name: 'Pizza', image: '/pizza.jpg' },
    { id: 5, name: 'Ice Cream', image: '/icecream.jpg' },
    { id: 6, name: 'Cake', image: '/cake.jpg' },
    { id: 7, name: 'Detergent', image: '/detergent.jpg' },
    { id: 8, name: 'Anti-Freeze', image: '/antifreeze.jpg' },
    { id: 9, name: 'Soda', image: '/soda.jpg' },
  ];

  // Price display component
  const PriceDisplay = ({ base, surge }) => {
    if (!base && !surge) return <Typography color="text.secondary">Loading...</Typography>;
    
    const isSurged = surge && base !== surge;
    const baseVal = base?.toFixed(2) || '?.??';
    const surgeVal = surge?.toFixed(2) || '?.??';

    return (
      <div>
        {isSurged ? (
          <Typography variant="h6" color="error">
            <s style={{ opacity: 0.5 }}>${baseVal}</s>
            <span style={{ marginLeft: '8px' }}>${surgeVal}</span>
          </Typography>
        ) : (
          <Typography variant="h6">${baseVal}</Typography>
        )}
        <Typography variant="caption" color="text.secondary">
          Updated {updateCount} times
        </Typography>
      </div>
    );
  };

  return (
    <Box sx={{ p: 3, minHeight: '100vh', backgroundColor: '#fafafa' }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 'bold' }}>
        E-Commerce Products
        {loading && (
          <Typography component="span" variant="body1" sx={{ ml: 2 }}>
            Loading prices...
          </Typography>
        )}
      </Typography>

      <Grid container spacing={3}>
        {products.map((product) => {
          const prices = priceMap[product.id] || {};
          const isSurged = prices.surge && prices.surge !== prices.base;

          return (
            <Grid item key={product.id} xs={12} sm={6} md={4} lg={3}>
              <ImgMediaCard
                image_input={product.image}
                alt_name={product.name}
                product_name={product.name}
                priceDisplay={<PriceDisplay {...prices} />}
                surgeBadge={isSurged}
                onBuy={() => handleBuy(product.id, product.name)}
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  transition: 'transform 0.2s',
                  '&:hover': { transform: 'translateY(-4px)' }
                }}
              />
            </Grid>
          );
        })}
      </Grid>
    </Box>
  );

  async function handleBuy(productId, productName) {
    try {
      await axios.post('http://localhost:8000/buy', {
        email: userEmail,
        product_id: productId
      });
      console.log(`✅ Purchased ${productName}`);
      fetchPrices(); // Force immediate refresh
    } catch (error) {
      console.error(`❌ Purchase failed: ${productName}`, error);
      alert(`Purchase failed: ${error.response?.data?.message || error.message}`);
    }
  }
}